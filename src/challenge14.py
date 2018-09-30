#!/usr/bin/python3

import base64
import sys
import urllib.request
import urllib.error


COOKIES={}


def die(msg, name=sys.argv[0]):
    print('%s:' % name, msg, file=sys.stderr)
    sys.exit(84)


def request(url, data=None, method='GET'):
    req = urllib.request.Request('http://127.0.0.1:5000/challenge14/' + url,
        method=method, data=data,
        headers={'Content-Type': 'text/plain'})
    if COOKIES:
        req.add_header('Cookie', '; '.join(key+'='+COOKIES[key] for key in COOKIES))
    try:
        r = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code != 500:
            die('server responded with code ' + r.code)
        else:
            r = e
    except urllib.error.URLError as e:
        die('connection error: ' + repr(e))

    for header in r.getheaders():
        if header[0] == 'Set-Cookie':
            cookie = header[1].split('; ')[0].split('=', 1)
            COOKIES[cookie[0]] = cookie[1]
    return r


def encrypt():
    data = request('encrypt').read()
    data = data.split(b'\n')
    if len(data) != 2:
        die('invalid response')
    return (base64.b64decode(d) for d in data)


def decrypt(iv, data):
    data = b'\n'.join(base64.b64encode(d) for d in [iv, data])
    return request('decrypt', data, 'POST').read().strip() == b'OK'


def main(args):
    if len(args) != 1:
        die('invalid number of arguments')

    iv, data = encrypt()

    secret = bytes()
    for i in range(len(data), 0, -16):
        # data up-to the current block
        d = data[:i]
        # previous block this current block was xored with
        p = (iv + data)[i-16:i]

        # intermediate values
        suffix = bytes()
        # secret block
        bs = bytes()

        for j in range(16):
            off = len(suffix) + 1
            prefix = bytes(16 - off)
            for k in range(256):
                corrupter = prefix + bytes([k]) + bytes(c ^ off for c in suffix)
                if decrypt(iv, d[:-32] + corrupter + d[-16:]):
                    intermediate = k ^ off
                    suffix = bytes([intermediate]) + suffix
                    bs = bytes([p[-off] ^ intermediate]) + bs
                    break

        secret = bs + secret

    secret = secret[:-secret[-1]]
    print(base64.b64encode(secret).decode())


if __name__ == '__main__':
    main(sys.argv)
