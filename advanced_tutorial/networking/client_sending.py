import communication
import json

en_file= 'bin\\en.bin'

with open(en_file, 'rb') as f:
    data = f.read()

with open('server_ip.json') as f:
    server = json.load(f)

server_address = (server['server_ip'], server['server_port'])

sock = communication.sock()

communication.connect(sock, server_address)

communication.send(sock, b'HELLO', False)
communication.check_responce(sock, b'OK', 128)
communication.send(sock, data, False)
communication.close(sock)



