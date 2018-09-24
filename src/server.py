#!/usr/bin/python3

import base64
import random
import urllib.parse
from flask import Flask, request, session
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

    data = data.replace(b'&', b'').replace(b'=', b'')
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
            'secret': b'hello there'
        }
        print('NEW session: len_p=%d' % len(session['ch12']['prefix']))

    key = session['ch12']['key']
    prefix = session['ch12']['prefix']
    secret = session['ch12']['secret']

    cleartext = prefix + data + secret
    padding = 16 - (len(cleartext) % 16)
    cleartext += bytes(padding for i in range(padding))

    ciphertext = AES.new(key, AES.MODE_ECB).encrypt(cleartext)

    return base64.b64encode(ciphertext)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
