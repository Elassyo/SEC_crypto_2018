#!/usr/bin/python3

import base64
import random
import re
import urllib.parse
from flask import Flask, request, session, make_response
from Crypto import Random
from Crypto.Cipher import AES

app = Flask(__name__)
app.secret_key = 'https://www.youtube.com/watch?v=LTl6OFnjslc'


@app.route('/challenge10', methods=['POST'])
def challenge10():
    data = base64.b64decode(request.get_data())

    if 'ch10' not in session:
        session['ch10'] = {
            'key': Random.new().read(16),
            'secret': b'hello there'
        }

    key = session['ch10']['key']
    secret = session['ch10']['secret']

    cleartext = data + secret
    padding = 16 - (len(cleartext) % 16)
    cleartext += bytes(padding for i in range(padding))

    ciphertext = AES.new(key, AES.MODE_ECB).encrypt(cleartext)

    return base64.b64encode(ciphertext)


@app.route('/challenge11/new_profile', methods=['POST'])
def challenge11_new_profile():
    data = base64.b64decode(request.get_data())

    if 'ch11' not in session:
        session['ch11'] = {
            'key': Random.new().read(16)
        }

    key = session['ch11']['key']

    data = re.sub(br'[&=]', b'', data)
    cleartext = b'email=' + data + b'&uid=10&role=user'
    padding = 16 - (len(cleartext) % 16)
    cleartext += bytes(padding for i in range(padding))

    ciphertext = AES.new(key, AES.MODE_ECB).encrypt(cleartext)

    return base64.b64encode(ciphertext)


@app.route('/challenge11/validate', methods=['POST'])
def challenge11_validate():
    data = base64.b64decode(request.get_data())

    if 'ch11' not in session:
        return 'KO'

    key = session['ch11']['key']

    cleartext = AES.new(key, AES.MODE_ECB).decrypt(data)
    cleartext = cleartext[:-cleartext[-1]]

    return b'OK' if b'role=admin' in cleartext.split(b'&') else b'KO'


@app.route('/challenge12', methods=['POST'])
def challenge12():
    data = base64.b64decode(request.get_data())

    if 'ch12' not in session:
        session['ch12'] = {
            'key': Random.new().read(16),
            'prefix': Random.new().read(random.randint(0, 128)),
            'secret': b'general kenobi'
        }

    key = session['ch12']['key']
    prefix = session['ch12']['prefix']
    secret = session['ch12']['secret']

    cleartext = prefix + data + secret
    padding = 16 - (len(cleartext) % 16)
    cleartext += bytes(padding for i in range(padding))

    ciphertext = AES.new(key, AES.MODE_ECB).encrypt(cleartext)

    return base64.b64encode(ciphertext)


@app.route('/challenge13/encrypt', methods=['POST'])
def challenge13_encrypt():
    data = base64.b64decode(request.get_data())

    if 'ch13' not in session:
        session['ch13'] = {
            'prefix': base64.b64encode(Random.new().read(96))[:random.randint(0, 128)],
            'iv': Random.new().read(16),
            'key': Random.new().read(16)
        }

    prefix = session['ch13']['prefix']
    iv = session['ch13']['iv']
    key = session['ch13']['key']

    data = re.sub(br'[;=]', b'', data)
    cleartext = b'title=' + prefix + b';content=' + data + b';type=jibberjabber;'
    len_p = len(b'title=' + prefix + b';content=')
    padding = 16 - (len(cleartext) % 16)
    cleartext += bytes(padding for i in range(padding))

    ciphertext = AES.new(key, AES.MODE_CBC, iv).encrypt(cleartext)

    return base64.b64encode(ciphertext)


@app.route('/challenge13/decrypt', methods=['POST'])
def challenge13_decrypt():
    data = base64.b64decode(request.get_data())

    if 'ch13' not in session:
        return 'KO'

    iv = session['ch13']['iv']
    key = session['ch13']['key']

    cleartext = AES.new(key, AES.MODE_CBC, iv).decrypt(data)
    cleartext = cleartext[:-cleartext[-1]]
    print(cleartext)

    return b'OK' if b'admin=true' in cleartext.split(b';') else b'KO'


@app.route('/challenge14/encrypt')
def challenge14_encrypt():
    if 'ch14' not in session:
        secrets = [
            b'000000Now that the party is jumping',
            b"000001With the bass kicked in and the Vega's are pumpin'",
            b'000002Quick to the point, to the point, no faking',
            b"000003Cooking MC's like a pound of bacon",
            b"000004Burning 'em, if you ain't quick and nimble",
            b'000005I go crazy when I hear a cymbal',
            b'000006And a high hat with a souped up tempo',
            b"000007I'm on a roll, it's time to go solo",
            b"000008ollin' in my five point oh",
            b'000009ith my rag-top down so my hair can blow'
        ]

        session['ch14'] = {
            'key': Random.new().read(16),
            'iv': Random.new().read(16),
            'secret': random.choice(secrets)
        }

    key = session['ch14']['key']
    iv = session['ch14']['iv']
    secret = session['ch14']['secret']

    cleartext = secret
    padding = 16 - (len(cleartext) % 16)
    cleartext += bytes(padding for i in range(padding))

    ciphertext = AES.new(key, AES.MODE_CBC, iv).encrypt(cleartext)

    return base64.b64encode(iv) + b'\n' + base64.b64encode(ciphertext)


@app.route('/challenge14/decrypt', methods=['POST'])
def challenge14_decrypt():
    data = request.get_data()
    data = data.split(b'\n')

    if len(data) != 2:
        return b'KO'

    iv = base64.b64decode(data[0])
    ciphertext = base64.b64decode(data[1])

    if 'ch14' not in session:
        return b'KO'

    key = session['ch14']['key']
    print(session['ch14']['secret'])

    cleartext = AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext)
    padding = cleartext[-1]
    if padding == 0 or not all(b == padding for b in cleartext[-padding:]):
        return b'Bad padding', '500 Internal Server Error'

    return b'OK'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
