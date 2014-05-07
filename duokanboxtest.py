#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

import ConfigParser


def test1():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    print(config.sections())
    pn = config.get('param', 'pn')
    size = config.get('param', 'size')
    print(pn)
    print(size)


if __name__ == '__main__':
    test1()





