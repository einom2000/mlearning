import requests, paramiko, os
import time


def change(ip):
    adds = ip.split('.')
    return '+'.join([adds[3], adds[0], str(int(adds[3]) // 2), adds[2], adds[1], str(int(adds[3]) // 5)])


def getip(k):
    ip = k.split('+')
    return '.'.join([ip[1], ip[4], ip[3], ip[0]])


while True:
    ip = requests.get('https://checkip.amazonaws.com').text.strip()

    print(ip)

    adds = change(ip)

    with open('d:\\myquest.bin', 'w') as file:
        file.write(adds)

    print(adds)

    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='119.45.4.205',username='myip', password='starBB')

    ftp_client=ssh_client.open_sftp()
    ftp_client.put('d:\\myquest.bin', '/home/myip/pass.bin')
    ftp_client.close()

    try:
        os.remove('d:\\myquest.bin')
    except FileNotFoundError:
        pass

    ftp_client=ssh_client.open_sftp()
    ftp_client.get('/home/myip/pass.bin','d:\\pass.bin')
    ftp_client.close()

    with open('d:\\pass.bin', 'r') as file:
        k = file.read()

    print(getip(k))

    os.remove('d:\\pass.bin')
    time.sleep(600)
