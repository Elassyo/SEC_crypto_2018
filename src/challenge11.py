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
    req = urllib.request.Request('http://127.0.0.1:5000/challenge11/' + url,
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


def new_profile(data):
    return base64.b64decode(request('new_profile', base64.b64encode(data)).read())


def validate(data):
    return request('validate', base64.b64encode(data)).read()


def main(args):
    if len(args) != 1:
        die('invalid number of arguments')

    a = new_profile(b'AAAAAAAAAAAAA')[:32]
    # -> b'email=AAAAAAAAAAAAA&uid=10&role='
    b = new_profile(b'AAAAAAAAAA' + b'admin' + bytes(11 for i in range(11)))[16:32]
    # -> b'admin' (+ padding)

    print(validate(a + b).decode())


if __name__ == '__main__':
    main(sys.argv)
