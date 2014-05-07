#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

import sys
import os
import ConfigParser
from libs import *
from xml.etree import ElementTree


class DuokanBox:
    xml = ''
    work_path = ''
    duokanbox = list()
    params = dict()
    site_list = list()

    def __init__(self):
        try:
            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            self.xml = config.get('config', 'xml')
            self.work_path = config.get('config', 'work_path')
            self.params['pn'] = config.get('param', 'pn')
            self.params['size'] = config.get('param', 'size')
            debug_msg('xml=%s' % self.xml)
            debug_msg('work_path=%s' % self.work_path)
            debug_msg('params=%s' % self.params)
        except IOError:
            print('IOError')
        if self.xml == '' or self.work_path == '':
            debug_msg(color_msg('Null.', RED, WHITE))
            sys.exit()

    def get_site(self):
        try:
            # debug_msg('xml=%s' % self.xml)
            os.chdir(self.work_path)
            root = ElementTree.parse(self.xml)
            if root:
                sites = root.findall('site')
                # debug_msg(sites)
                site_list = list()
                for site in sites:
                    if isinstance(site, ElementTree.Element):
                        # debug_msg(list(site))
                        ele_dict_tmp = dict()
                        for ele in list(site):
                            if isinstance(ele, ElementTree.Element):
                                # debug_msg('tag=%s,text=%s' % (ele.tag, ele.text))
                                ele_dict_tmp[ele.tag] = ele.text
                        site_list.append(ele_dict_tmp)
                self.site_list = site_list
                debug_msg(self.site_list)
            else:
                sys.exit()
        except IOError:
            print('IOError')


if __name__ == '__main__':
    dkb = DuokanBox()
    dkb.get_site()