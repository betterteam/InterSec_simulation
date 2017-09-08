import socket
from datetime import datetime
import struct
import json

server_address = ('localhost', 6789)
max_size = 4096

sendData = [{
    'Veh_Num': 1
}, {
    'Veh_Num': 2
}]



i = 1

V_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

while i < 10:

    # Number Version
    print('Starting the client at', datetime.now())
    for i in range(10):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # mes = struct.pack("i", i)
        #mes = bytes(json.dumps(sendData), encoding='utf-8')
        mes = struct.pack("i", V_num[i])

        client.sendto(mes, server_address)
        data, server = client.recvfrom(max_size)

        data = struct.unpack("i", data)

        print('At', datetime.now(), server, 'said', data)

    i += 1

client.close()