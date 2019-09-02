
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json
import rsa_encrypto

keys_file = 'keys_here.json'

with open(keys_file) as f:
    keys = json.load(f)

server_pub = keys['SERVER_PUB']
local_pub = keys['CLIENT_PUB']
local_pri = keys['PRIVATE_KEY']



rsa_encrypto.encryption('this is a test, whatever you said is true!, but i don\'t trust you',local_pub,'bin\\en.bin' )

data = rsa_encrypto.decryption('bin\\en.bin', local_pri)
print(data)
