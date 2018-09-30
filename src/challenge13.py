#!/usr/bin/python3

import base64
import sys
import urllib.request
import urllib.error


COOKIES={}


def die(msg, name=sys.argv[0]):
    print('%s:' % name, msg, file=sys.stderr)
    sys.exit(84)


def request(url, data):
    req = urllib.request.Request('http://127.0.0.1:5000/challenge13/' + url,
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
    return base64.b64decode(request('encrypt', base64.b64encode(data)).read())


def decrypt(data):
    return request('decrypt', base64.b64encode(data)).read()


def main(args):
    if len(args) != 1:
        die('invalid number of arguments')

    a = encrypt(bytes(0))
    if len(a) == 0 or len(a) % 16 != 0:
        die('empty or invalid ciphertext')
    b = encrypt(bytes(1))

    if a == b:
        die('input not used in ciphertext')

    diff = [i for i in range(0, len(a), 16) if a[i:i+16] != b[i:i+16]][0]
    a = b
    for i in range(1, 17):
        b = encrypt(bytes(1 + i))
        if a[diff:diff+16] == b[diff:diff+16]:
            len_pp = i
            break
        a = b
    a = encrypt(bytes(len_pp for i in range(len_pp)) + bytes(16) + b'\0admin\0true')
    a = list(a)
    a[diff+16] ^= ord(';')
    a[diff+16+6] ^= ord('=')
    a = bytes(a)
    print(decrypt(a).decode())


if __name__ == '__main__':
    main(sys.argv)
