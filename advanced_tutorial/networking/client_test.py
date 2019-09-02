import socket
import sys
import datetime
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('144.202', 15200)  #
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
