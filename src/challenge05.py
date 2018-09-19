#!/usr/bin/python3

import sys


def die(msg, name=sys.argv[0]):
    print('%s:' % name, msg, file=sys.stderr)
    sys.exit(84)


def main(args):
    if len(args) != 2:
        die('invalid number of arguments')
    try:
        with open(args[1], 'r') as f:
            key = bytes.fromhex(f.readline())
            data = bytes.fromhex(f.read())
    except IOError as e:
        die('cannot open or read file: %s' % e.strerror, name=args[1])
    except ValueError:
        die('invalid data in file', name=args[1])

    print(bytes(data[i] ^ key[i % len(key)] for i in range(len(data))).hex().upper())


if __name__ == '__main__':
    main(sys.argv)
