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
            a = bytes.fromhex(f.readline())
            b = bytes.fromhex(f.readline())
            if len(a) == 0 or len(a) != len(b):
                raise ValueError()
    except IOError as e:
        die('cannot open or read file: %s' % e.strerror, name=args[1])
    except ValueError:
        die('invalid data in file', name=args[1])

    print(bytes(a ^ b for a, b in zip(a, b)).hex().upper())


if __name__ == '__main__':
    main(sys.argv)
