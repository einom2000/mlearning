import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 15200)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)
log = 'log.txt'
sock.listen(1)

while True:
    print('waiting for connection...', file=sys.stderr)
    connection, client_address = sock.accept()
    try:
        print('connection from: ' + str(client_address), file=sys.stderr)
        while True:
            data = connection.recv(128)
            print('received: "%s"' % data, file=sys.stderr)
            if data and data.decode('utf-8') != 'ENDED!':
                print('sending data back to the client', file=sys.stderr)
                with open(log, 'a') as log_file:
                    log_file.write(data.decode('utf-8') + '\n')
                connection.sendall(data)
            elif data.decode('utf-8') == 'ENDED!':
                connection.close()
                sys.exit()
            else:
                print('no more data from: ' + str(client_address), file=sys.stderr)
                break
    finally:
        connection.close()
