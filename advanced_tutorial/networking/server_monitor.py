import communication
import sys
import json
import rsa_encrypto


en_file = 'en.bin'
key_file = 'keys_here.json'

with open(key_file) as f:
    keys = json.load(f)

local_pri = keys['PRIVATE_KEY']

server_address = ('', 15200)

print('starting listen to  %s port %s' % server_address, file=sys.stderr)
sock = communication.sock()
communication.bind_listen(sock, server_address, 1)


while True:
    print('waiting for handshake...', file=sys.stderr)
    connection, client_address = communication.server_accept(sock)
    print('connection from: ' + str(client_address), file=sys.stderr)
    try:
        communication.check_responce(connection, b'HELLO', 128)
        communication.send(connection, b'OK', False)
        data = communication.receiving_data(connection, 1024)
        length = len(data)
        print('Server received data at length of %d' % length)
        with open(en_file, 'wb') as f:
            f.write(data)
        print('data saved!...')
        data = rsa_encrypto.decryption(en_file, local_pri)
        print('IT IS MEANS:....')
        print(data)
    finally:
        communication.close(connection)



