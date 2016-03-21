#!/usr/bin/python
# Filename: display_format.py


class DisplayFormat(object):
    def __init__(self):
        self.formatstring = '%-5s %-17s %-10s %-20s %-10s %-20s %-20s %-20s %-20s'

    def display_line(self):
        print self.formatstring % ('-'*5, '-'*17, '-'*10, '-'*20, '-'*10, '-'*20, '-'*20, '-'*20, '-'*20)

    def head(self):
        print self.formatstring % ('id', 'ip', 'user', 'password', 'port',
                                   'local_path', 'remote_path', 'patch_path', 'release_path(stable)')
