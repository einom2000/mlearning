
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json

keys_file = 'keys_here.json'

with open(keys_file) as f:
    keys = json.load(f)

server_pub = keys['SERVER_PUB']
local_pub = keys['CLIENT_PUB']
local_pri = keys['PRIVATE_KEY']


recipient_key = RSA.importKey(local_pub)
print(recipient_key)
session_key = get_random_bytes(16)
print(session_key)

cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)


def encryption(data):
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode('utf-8'))

    return enc_session_key, cipher_aes.nonce, tag, ciphertext


enc_s_key, nonce, tag, ciphered = encryption('this is a test, whatever you said is true!')

print('enc_s_key = %s' % enc_s_key)
print('nonce = %s ' % nonce)
print('tag = %s ' % tag)
print('ciphered = %s' % ciphered)

private_key = RSA.import_key(local_pri)


cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_s_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphered, tag)
print(data.decode("utf-8"))
