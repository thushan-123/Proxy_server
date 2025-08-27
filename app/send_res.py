import asyncio
import struct

SOCKS_VERSION = 5

ATYP_IPV4 =1

async def send_response(writer: asyncio.StreamWriter, 
                        rep: int,
                        atyp: int = ATYP_IPV4,
                        addr: bytes = b'\x00\x00\x00\x00',
                        port: bytes = b'\x00\x00'
                        ):
    res = struct.pack("!BBBB", SOCKS_VERSION, rep,0, atyp) +addr+ port
    writer.write(res)
    await writer.drain()
    
    