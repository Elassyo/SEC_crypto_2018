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

    # find prefix and required prefix padding length
    b = encrypt(bytes(46))
    len_p = -1
    for i in range(0, len(b) - 16, 16):
        if i >= len(a) or a[i:i+16] != b[i:i+16] and b[i:i+16] == b[i+16:i+32]:
            len_p = i
            break
    if len_p == -1:
        die('failed to find prefix length: invalid blocksize or cipher mode')
    for i in range(16, -1, -1):
        if encrypt(bytes(15 + i))[len_p:len_p+16] != b[len_p:len_p+16]:
            len_pp = i
            break

    # find full padding length
    a = encrypt(bytes(len_pp))
    b = a
    i = 0
    while len(a) == len(b):
        i += 1
        b = encrypt(bytes(len_pp + i))
    c = b
    j = i
    while len(b) == len(c):
        j += 1
        c = encrypt(bytes(len_pp + j))

    # full, full padding and secret length
    len_f = len(a)
    len_fp = i
    len_s = len_f - len_p

    def decrypt(i, secret):
        #print(i, secret)
        if i == len_s - len_fp:
            if encrypt(bytes(len_pp) + secret + bytes(len_fp for i in range(len_fp)))[:len_f] == a:
                return secret
            return
        base = bytes(len_pp + len_s - i - 1)
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
