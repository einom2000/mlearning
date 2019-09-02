
import communication
import json
import rsa_encrypto


def sending(text, show_detail):
    en_file = 'bin\\en.bin'
    key_file = 'bin\\keys_here.json'
    server_file = 'bin\\server_ip.json'
    with open(key_file) as f:
        keys = json.load(f)

    recipient_pub = keys['SERVER_PUB']

    rsa_encrypto.encryption(text, recipient_pub, en_file)

    with open(en_file, 'rb') as f:
        data = f.read()

    with open(server_file) as f:
        server = json.load(f)

    server_address = (server['server_ip'], server['server_port'])

    sock = communication.sock()

    communication.connect(sock, server_address)

    communication.send(sock, b'HELLO', show_detail)
    communication.check_responce(sock, b'OK', 128)
    communication.send(sock, data, show_detail)
    communication.close(sock)


def main():
    pass


if __name__ == '__main()__':
    main()


