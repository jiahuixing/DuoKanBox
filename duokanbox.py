#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

#system lib
import ConfigParser
from xml.etree import ElementTree

#user lib
from libs import *

#staging or online
STAGING = 1


# noinspection PyClassHasNoInit
class Info:
    domain = ''
    xml = ''
    work_path = ''
    params = dict()
    sites = list()
    categories = list()
    channels = list()
    musics = list()
    cp_ids = list()


# noinspection PyClassHasNoInit
class Site:
    m_id = ''
    name = ''
    main_url = ''
    sub_count = ''
    sub = ''
    param_or_not = ''


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
        config_file = 'config.ini'
        config.read(config_file)
        info = Info()
        info.xml = config.get('config', 'xml')
        info.work_path = config.get('config', 'work_path')
        info.params['pn'] = config.get('param', 'pn')
        info.params['size'] = config.get('param', 'size')
        if STAGING == 1:
            info.domain = config.get('domains', 'test_domain')
        else:
            info.domain = config.get('domains', 'domain')
        self.m_info = info

    def get_site(self):
        info = self.m_info
        root = ElementTree.parse(info.xml)
        if root:
            read_sites = root.findall('site')
            for read_site in read_sites:
                tmp_site = Site()
                # assert isinstance(read_site, ElementTree.Element)
                tmp_site.m_id = int(read_site.findtext('m_id'))
                tmp_site.name = read_site.findtext('name')
                tmp_site.main_url = '%s%s' % (self.m_info.domain, read_site.findtext('main_url'))
                tmp_site.sub_count = read_site.findtext('sub_count')
                tmp_site.sub = read_site.findtext('sub')
                tmp_site.param_or_not = read_site.findtext('param_or_not')
                info.sites.append(tmp_site)

    def req_site(self, n_site=Site()):
        m_id = n_site.m_id
        name = n_site.name
        main_url = n_site.main_url
        param_or_not = n_site.param_or_not
        sub_count = n_site.sub_count
        sub = n_site.sub
        debug_msg('m_id=%s\nname=%s\nmain_url=%s\nsub_count=%s,sub=%s\nparam_or_not=%s' % (
            m_id, name, main_url, sub_count, sub, param_or_not))
        if m_id == 0:
            debug_msg('0')
        elif m_id == 1:
            debug_msg('1')
        elif m_id == 2:
            debug_msg('2')
        elif m_id == 3:
            debug_msg('3')
        elif m_id == 4:
            debug_msg('4')
        elif m_id == 5:
            debug_msg('5')


if __name__ == '__main__':
    dkb = DuokanBox()
    dkb.init()
    for site in dkb.m_info.sites:
        dkb.req_site(site)