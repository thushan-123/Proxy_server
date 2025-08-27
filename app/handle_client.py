import asyncio
import struct
import socket
from app.read import read_data
from app.send_res import send_response
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

import asyncio
import struct
import socket

async def handle_user(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        data = await reader.read(2)
        if len(data) < 2:
            print("Invalid greeting")
            writer.close()
            return

        ver, nmethods = data[0], data[1]
        methods = await reader.read(nmethods)
        print(f"Greeting: ver={ver}, nmethods={nmethods}, methods={methods}")

        writer.write(b"\x05\x00")
        await writer.drain()

        data = await reader.read(4)
        if len(data) < 4:
            print("Invalid request header")
            writer.close()
            return

        ver, cmd, rsv, atyp = data
        print(f"Request: ver={ver}, cmd={cmd}, atyp={atyp}")

        if atyp == 1:  # chk ipv4
            addr = await reader.read(4)
            address = socket.inet_ntoa(addr)
        elif atyp == 3:  # Domain
            domain_len = (await reader.read(1))[0]
            domain = await reader.read(domain_len)
            address = domain.decode()
        else:
            print("Unsupported ATYP")
            writer.close()
            return

        port_bytes = await reader.read(2)
        port = struct.unpack("!H", port_bytes)[0]

        print(f"Target: {address}:{port}")

        # Connect destn
        try:
            remote_reader, remote_writer = await asyncio.open_connection(address, port)
            writer.write(b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + struct.pack("!H", 0))
            await writer.drain()
        except Exception as e:
            print(f"Connection to {address}:{port} failed: {e}")
            writer.write(b"\x05\x01\x00\x01" + socket.inet_aton("0.0.0.0") + struct.pack("!H", 0))
            await writer.drain()
            writer.close()
            return

        async def relay(reader, writer):
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        break
                    writer.write(data)
                    await writer.drain()
            except Exception as e:
                print("Relay error:", e)
            finally:
                writer.close()

        asyncio.create_task(relay(reader, remote_writer))
        asyncio.create_task(relay(remote_reader, writer))

    except Exception as e:
        print("Handle_user error:", e)
        writer.close()
