#!/usr/bin/python
# coding: utf8
# Filename: resource_release.py

import sys
import paramiko
import os
import traceback
import hashlib
from colors import red, green, yellow


class ReleaseCode:
    def __init__(self, **server_info):
        self.server_info = server_info
        self.connection = paramiko.SSHClient()

    def check_ssh_connect(self):
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.connection.connect(self.server_info['hostname'],
                                    username=self.server_info['username'],
                                    password=self.server_info['password'],
                                    port=self.server_info['port'])
            return True
        except paramiko.SSHException:
            print red("Connection Failed.")
            quit()

    def run_command(self, command):
        stdin, stdout, stderr = self.connection.exec_command(command)
        for line in stdout.readlines():
            print green(line.strip())
        self.connection.close()

    def display_packages(self):
        try:
            package_path = os.path.join(self.server_info['remote_path'], self.server_info['release_version'])
            sftp = self.connection.open_sftp()
            try:
                dirlist = sftp.listdir(package_path)
                for item in dirlist:
                    print "%s include: %s" % (package_path, item)
            except IOError:
                print red("%s not exists.")
                
            sftp.close()

        except EOFError:
            print red("open sftp failed.")

    def extract(self):
        extract_folder = os.path.join(self.server_info['remote_path'],
                                      self.server_info['Extract_directory'])
        command = "cd %s && unzip -o %s" % (extract_folder, self.server_info['package_name'])
        stdin, stdout, stderr = self.connection.exec_command(command)
        for line in stdout.readlines():
            print green(line)
        self.connection.close()

    def _uploads_with(self, top_path):
        """sftp uploads"""
        def internal_uploads(*args):
            try:
                sftp = self.connection.open_sftp()
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
                            print yellow("assume %s create success or target folder exists.") % dir_path
                        try:
                            sftp.mkdir("%s/%s" % (dir_path, base_name))
                        except IOError:
                            print yellow("assume %s/%s create sucess or folder already exists.") % \
                                  (dir_path, base_name)
                    for filename in filenames:
                        if sftp.put(os.path.join(dirpath, filename), os.path.join(remote_path, filename)):
                            print "Upload %s to %s %s " % \
                                  (filename, self.server_info['hostname'],
                                   remote_path), green("success")
                        else:
                            print "Upload %s to %s %s " % \
                                  (filename, self.server_info['hostname'],
                                   remote_path), red("failed")
                sftp.close()

            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
                # try:
                #     sftp.close()
                # except:
                #     pass
                sys.exit(1)
            print green("%s upload success" % top_path)
        return internal_uploads(self)

    def increment_upload(self, val):
        top_path = os.path.join(self.server_info['patch_path'], val)
        return self._uploads_with(top_path)

    def full_upload(self, val):
        top_path = os.path.join(self.server_info['local_path'], val)
        return self._uploads_with(top_path)

    def islink(self, path):
        try:
            sftp = self.connection.open_sftp()
            try:
                return sftp.readlink(path)
            except IOError:
                return False
            sftp.close()
        except EOFError:
            print red("open sftp failed.")

    def unlink(self, link_target):
        try:
            sftp = self.connection.open_sftp()
            try:
                sftp.unlink(link_target)
                print green("unlink success")
            except IOError:
                print red("assume path is a folder(directory).")

        except EOFError:
            print red("open sftp failed.")

    def _symlink(self, link_target):
        link_src = os.path.join(self.server_info['remote_path'], self.server_info['link_version'])

        def internal_symlink(*args):
            try:
                sftp = self.connection.open_sftp()
                if sftp:
                    print green("open sftp success")
                    try:
                        sftp.listdir(self.server_info['release_path'])
                    except IOError:
                        sftp.mkdir(self.server_info['release_path'])
                        print green("%s create success.") % self.server_info['release_path']

                sftp.symlink(link_src, link_target)
                print green("create symlink success.")

                sftp.close()

            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
                # try:
                #     sftp.close()
                # except:
                #     pass
                sys.exit(1)
            print green("%s %s symlink success") % (link_src, link_target)

        return internal_symlink(self)

    def release_symlink(self):
        release_version = self.server_info['stable_version']
        link_target = os.path.join(self.server_info['release_path'], release_version)
        if self.islink(link_target):
            self.unlink(link_target)
            self._symlink(link_target)
        else:
            return self._symlink(link_target)

    def display_history_version(self):
        try:
            sftp = self.connection.open_sftp()
            try:
                dirlist = sftp.listdir(self.server_info['remote_path'])
                for item in dirlist:
                    print "远程服务器已部署版本: ", green(item)
            except IOError:
                print yellow("assume %s folder is not exists. Please upload first") \
                      % self.server_info['remote_path']

        except Exception as e:
            print ('*** caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            # try:
            #     sftp.close()
            # except:
            #     pass
            sys.exit(1)

    def check_md5(self):
        global rmd5sum

        def md5_checksum(file_path):
            with open(file_path, 'rb') as fh:
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
            ok_number = 0
            file_number = 0
            for (dirname, subdir, subfile) in os.walk(local_path):
                remote_path = os.path.join(self.server_info['remote_path'],
                                           self.server_info['release_version'],
                                           dirname[len(local_path)+1:])
                for fname in subfile:
                    file_abs_path = (os.path.join(dirname, fname))
                    lmd5sum = md5_checksum(file_abs_path)
                    file_number += 1
                    remote_file_abs_path = (os.path.join(remote_path, fname))
                    try:
                        command = "md5sum %s | awk '{print $1}'" % remote_file_abs_path
                        stdin, stdout, stderr = self.connection.exec_command(command)
                        for line in stdout.readlines():
                            rmd5sum = line.strip('\n')
                        if lmd5sum != rmd5sum:
                            print red("%s md5sum check failed.") % fname
                        else:
                            ok_number += 1
                    except Exception:
                        print red("%s is not exsits.") % fname
            print green("The File number is %d  md5sum check %d is OK") % (file_number, ok_number)

            sftp.close()

        except Exception as e:
            print ('*** caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            # try:
            #     sftp.close()
            # except:
            #     pass
            sys.exit(1)
