import socket
import sys
import datetime
import time
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with open('server_ip.json') as f:
    server = json.load(f)

server_address = (server['server_ip'], server['server_port'])
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)


try:
    for _ in range(10):
        message = str(datetime.datetime.now())
        print('sending %s' % message, file=sys.stderr)
        sock.sendall(message.encode('utf-8'))

        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(128)
            amount_received = len(data)
            print('received: %s' % data, file=sys.stderr)
        time.sleep(1)
finally:
    message = 'ENDED!'
    sock.sendall(message.encode('utf-8'))
    print('colosing socket', file=sys.stderr)
    sock.close()
