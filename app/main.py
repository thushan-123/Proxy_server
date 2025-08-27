import asyncio
import struct
import socket

def handle_client():
    pass


async def start_proxy(host="127.0.0.1", port=1080):
    server = await asyncio.start_server(handle_client,host, port)
    address = server.sockets[0].getsockname()
    print(f"SOCKS 5 proxy server running on {host} port {port}")
    
    async with server:
        await server.serve_forever()

