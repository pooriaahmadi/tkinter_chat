from config import *

def decode(data, format='utf-8'):
    return data.decode(format)

def encode(data, format='utf-8'):
    return data.encode(format)

def create_header(data, decode=False):
    data = f"{len(data):<{HEADER_SIZE}}"
    if decode:
        data = decode(data)
    return data

def get_length(message_header):
    return int(message_header)
