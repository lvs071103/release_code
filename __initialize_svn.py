#!/usr/bin/python
# coding:utf8

import os
from settings import svn_info
from check import check_isexists
from call_bash import bash_process


def initialize():
    if not check_isexists(svn_info['co_folder']):
        os.makedirs(svn_info['co_folder'])
        print u"%s 创建成功" % svn_info['co_folder']
    else:
        print u"目标已存在"
    command = "svn checkout --username=%s --password=%s %s %s" % (svn_info['username'],
                                                                  svn_info['password'],
                                                                  svn_info['url'],
                                                                  svn_info['co_folder'])
    if bash_process(command):
        print u"本地checkout成功"
    else:
        print u"本地checkout失败"
