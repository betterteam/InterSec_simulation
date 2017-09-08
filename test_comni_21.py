import socket
from datetime import datetime
import struct
import json

server_address = ('localhost', 6789)
max_size = 4096

sendData = [{
    "Veh_id": 1,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 2,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 3,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 4,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 5,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 6,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 7,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 8,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 9,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 10,
    "arrival_time": 1,
    "arrival_lane": 1}]

i = 0

while i < 10:

    print(i)
    # Json Version
    print('Starting the client at', datetime.now())

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mes = bytes(json.dumps(sendData[i]), encoding='utf-8')

    client.sendto(mes, server_address)
    data, server = client.recvfrom(max_size)
    data = struct.unpack("i", data)

    print('At', datetime.now(), server, 'said', data)

    i += 1

client.close()