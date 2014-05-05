#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

import ConfigParser
from libs import *
# from xml.etree import ElementTree as ET


class DuokanBox:
    xml = ''
    work_path = ''

    def __init__(self):
        try:
            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            self.xml = config.get('config', 'xml')
            self.work_path = config.get('config', 'work_path')
            debug_msg(color_msg('xml=%s' % self.xml))
            debug_msg(color_msg('work_path=%s' % self.work_path))
        except IOError:
            print('IOError')

    def get_sites(self):
        pass


if __name__ == '__main__':
    dkb = DuokanBox()