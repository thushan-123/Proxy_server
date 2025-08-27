import asyncio
import struct
import socket
from .read import read_data

SOCKS_VERSION = 5
NO_AUTH = 0

async def handle_user(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    
    try:
        version, method = await read_data(reader, 2)
        if version != SOCKS_VERSION:
            raise ValueError("unsupport version")
        
        new_methods = await read_data(reader,method)
        if NO_AUTH not in new_methods:
            raise ValueError("authentication err")
    except:
        pass
    
    
    