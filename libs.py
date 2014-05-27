#!/usr/local/bin/python -u
# -*- coding: utf-8 -*-
__author__ = 'jiahuixing'

COLOR_START = '\033[0'
COLOR_END = '\033[0m'
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

DEBUG = 1


def debug_msg(msg, flag=DEBUG):
    if flag == 1:
        print('------------------------')
        print(msg)


def color_msg(msg, fg=GREEN, bg=None):
    color = list()
    if fg is not None:
        color_fg = '3%d' % fg
        color.append(color_fg)
    if bg is not None:
        color_bg = '4%d' % bg
        color.append(color_bg)
    if len(color) > 0:
        color_str = ';'.join(color)
        msg = '%s%sm%s%s' % (COLOR_START, color_str, msg, COLOR_END)
    return msg