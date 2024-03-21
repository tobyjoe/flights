#!/usr/bin/python

import sys
import time

import overhead

def main_loop():
    overhead.setup()
    while 1:
        overhead.update()
        overhead.draw()

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        overhead.shutdown()
        sys.exit(0)