import communication
import json
import rsa_encrypto

en_file= 'bin\\en.bin'
key_file = 'keys_here.json'

with open(key_file) as f:
    keys = json.load(f)

recipient_pub = keys['SERVER_PUB']

TEXT = 'are you ready'

rsa_encrypto.encryption(TEXT, recipient_pub,en_file)

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



