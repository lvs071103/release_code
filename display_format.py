#!/usr/bin/python
# coding: utf8
# Filename: display_format.py


class DisplayFormat(object):
    def __init__(self):
        self.formatstring = '%-5s %-17s %-17s %-40s %-18s %-40s %-15s'

    def display_line(self):
        print self.formatstring % ('-'*5, '-'*17, '-'*17, '-'*40, '-'*18, '-'*40, '-'*15)

    def head(self):
        print self.formatstring % ('ID', 'REMOTE_SERVER_IP', 'LOCAL_CODE_FOLDER',
                                   'REMOTE_DEPLOY_FOLDER', 'LOCAL_PATCH_FOLDER',
                                   'REMOTE_RELEASE_FOLDER', 'RELEASE_VESION')
