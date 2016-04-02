#!/usr/bin/python
# Filename: call_bash.py

import subprocess


class CallBash():
    def __init__(self, command):
        self.command = command

    def bash_process(self):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        for line in stdout.split('\n'):
            print line
