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
        print('------------------------')


def color_msg(msg, fg=GREEN, bg=WHITE):
    """

    @param msg:
    @param fg:
    @param bg:
    @return:
    """
    color = 0
    color_fg = None
    color_bg = None
    if fg is not None:
        color_fg = ';3%d' % fg
        # debug('color_fg=%s' % color_fg)
        color += 1
    if bg is not None:
        color_bg = ';4%dm' % bg
        # debug('color_bg=%s' % color_bg)
        color += 1
    if color > 1:
        return '%s%s%s%s%s' % (COLOR_START, color_fg, color_bg, msg, COLOR_END)
    else:
        return msg