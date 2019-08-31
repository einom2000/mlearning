import sys
import base64
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = 16
        self.cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)

    def encrypt(self, raw):
        raw = self._pad(raw)
        encrypted = self.cipher.encrypt(raw.encode('utf-8'))
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(self._unpad(decrypted), 'utf-8')

    def _pad(self, s):
        ss = s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        print('_pad to %s' % ss)
        return ss

    def _unpad(self, s):
        ss = s[:-ord(s[len(s)-1:])]
        print('_unpad to %s' % ss)
        return ss


if __name__ == '__main__':
    key = '`?.F(fHbN6XK|j!t'
    cipher = AESCipher(key)

    plaintext = '542#1504891440039'
    encrypted = cipher.encrypt(plaintext)
    print('Encrypted: %s' % encrypted)
    ciphertext = '5bgJqIqFuT8ACuvT1dz2Bj5kx9ZAIkODHWRzuLlfYV0='
    assert encrypted == ciphertext

    decrypted = cipher.decrypt(encrypted)
    print('Decrypted: %s' % decrypted)
    assert decrypted == plaintext
