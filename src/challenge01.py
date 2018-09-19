#!/usr/bin/python3

import base64
import sys


def die(msg, name=sys.argv[0]):
    print('%s:' % name, msg, file=sys.stderr)
    sys.exit(84)


def main(args):
    if len(args) != 2:
        die('invalid number of arguments')
    try:
        with open(args[1], 'r') as f:
            data = bytes.fromhex(f.read())
    except IOError as e:
        die('cannot open or read file: %s' % e.strerror, name=args[1])
    except ValueError:
        die('invalid data in file', name=args[1])

    print(base64.b64encode(data).decode())


if __name__ == '__main__':
    main(sys.argv)
