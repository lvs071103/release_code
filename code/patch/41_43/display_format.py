#!/usr/bin/python
# coding: utf8
# Filename: display_format.py


class DisplayFormat(object):
    def __init__(self):
        self.formatstring = '%-5s %-17s %-10s %-20s %-10s %-20s %-20s %-20s %-20s'

    def display_line(self):
        print self.formatstring % ('-'*5, '-'*17, '-'*10, '-'*20, '-'*10, '-'*20, '-'*20, '-'*20, '-'*20)

    def head(self):
        print self.formatstring % ('ID', 'REMOTE_SERVER_IP', 'USER', 'PASSWORD', 'SSH_PORT',
                                   'LOCAL_CODE_FOLDER', 'REMOTE_DEPLOY_FOLDER', 'LOCAL_PATCH_FOLDER', 'REMOTE_RELEASE_FOLDER')
