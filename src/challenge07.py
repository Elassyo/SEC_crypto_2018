#!/usr/bin/python3

import base64
import re
import sys
from Crypto.Cipher import AES


def die(msg, name=sys.argv[0]):
    print('%s:' % name, msg, file=sys.stderr)
    sys.exit(84)


def main(args):
    if len(args) != 2:
        die('invalid number of arguments')
    try:
        with open(args[1], 'r') as f:
            key = bytes.fromhex(re.sub(r'\s', '', f.readline()))
            data = base64.b64decode(''.join(f.readlines()))
            if len(key) == 0 or len(data) == 0:
                raise ValueError()
    except IOError as e:
        die('cannot open or read file: %s' % e.strerror, name=args[1])
    except ValueError:
        die('invalid data in file', name=args[1])

    try:
        clear = AES.new(key, AES.MODE_ECB).decrypt(data)
    except ValueError:
        die('invalid key or ciphertext')

    print(base64.b64encode(clear[:-clear[-1]]).decode())


if __name__ == '__main__':
    main(sys.argv)
