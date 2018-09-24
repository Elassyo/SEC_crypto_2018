#!/usr/bin/python3

import base64
import sys
import urllib.request
import urllib.error


COOKIES={}


def die(msg, name=sys.argv[0]):
    print('%s:' % name, msg, file=sys.stderr)
    sys.exit(84)


def request(data):
    req = urllib.request.Request('http://127.0.0.1:5000/challenge12',
        method='POST', data=data,
        headers={'Content-Type': 'text/plain'})
    if COOKIES:
        req.add_header('Cookie', '; '.join(key+'='+COOKIES[key] for key in COOKIES))
    try:
        r = urllib.request.urlopen(req)
        if r.status != 200:
            die('server responded with code ' + r.status)
        for header in r.getheaders():
            if header[0] == 'Set-Cookie':
                cookie = header[1].split('; ')[0].split('=', 1)
                COOKIES[cookie[0]] = cookie[1]
        return r
    except urllib.error.URLError as e:
        die('connection error: ' + repr(e))


def encrypt(data):
    return base64.b64decode(request(base64.b64encode(data)).read())


def main(args):
    if len(args) != 1:
        die('invalid number of arguments')

    # test if the secret string is empty
    a = encrypt(b'')
    if len(a) == 0:
        die('unknown string is empty')

    # test if the key is consistent (session cookie working)
    b = encrypt(b'')
    if a != b:
        die('failed to get session cookie\n' + str(COOKIES))

    # check the blocksize
    i = 0
    while len(a) == len(b):
        i += 1
        b = encrypt(bytes(i))
    c = b
    j = i
    while len(b) == len(c):
        j += 1
        c = encrypt(bytes(j))
    if j - i != 16:
        die('invalid blocksize')

    # check that the cipher mode is ECB
    #b = encrypt(bytes(32))
    #if b[0:16] != b[16:32]:
    #    die('invalid cipher mode')

    # full length (secret + padding) and secret length
    len_f = len(a)
    len_s = len_f - i
    print(len_f, len_s)
    return

    def decrypt(i, secret):
        #print(i, secret)
        if i == len_s:
            p = len_f - len_s
            if encrypt(secret + bytes(p for i in range(p)))[:len_f] == a:
                return secret
            return
        base = bytes(len_f - i - 1)
        unknown = encrypt(base)[len_f - 1]
        for j in range(256):
            c = bytes([j])
            if unknown == encrypt(base + secret + c)[len_f - 1]:
                res = decrypt(i + 1, secret + c)
                if res:
                    return res

    secret = decrypt(0, bytes())
    print(base64.b64encode(secret).decode())


if __name__ == '__main__':
    main(sys.argv)
