#!/usr/bin/env python
# -*- coding: utf-8 -*-  @Author  : bjsasc
import os
import sys


def upstr(s):
    return s.upper()

def filter_int(a):
    if a%2<>0:
        return True
    else:
        return False


def main():
    li = range(1, 7)
    print map(upstr, ['nihao'])
    print reduce(lambda x,y: x+y, li)
    # print filter(lambda x: x%2<>0, li)
    print filter(filter_int, li)
if __name__ == '__main__':
    sys.exit(int(main() or 0))
