import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('144.202.93.164', 15200)  #
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)
try:
    message = 'This is a test message. It will be repeated.'
    print('sending %s' % message, file=sys.stderr)
    sock.sendall(message.encode('utf-8') )

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received = len(data)
        print('received: %s' % data, file=sys.stderr)
finally:
    print('colosing socket', file=sys.stderr)
    sock.close()
