#!/usr/bin/python
# coding: utf8
# Filename: call_bash.py

import subprocess
from colors import red, green


def bash_process(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()
    # for line in stdout.split('\n'):
    #    print line
    if process.returncode == 0:
        return True
    else:
        return False
