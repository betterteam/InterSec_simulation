
from datetime import datetime
import socket
import struct

server_address = ('localhost', 6789)
max_size = 4096

STOP_CHAT = True

while STOP_CHAT:
    check = 0

    print('starting the server at', datetime.now())
    print('waiting for a client to call.')
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(server_address)

    data, client = server.recvfrom(max_size)

    data = struct.unpack("i", data)
    print(data)

    if data[0] % 2 == 1:
       check = 1

    print('At', datetime.now(), client, 'said', data)

    str = struct.pack("i", check)
    server.sendto(str, client)

server.close()
