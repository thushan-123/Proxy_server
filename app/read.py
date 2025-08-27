import asyncio
import struct

async def read_data(reader: asyncio.StreamReader, n:int) -> bytes:
    data = await reader.readexactly(n)
    
    if len(data) != n:
        raise EOFError("end stream")
    return data