import socket
from datetime import datetime
import struct

server_address = ('localhost', 6789)
max_size = 4096

i = 1

while i < 100:

    print('Starting the client at', datetime.now())
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    mes = struct.pack("i", i)

    client.sendto(mes, server_address)
    data, server = client.recvfrom(max_size)

    data = struct.unpack("i", data)

    print('At', datetime.now(), server, 'said', data)

    i += 1

client.close()