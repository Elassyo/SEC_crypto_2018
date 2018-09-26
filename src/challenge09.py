#!/usr/bin/python3

import base64
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
            key = bytes.fromhex(f.readline())
            iv = bytes.fromhex(f.readline())
            data = base64.b64decode(f.read())
            if len(key) == 0 or len (data) == 0:
                raise ValueError()
            if len(iv) != 16 or len(data) % 16 != 0:
                raise ValueError()
    except IOError as e:
        die('cannot open or read file: %s' % e.strerror, name=args[1])
    except ValueError:
        die('invalid data in file', name=args[1])

    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    try:
        aes = AES.new(key, AES.MODE_ECB)
        clear = b''.join(bytes(b ^ v for b, v in zip(aes.decrypt(block), iv)) for block, iv in zip(blocks, [iv] + blocks))
    except ValueError:
        die('invalid key or ciphertext')

    print(clear[:-clear[-1]].decode())


if __name__ == '__main__':
    main(sys.argv)
