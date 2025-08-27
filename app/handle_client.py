import asyncio
import struct
import socket
from .read import read_data
from .send_res import send_response
SOCKS_VERSION = 5
NO_AUTH = 0

CMD_CONNECT = 1

REPLY_SUCCEEDED = 0
REPLY_GENERAL_FAILURE = 1
REPLY_CONNECTION_NOT_ALLOWED = 2
REPLY_NETWORK_UNREACHABLE = 3
REPLY_HOST_UNREACHABLE = 4
REPLY_CONNECTION_REFUSED = 5
REPLY_TTL_EXPIRED = 6
REPLY_COMMAND_NOT_SUPPORTED = 7
REPLY_ADDRESS_TYPE_NOT_SUPPORTED = 8


ATYP_IPV4 = 1
ATYP_DOMAIN = 3
ATYP_IPV6 = 4

async def relay(source: asyncio.StreamReader, dest: asyncio.StreamWriter):
    try:
        while True:
            data = await source.read(4096)  # Read in 4KB chunks for efficiency
            if not data:
                break
            dest.write(data)
            await dest.drain()
    except Exception as e:
        print(f"Relay error: {e}")
    finally:
        dest.close()
        await dest.wait_closed()

async def handle_user(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    
    try:
        # handle handshake
        version, method = await read_data(reader, 2)
        if version != SOCKS_VERSION:
            raise ValueError("unsupport version")
        
        new_methods = await read_data(reader,method)
        
        if NO_AUTH not in new_methods:
            raise ValueError("authentication err")
        
        # res no auth
        writer.write(struct.pack("!BB", SOCKS_VERSION, NO_AUTH))
        await writer.drain()
        
        #handle req
        v, c,_, atyp = await read_data(reader,4)
        
        if v != SOCKS_VERSION or c != CMD_CONNECT:
            await send_response(writer, REPLY_COMMAND_NOT_SUPPORTED)
            return
        
        if atyp != ATYP_IPV4:
            await send_response(writer, REPLY_ADDRESS_TYPE_NOT_SUPPORTED)
            return
        
        addr_b = await read_data(reader, 4)
        port_b = await read_data(reader, 2)
        target_address = socket.inet_ntoa(addr_b)
        target_port = struct.unpack("!H", port_b)[0]
        
        # connect target
        try:
            target_reader, target_writer = await asyncio.open_connection(target_address, target_port)
            # Send success res
            await send_response(writer, REPLY_SUCCEEDED, atyp=ATYP_IPV4, addr=addr_b, port=port_b)
        except Exception as e:
            print(f"Connection failed: {e}")
            await send_response(writer, REPLY_GENERAL_FAILURE)
            return
        
        await asyncio.gather(
            relay(reader, target_writer),
            relay(target_reader,writer)
        )
        
    except Exception as e:
        print(f"user handle err {e}")
    finally:
        writer.close()
        await writer.wait_closed()
    
    
    