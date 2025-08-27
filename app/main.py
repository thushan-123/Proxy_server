import asyncio
import struct
import socket

from .handle_client import handle_user


async def start_proxy(host="127.0.0.1", port=1080):
    server = await asyncio.start_server(handle_user,host, port)
    address = server.sockets[0].getsockname()
    
    print(f"SOCKS 5 proxy server running on {address[0]} port {address[1]}")
    
    async with server:
        await server.serve_forever()
        
        


