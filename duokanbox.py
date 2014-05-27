#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

#system lib
import ConfigParser
from xml.etree import ElementTree

#user lib
from libs import *


# noinspection PyClassHasNoInit
class Info:
    xml = ''
    work_path = ''
    params = dict()
    sites = list()


# noinspection PyClassHasNoInit
class Site:
    id = ''
    name = ''
    main_url = ''
    param_or_not = ''
    sub_count = ''
    sub = ''


# noinspection PyMethodMayBeStatic
class DuokanBox():
    m_info = Info()

    def __init__(self, info=Info()):
        self.m_info = info

    def init(self):
        try:
            self.get_config()
            self.get_site()
        except IOError:
            print('IOError')

    def get_config(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        info = Info()
        info.xml = config.get('config', 'xml')
        info.work_path = config.get('config', 'work_path')
        info.params['pn'] = config.get('param', 'pn')
        info.params['size'] = config.get('param', 'size')
        self.m_info = info

    def get_site(self):
        info = self.m_info
        root = ElementTree.parse(info.xml)
        if root:
            read_sites = root.findall('site')
            for read_site in read_sites:
                tmp_site = Site()
                assert isinstance(read_site, ElementTree.Element)
                tmp_site.id = read_site.findtext('id')
                tmp_site.name = read_site.findtext('name')
                tmp_site.main_url = read_site.findtext('main_url')
                tmp_site.param_or_not = read_site.findtext('param_or_not')
                tmp_site.sub_count = read_site.findtext('sub_count')
                tmp_site.sub = read_site.findtext('sub')
                info.sites.append(tmp_site)

    def req_site(self, n_site=Site()):
        d_id = n_site.id
        name = n_site.name
        main_url = n_site.main_url
        param_or_not = n_site.param_or_not
        sub_count = n_site.sub_count
        sub = n_site.sub
        debug_msg('id=%s,name=%s\nmain_url=%s\nsub_count=%s,param_or_not=%s,sub=%s' % (
            d_id, name, main_url, sub_count, param_or_not, sub))


if __name__ == '__main__':
    dkb = DuokanBox()
    dkb.init()
    debug_msg(dkb.m_info.sites)
    for site in dkb.m_info.sites:
        dkb.req_site(site)
