#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

#system lib
import ConfigParser
from xml.etree import ElementTree
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
    sids = list()
    cp_ids = list()

    result = dict()

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

    def set_sids(self, sids):
        self.sids = sids

    def get_sids(self):
        return self.sids

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

    status = 0
    msg = ''
    total = 0
    m_list = list()

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

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_msg(self, msg):
        self.msg = msg

    def get_msg(self):
        return self.msg

    def set_total(self, total):
        self.total = total

    def get_total(self):
        return self.total

    def set_list(self, m_list):
        self.m_list = m_list

    def get_list(self):
        return self.m_list


# noinspection PyMethodMayBeStatic
class DuokanBox():
    m_info = Info()

    def __init__(self, info=Info()):
        self.m_info = info

    def init(self):
        try:
            self.get_config()
            self.get_sites()
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

    def get_sites(self):
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
        m_id = n_site.get_id()
        sub = n_site.get_sub()
        sub_count = n_site.get_sub_count()
        subs = ''
        if m_id == 1:
            subs = sub % self.m_info.get_categories()[0]
        if m_id == 2:
            subs = sub % self.m_info.get_channels()[0]
        if m_id == 3:
            count = max(sub_count, len(self.m_info.get_sids()))
            for i in xrange(count):
                tmp = sub % self.m_info.get_sids()[i]
                subs += tmp
        if m_id == 4:
            count = max(sub_count, len(self.m_info.get_cp_ids()))
            for i in xrange(count):
                tmp = sub % self.m_info.get_cp_ids()[i]
                subs += tmp
        if m_id == 5:
            subs = sub % '王力宏'

        return subs

    def init_url(self, n_site=Site()):
        main_url = n_site.get_main_url()
        param_or_not = n_site.get_param_or_not()
        sub_count = n_site.get_sub_count()
        m_url = main_url
        if sub_count != 0:
            subs = self.init_subs(n_site)
            m_url += subs
        if param_or_not == 1:
            param = self.init_param()
            # debug_msg(color_msg('param=%s' % param))
            m_url += param
        # debug_msg(color_msg('url=%s' % m_url))
        n_site.m_url = m_url

    def req_url(self, n_site=Site()):
        m_id = n_site.get_id()
        name = n_site.get_name()
        main_url = n_site.get_main_url()
        param_or_not = n_site.get_param_or_not()
        sub_count = n_site.get_sub_count()
        sub = n_site.get_sub()
        m_url = n_site.get_m_url()
        debug_msg('m_id=%s\nname=%s\nmain_url=%s\nsub_count=%s,sub=%s\nparam_or_not=%s' % (
            m_id, name, main_url, sub_count, sub, param_or_not))
        debug_msg('m_url=%s' % m_url)
        try:
            m_url = urllib2.quote(m_url, safe=':\'/?&=()')
            request = urllib2.Request(m_url)
            response = urllib2.urlopen(request)
            read_str = response.read()
            # debug_msg(read_str)
            json_obj = json.loads(read_str)
            status = json_obj['status']
            msg = json_obj['msg']
            total = json_obj['total']
            m_list = json_obj['list']
            debug_msg('status=%s' % status)
            debug_msg('msg=%s' % msg)
            debug_msg('total=%s' % total)
            debug_msg('m_list=%s' % m_list)
            site.set_status(status)
            site.set_msg(msg)
            site.set_total(total)
            site.set_list(m_list)
            txt_file_name = name + '.txt'
            if m_id == 0:
                categories = list()
                for info in m_list:
                    # json_obj = json.loads(info)
                    cid = info['cid']
                    categories.append(cid)
                self.m_info.categories = sorted(categories)
                debug_msg(self.m_info.categories)
            elif m_id == 1:
                channels = list()
                for info in m_list:
                    nid = info['nid']
                    channels.append(nid)
                self.m_info.channels = sorted(channels)
                debug_msg(self.m_info.channels)
            elif m_id == 2:
                sids = list()
                for info in m_list:
                    sid = info['sid']
                    sids.append(sid)
                self.m_info.sids = sorted(sids)
                debug_msg(self.m_info.sids)
            elif m_id == 3:
                cp_ids = list()
                for info in m_list:
                    cp_song_id = info['cp_song_id']
                    cp_ids.append(cp_song_id)
                self.m_info.cp_ids = sorted(cp_ids)
                debug_msg(self.m_info.cp_ids)
            elif m_id == 4:
                cp_ids = list()
                for info in m_list:
                    cp_song_id = info['cp_song_id']
                    cp_ids.append(cp_song_id)
                self.m_info.cp_ids = sorted(cp_ids)
                debug_msg(self.m_info.cp_ids)
                # elif m_id == 5:
                #     cp_ids = list()
                #     for info in m_list:
                #         cp_song_id = info['cp_song_id']
                #         cp_ids.append(cp_song_id)
                #     self.m_info.cp_ids = sorted(cp_ids)
                #     debug_msg(self.m_info.cp_ids)
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