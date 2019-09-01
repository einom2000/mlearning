import socket
import sys
import datetime
import json
from Crypto.PublicKey import RSA
from Crypto import Random
import time



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 15200)

print('starting listen to  %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)
keys_file= 'keys_here.json'
sock.listen(1)

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)

private_key = key.export_key(format='PEM').decode('utf-8')
print('new private key is :' + str(private_key))

server_public = key.publickey().export_key(format='PEM')

with open(keys_file) as f:
    keys = json.load(f)

keys.update({'PRIVATE_KEY': private_key})
keys.update({'SERVER_PUB' : server_public.decode('utf-8')})


while True:
    print('waiting for handshake...', file=sys.stderr)
    connection, client_address = sock.accept()
    try:
        print('connection from: ' + str(client_address), file=sys.stderr)
        while True:
            data = connection.recv(128)
            if data and data.decode('utf-8') == 'CHANGE_KEYS!':
                print('START TO EXCHANGE PUBLIC KEYS!', file=sys.stderr)
                data = b'PLS SEND!'
                connection.sendall(data)
                break
        while True:
            data = connection.recv(1024)
            if data:
                length = len(data)
                keys.update({'CLIENT_PUB':data.decode('utf-8')})
                print('CLIENT PUBLIC KEY RECEIVED WITH A LENGTH OF %d!' %length)
                with open (keys_file, 'w') as f:
                    json.dump(keys, f)
                time.sleep(1)
                data = b'SERVER_PUB!'
                connection.sendall(data)
                time.sleep(1)
                data = server_public
                length = len(data)
                connection.sendall(data)
                print('SERVER PUBLIC KEY SEND WITH A LENGTH OF %d!' %length)
                connection.close()
                print('------Keys Exchagned successfully....')
                print(keys)
                sys.exit()
    finally:
        connection.close()
