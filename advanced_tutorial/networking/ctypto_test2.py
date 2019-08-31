

def _decrypt_stealth_auth(content, authentication_cookie):
    from Crypto.Cipher import AES
    from Crypto.Util import Counter
    from Crypto.Util.number import bytes_to_long

    # byte 1 = authentication type, 2-17 = input vector, 18 on = encrypted content

    iv, encrypted = content[1:17], content[17:]
    counter = Counter.new(128, initial_value=bytes_to_long(iv))
    cipher = AES.new(authentication_cookie, AES.MODE_CTR, counter=counter)

    return cipher.decrypt(encrypted)