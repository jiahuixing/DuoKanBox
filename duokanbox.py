#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

import sys
import os
import ConfigParser
from xml.etree import ElementTree

from libs import *



# noinspection PyClassHasNoInit
class Info:
    xml = ''
    work_path = ''
    duokanbox = list()
    params = dict()
    site_list = list()
    cids = list()


class DuokanBox:
    m_info = Info()

    def __init__(self, info=Info()):
        if isinstance(info, Info):
            self.m_info = info
            self.init()
            if info.xml == '' or info.work_path == '':
                debug_msg(color_msg('Null.', RED, WHITE))
                sys.exit()
        else:
            sys.exit()

    def init(self):
        self.get_config()
        self.get_site()

    def get_config(self):
        try:
            info = self.m_info
            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            info.xml = config.get('config', 'xml')
            info.work_path = config.get('config', 'work_path')
            info.params['pn'] = config.get('param', 'pn')
            info.params['size'] = config.get('param', 'size')
            debug_msg('xml=%s' % info.xml)
            debug_msg('work_path=%s' % info.work_path)
            debug_msg('params=%s' % info.params)
        except IOError:
            print('IOError')

    def get_site(self):
        try:
            info = self.m_info
            # debug_msg('xml=%s' % self.xml)
            os.chdir(info.work_path)
            root = ElementTree.parse(info.xml)
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
                info.site_list = sorted(site_list)
                # for i in xrange(len(info.site_list)):
                #     site = info.site_list[i]
                #     debug_msg(site)
                #     if isinstance(site, dict):
                #         for item in sorted(site.items()):
                #             debug_msg('key=%s' % item[0])
                #             debug_msg('value=%s' % item[1])
                #             if isinstance(item, tuple):
                #                 debug_msg(item[0])
                #                 debug_msg(item[1])
            else:
                sys.exit()
        except IOError:
            print('IOError')

    # noinspection PyMethodMayBeStatic
    def req_site(self, site=None):
        if isinstance(site, dict):
            try:
                name = site['name']
                debug_msg(name)
            except KeyError:
                print('KeyError')
        else:
            print('Not a correct site.')
            sys.exit()


if __name__ == '__main__':
    m_info = Info()
    dkb = DuokanBox(m_info)
    for i in xrange(len(m_info.site_list)):
        dkb.req_site(m_info.site_list[i])