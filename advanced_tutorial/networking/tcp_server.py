import socket

def main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host, port))
