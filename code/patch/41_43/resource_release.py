#!/usr/bin/python
# coding: utf8
# Filename: resource_release.py

import sys
import paramiko
import os
import traceback
import hashlib
from colors import red, green


class ReleaseCode():

    def __init__(self, **server_info):
        self.server_info = server_info

    def check_sshconnect(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.connection.connect(self.server_info['hostname'],
                                    username=self.server_info['username'],
                                    password=self.server_info['password'],
                                    port=self.server_info['port'])
        except paramiko.SSHException:
            print red("Connection Failed.")
            quit()
        return True

    def run_command(self):
        stdin, stdout, stderr = self.connection.exec_command(self.server_info['command'])
        for line in stdout.readlines():
            print green(line.strip())
        self.connection.close

    def _uploads_with(self, val):

        def inner(val):
            try:
                sftp = self.connection.open_sftp()
                top_path = os.path.join(self.server_info['patch_path'], val)
                for dirpath, dirname, filenames in os.walk(top_path):
                    remote_path = os.path.join(self.server_info['remote_path'],
                                               self.server_info['release_version'],
                                               dirpath[len(top_path)+1:])
                    try:
                        sftp.listdir(remote_path)     # Test if remote folder exists
                    except IOError:
                        dir_path, base_name = os.path.split(remote_path.rstrip('/'))
                        try:
                            sftp.mkdir(dir_path)     # Create remote folder
                        except IOError:
                            print red("assume %s create success or target folder exists.") % dir_path
                        try:
                            sftp.mkdir("%s/%s" % (dir_path, base_name))
                        except IOError:
                            print red("assume %s/%s create sucess or folder already exists.") % (dir_path, base_name)
                    for filename in filenames:
                        sftp.put(os.path.join(dirpath, filename), os.path.join(remote_path, filename))
                        print "Upload %s to %s %s success." % (filename, self.server_info['hostname'], remote_path)

            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
                try:
                    sftp.close()
                except:
                    pass
                sys.exit(1)
            return green("update success")
        return inner

    def increment_upload(self, val):
        increment_upload = self._uploads_with(val)
        return increment_upload

    def full_upload(self, val):
        full_upload = self._uploads_with(val)
        return full_upload

    def release_symlink(self):
        release_version = "stable"
        symlink = os.path.join(self.server_info['release_path'], release_version)
        self.connection.exec_command("test -L %s && rm -rf %s" % (symlink, symlink))
        try:
            sftp = self.connection.open_sftp()
            try:
                sftp.listdir(self.server_info['release_path'])
            except IOError:
                sftp.mkdir(self.server_info['release_path'])
                print "%s create success." % self.server_info['release_path']
            link_target = os.path.join(self.server_info['release_path'], release_version)
            link = os.path.join(self.server_info['remote_path'],
                                self.server_info['release_version'])
            sftp.symlink(link, link_target)
            print "create symlink success."

            sftp.close()
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                sftp.close()
            except:
                pass
            sys.exit(1)

    def display_last_version(self):
        try:
            sftp = self.connection.open_sftp()
            try:
                dirlist = sftp.listdir(self.server_info['remote_path'])
                for item in dirlist:
                    print green("线上已有版本: "), green(item)
            except IOError:
                print "assume %s folder is not exists. Please upload first" \
                      % self.server_info['remote_path']

        except Exception as e:
            print ('*** caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                sftp.close()
            except:
                pass
            sys.exit(1)

    def rollback(self):
        try:
            sftp = self.connection.open_sftp()
            release_version = "stable"
            symlink = os.path.join(self.server_info['release_path'], release_version)
            self.connection.exec_command("test -L %s && rm -rf %s" % (symlink, symlink))
            print "delete old symlink success."
            link = os.path.join(self.server_info['remote_path'],
                                self.server_info['last_version'])
            try:
                sftp.listdir(self.server_info['release_path'])
            except IOError:
                sftp.mkdir(self.server_info['release_path'])
                print "%s create success." % self.server_info['release_path']
            sftp.symlink(link, symlink)
            print "version rollback %s success." % (self.server_info['last_version'])

        except Exception as e:
            print ('*** caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                sftp.close()
            except:
                pass
            sys.exit(1)

    def check_md5(self):
        def md5Checksum(filePath):
            with open(filePath, 'rb') as fh:
                m = hashlib.md5()
                while True:
                    data = fh.read(8192)
                    if not data:
                        break
                    m.update(data)
                return m.hexdigest()
        try:
            sftp = self.connection.open_sftp()
            local_path = os.path.join(self.server_info['local_path'],
                                      self.server_info['release_version'])
            number = 0
            for (dirname,subdir, subfile) in os.walk(local_path):
                remote_path = os.path.join(self.server_info['remote_path'],
                                           self.server_info['release_version'],
                                           dirname[len(local_path)+1:])
                for fname in subfile:
                    file_abs_path = (os.path.join(dirname, fname))
                    lmd5sum = md5Checksum(file_abs_path)
                    rfile_abs_path = (os.path.join(remote_path, fname))
                    try:
                        command = "md5sum %s | awk '{print $1}'" % rfile_abs_path
                        stdin, stdout, stderr = self.connection.exec_command(command)
                        for line in stdout.readlines():
                            rmd5sum = line.strip()
                        if lmd5sum != rmd5sum:
                            print red("%s md5sum check failed.") % fname
                        else:
                            number += 1
                    except Exception:
                        print red("%s is not exsits.") % fname
            print green("The number of md5sum check is OK: %d") % number

            sftp.close()

        except Exception as e:
            print ('*** caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                sftp.close()
            except:
                pass
            sys.exit(1)
