#!/usr/bin/python
# encoding: utf8


import os


def check_isexists(target):
    __isexists = os.path.exists(target)
    if not __isexists:
        return False
    else:
        return True
