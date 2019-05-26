# Test Intersection Manager with UDP
# Get vehicle proposal, return the result

from datetime import datetime
import socket
import struct
import json

server_address = ('localhost', 6789)
max_size = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_address)

sendData = [{
    "Veh_id": 0,
    "result": 0
}, {
    "Veh_id": 1,
    "result": 0
}, {
    "Veh_id": 2,
    "result": 0
}, {
    "Veh_id": 3,
    "result": 0
}, {
    "Veh_id": 4,
    "result": 0
}, {
    "Veh_id": 5,
    "result": 0
}, {
    "Veh_id": 6,
    "result": 0
}, {
    "Veh_id": 7,
    "result": 0
}, {
    "Veh_id": 8,
    "result": 0
}, {
    "Veh_id": 9,
    "result": 0
}]


STOP_CHAT = True

while STOP_CHAT:
    check = 0

    print('starting the server at', datetime.now())
    print('waiting for a client to call.')


    data, client = server.recvfrom(max_size)

    data = data.decode('utf-8')
    recData = json.loads(data)

    print(recData["arrival_time"])

    if recData["arrival_time"] < 5:
        sendData[recData["Veh_id"]]["result"] = 1

    print(sendData)

    #Send Json
    mes = bytes(json.dumps(sendData[recData["Veh_id"]]), encoding='utf-8')
    server.sendto(mes, client)

server.close()