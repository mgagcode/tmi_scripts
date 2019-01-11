#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Martin Guthrie, copyright, all rights reserved, 2018-2019

"""
from app.const import APP


def pub_notice(notice, sender, type=APP.NOTICE_NRM, on_change_only=False, replace=False):
    """
    :param notice: <string>
    :param sender: this should be a unique key of the notice sender IF
                   on_change_only, or replace is used
    :param type:  one of APP.NOTICE_*
    :param on_change_only: when set, only queue is message is updated
                           uses the sender as a key to find the previous notice
    :param replace: replace previous notice
                    uses the sender as a key to find the previous notice
    """
    pass

