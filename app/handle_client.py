import asyncio
import struct
import socket
from .read import read_data

SOCKS_VERSION = 5
NO_AUTH = 0

REPLY_SUCCEEDED = 0
REPLY_GENERAL_FAILURE = 1
REPLY_CONNECTION_NOT_ALLOWED = 2
REPLY_NETWORK_UNREACHABLE = 3
REPLY_HOST_UNREACHABLE = 4
REPLY_CONNECTION_REFUSED = 5
REPLY_TTL_EXPIRED = 6
REPLY_COMMAND_NOT_SUPPORTED = 7
REPLY_ADDRESS_TYPE_NOT_SUPPORTED = 8

async def handle_user(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    
    try:
        version, method = await read_data(reader, 2)
        if version != SOCKS_VERSION:
            raise ValueError("unsupport version")
        
        new_methods = await read_data(reader,method)
        if NO_AUTH not in new_methods:
            raise ValueError("authentication err")
        writer.write(struct.pack("!BB", SOCKS_VERSION, NO_AUTH))
    except:
        pass
    
    
    