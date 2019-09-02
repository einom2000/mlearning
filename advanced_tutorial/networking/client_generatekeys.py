import socket
import sys
import datetime
import time
from Crypto.PublicKey import RSA
from Crypto import Random
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)


publickey = key.publickey().export_key(format='PEM')

keys_file= 'keys_here.json'

with open(keys_file) as f:
    keys = json.load(f)

keys.update({'PRIVATE_KEY': key.export_key(format='PEM').decode('utf-8')})
keys.update({'CLIENT_PUB': publickey.decode('utf-8')})

with open('server_ip.json') as f:
    server = json.load(f)

server_address = (server['server_ip'], server['server_port'])  #
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)


try:
    message = 'CHANGE_KEYS!'
    print('sending %s' % message, file=sys.stderr)
    sock.sendall(message.encode('utf-8'))

    amount_received = 0
    amount_expected = len(message)


    while True:
        data = sock.recv(128)
        if data and data == b'PLS SEND!':
            print('received: %s' % data, file=sys.stderr)
            print('SENDING CLIENT PUBLIC KEY TO SERVER !')
            time.sleep(1)
            sock.sendall(publickey)
            length = len(publickey)
            print('CLIENT PUBLIC KEY SEND WITH A LENGTH OF %d!' %length)
        data = sock.recv(128)
        if data and data == b'SERVER_PUB!':
            print('START TO RECEIVE SERVER PUBLIC KEY !')
            data = sock.recv(1024)
            if data:
                length = len(data)
                print('SERVER PUBLIC KEY RECIEVED WITH A LENGTH OF %d!' % length)
                keys.update({'SERVER_PUB': data.decode('utf-8')})
                with open (keys_file, 'w') as f:
                    json.dump(keys, f)
                time.sleep(1)
                print('------Keys Exchagned successfully....')
                print(keys)
                sys.exit()
finally:
    message = 'ENDED!'
    sock.sendall(message.encode('utf-8'))
    print('colosing socket', file=sys.stderr)
    sock.close()

