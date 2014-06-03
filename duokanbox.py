#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

#system lib
import ConfigParser
from xml.etree import ElementTree
import random
import urllib2
import json

#user lib
from libs import *

#staging or online
STAGING = 0


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

    def set_domain(self, domain):
        self.domain = domain

    def get_domain(self):
        return self.domain

    def set_xml(self, xml):
        self.xml = xml

    def get_xml(self):
        return self.xml

    def set_work_path(self, work_path):
        self.work_path = work_path

    def get_work_path(self):
        return self.work_path

    def set_params(self, params):
        self.params = params

    def get_params(self):
        return self.params

    def set_sites(self, sites):
        self.sites = sites

    def get_sites(self):
        return self.sites

    def set_categories(self, categories):
        self.categories = categories

    def get_categories(self):
        return self.categories

    def set_channels(self, channels):
        self.channels = channels

    def get_channels(self):
        return self.channels

    def set_musics(self, musics):
        self.musics = musics

    def get_musics(self):
        return self.musics

    def set_cp_ids(self, cp_ids):
        self.cp_ids = cp_ids

    def get_cp_ids(self):
        return self.cp_ids


# noinspection PyClassHasNoInit
class Site:
    m_id = 0
    name = ''
    main_url = ''
    sub_count = 0
    sub = ''
    param_or_not = 0
    m_url = ''

    def set_id(self, m_id):
        self.m_id = m_id

    def get_id(self):
        return self.m_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_main_url(self, main_url):
        self.main_url = main_url

    def get_main_url(self):
        return self.main_url

    def set_sub_count(self, sub_count):
        self.sub_count = sub_count

    def get_sub_count(self):
        return self.sub_count

    def set_sub(self, sub):
        self.sub = sub

    def get_sub(self):
        return self.sub

    def set_param_or_not(self, param_or_not):
        self.param_or_not = param_or_not

    def get_param_or_not(self):
        return self.param_or_not

    def set_m_url(self, m_url):
        self.m_url = m_url

    def get_m_url(self):
        return self.m_url


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
        xml = config.get('config', 'xml')
        info.set_xml(xml)
        work_path = config.get('config', 'work_path')
        info.set_work_path(work_path)
        params = dict()
        params['pn'] = config.get('param', 'pn')
        params['size'] = config.get('param', 'size')
        info.set_params(params)
        if STAGING == 1:
            domain = config.get('domains', 'test_domain')
        else:
            domain = config.get('domains', 'domain')
        info.set_domain(domain)
        self.m_info = info

    def get_site(self):
        sites = list()
        root = ElementTree.parse(self.m_info.xml)
        if root:
            read_sites = root.findall('site')
            for read_site in read_sites:
                tmp_site = Site()
                # assert isinstance(read_site, ElementTree.Element)
                tmp_site.set_id(int(read_site.findtext('m_id')))
                tmp_site.set_name(read_site.findtext('name'))
                tmp_site.set_main_url('%s%s' % (self.m_info.domain, read_site.findtext('main_url')))
                tmp_site.set_sub_count(int(read_site.findtext('sub_count')))
                tmp_site.set_sub(read_site.findtext('sub'))
                tmp_site.set_param_or_not(int(read_site.findtext('param_or_not')))
                sites.append(tmp_site)
        self.m_info.set_sites(sites)

    def init_param(self, pn=1, size=10):
        m_pn = self.m_info.get_params()['pn'] % pn
        m_size = self.m_info.get_params()['size'] % size
        param = '?%s&%s' % (m_pn, m_size)
        return param

    def init_subs(self, n_site=Site()):
        sub = n_site.get_sub()
        sub_count = n_site.get_sub_count()
        subs = ''
        rnd = random.randint(1, sub_count)
        debug_msg(color_msg('rnd=%s' % rnd))
        for j in xrange(rnd):
            tmp = sub % (j + 3)
            subs += tmp
        return subs

    def init_url(self, n_site=Site()):
        m_id = n_site.get_id()
        name = n_site.get_name()
        main_url = n_site.get_main_url()
        param_or_not = n_site.get_param_or_not()
        sub_count = n_site.get_sub_count()
        sub = n_site.get_sub()
        debug_msg('m_id=%s\nname=%s\nmain_url=%s\nsub_count=%s,sub=%s\nparam_or_not=%s' % (
            m_id, name, main_url, sub_count, sub, param_or_not))
        m_url = main_url
        if m_id == 0:
            pass
        elif m_id == 1:
            pass
        elif m_id == 2:
            pass
        elif m_id == 3:
            pass
        elif m_id == 4:
            pass
        elif m_id == 5:
            pass
        if sub_count != 0:
            m_url = m_url + self.init_subs(n_site)
        if param_or_not == 1:
            param = self.init_param()
            debug_msg(color_msg('param=%s' % param))
            m_url += param
        debug_msg(color_msg('url=%s' % m_url))
        n_site.m_url = m_url

    def req_url(self, n_site=Site()):
        try:
            request = urllib2.Request(n_site.m_url)
            response = urllib2.urlopen(request)
            read_str = response.read()
            debug_msg(read_str)
        except urllib2.HTTPError, e:
            print('\nError=%s' % e.code)

    def check_json(self):
        json.loads('')


if __name__ == '__main__':
    dkb = DuokanBox()
    dkb.init()
    for site in dkb.m_info.sites:
        dkb.init_url(site)
        dkb.req_url(site)