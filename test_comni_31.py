# Test UDP with Json format
# Client

import socket
from datetime import datetime
import struct
import json

server_address = ('localhost', 6788)
max_size = 4096

sendData = [{
    "Veh_id": 0,
    "arrival_time": 1,
    "arrival_lane": 1
}, {
    "Veh_id": 1,
    "arrival_time": 2,
    "arrival_lane": 1
}, {
    "Veh_id": 2,
    "arrival_time": 3,
    "arrival_lane": 1
}, {
    "Veh_id": 3,
    "arrival_time": 4,
    "arrival_lane": 1
}, {
    "Veh_id": 4,
    "arrival_time": 5,
    "arrival_lane": 1
}, {
    "Veh_id": 5,
    "arrival_time": 6,
    "arrival_lane": 1
}, {
    "Veh_id": 6,
    "arrival_time": 7,
    "arrival_lane": 1
}, {
    "Veh_id": 7,
    "arrival_time": 8,
    "arrival_lane": 1
}, {
    "Veh_id": 8,
    "arrival_time": 9,
    "arrival_lane": 1
}, {
    "Veh_id": 9,
    "arrival_time": 10,
    "arrival_lane": 1}]

i = 0

while i < 10:

    print(i)
    # Json Version
    print('Starting the client at', datetime.now())

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)

    mes = bytes(json.dumps(sendData[i]), encoding='utf-8')

    client.send(mes)
    data = client.recv(max_size)

    data = data.decode('utf-8')
    recData = json.loads(data)
    print('At', datetime.now(), 'server', 'said', recData)

    # data = struct.unpack("i", data)
    # print('At', datetime.now(), server, 'said', data)

    i += 1

client.close()