import socket
import sys


def connect(sock, server_address):
    sock.connect(server_address)


def close(sock):
    sock.close()


def bind_listen(sock, server_address, a):
    sock.bind(server_address)
    sock.listen(a)


def sock():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def server_accept(sock):
    connection, client_address = sock.accept()
    return connection, client_address


def send(sock, msg):  #msg = b''
    try:
        message = msg
        print('sending %s' % message, file=sys.stderr)
        sock.sendall(message)
    finally:
        return


def check_responce(sock, msg, length):  # msg = b''
    while True:
        data = sock.recv(length)
        if data and data == msg:
            print('received: %s' % data.decode('utf-8'), file=sys.stderr)
            break
    return


def receiving_data(sock, length):
    while True:
        data = sock.recv(length)
        if data:
            length = len(data)
            print('received data at length of %d' % length)
            break
    return data
