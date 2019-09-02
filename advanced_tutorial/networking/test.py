import client_sending
import json

text = '{"bot_hears": "pause", "pet_train": "pause"}'


client_sending.sending(text, False)

with open('test.json', 'w') as f:
    f.write(text)

with open('test.json') as f:
    dict = json.load(f)

print(dict)
