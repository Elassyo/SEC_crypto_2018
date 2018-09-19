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
            data = [base64.b64decode(line) for line in f]
            if any(len(d) % 16 != 0 for d in data):
                raise ValueError()
    except IOError as e:
        die('cannot open or read file: %s' % e.strerror, name=args[1])
    except ValueError:
        die('invalid data in file', name=args[1])

    for line, d in enumerate(data):
        blocks = [d[i:i+16] for i in range(0, len(data))]
        if any(blocks.count(b) > 1 for b in blocks):
            print(line + 1)
            break


if __name__ == '__main__':
    main(sys.argv)
