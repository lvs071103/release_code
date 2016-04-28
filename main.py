#!/usr/bin/python
# coding: utf8
# Filename: display_format.py

from settings import *
from resource_release import *
from call_bash import bash_process
from display_format import *
from get_patch_subdir import *
from colors import red, green
import os
import sys
import shutil
from check import check_isexists


class Main:

    def __init__(self):
        """init"""
        self.server_info = {}

    @staticmethod
    def displayserver():
        DisplayFormat().display_line()
        DisplayFormat().head()
        DisplayFormat().display_line()
        for line in range(len(platform_list)):
            print DisplayFormat().formatstring % (
                platform_list[line]['server_id'],
                platform_list[line]['connect_params']['hostname'],
                platform_list[line]['connect_params']['local_path'],
                platform_list[line]['connect_params']['remote_path'],
                platform_list[line]['connect_params']['patch_path'],
                platform_list[line]['connect_params']['release_path'],
                platform_list[line]['connect_params']['stable_version']
            )
        DisplayFormat().display_line()

    def choiceserver(self):
        prompt = """输入上述表中服务器id: """
        while True:
            while True:
                try:
                    choice = int(raw_input(prompt))
                except (EOFError, KeyboardInterrupt):
                    break
                id_list = []
                for item in range(len(platform_list)):
                    id_list.append(platform_list[item]['server_id'])
                if choice not in id_list:
                    print red('你输入的id不存在，什么眼神... try again')
                else:
                    for item in range(len(platform_list)):
                        if platform_list[item]['server_id'] == choice:
                            self.server_info = platform_list[item]['connect_params']
                            return self.server_info

    def choicetype(self):
        prompt = """
        (A)全量更新(上传至部署目录)
        (B)差异更新(上传补丁至部署目录)
        (C)指定版本校验MD5(本地./code/export/版本目录与远程部署目录进行比对,比对后,可发布操作)
        (D)发布操作(创建软链部署目录至发布目录)
        (E)版本回退(删除现有软链,选择先以版本创建软链至发布目录)
        (F)执行命令
        (G)压缩包更新（跳过上述步骤）
        (H)解压缩（解压远程服务器压缩包）
        (Q)退出
        Enter choice: """
        while True:
            while True:
                try:
                    choice = raw_input(prompt).strip()[0].lower()
                except (EOFError, KeyboardInterrupt):
                    choice = 'q'

                print green('You picked: [%s]') % choice
                if choice not in 'abcdefgqh':
                    print red('invalid option... try again')
                else:
                    break

            if choice == 'q':
                break

            if choice == 'a':
                try:
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.display_history_version()
                    upload_version = raw_input("输入一个版本号，远程服务器将创建以这个版本号命名的目录: ")
                    self.server_info['release_version'] = upload_version
                    command = "bash svn_export_version.sh %s" % upload_version
                    bash_process(command)
                    local_upload_path = os.path.join(self.server_info['local_path'], upload_version)
                    if not check_isexists(local_upload_path):
                        print "目标不存在"
                        sys.exit()
                    ssh_handle = ReleaseCode(**self.server_info)
                    if ssh_handle.check_ssh_connect() is True:
                        print "%s 远程服务器连接成功" % self.server_info['hostname']
                    else:
                        print "%s 远程服务器连接失败" % self.server_info['hostname']
                    ssh_handle.full_upload(upload_version)
                except (KeyboardInterrupt, EOFError):
                    break

            if choice == 'b':
                try:
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.display_history_version()
                    upload_version = raw_input("输入需要增量更新的版本号: ")
                    self.server_info['release_version'] = upload_version
                    command = "bash svn_diff_version.sh"
                    bash_process(command)
                    patch_sub_folder = get_patch_sub_folder()
                    if not patch_sub_folder:
                        print red("没有取得更新补丁")
                    else:
                        ssh_handle = ReleaseCode(**self.server_info)
                        ssh_handle.check_ssh_connect()
                        ssh_handle.increment_upload(patch_sub_folder)
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'c':
                try:
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.display_history_version()
                    diff_version = raw_input("输入列出的版本号，比如v1: ")
                    self.server_info['release_version'] = diff_version
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.check_md5()
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'd' or choice == 'e':
                try:
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    link_path = os.path.join(self.server_info['release_path'],
                                             self.server_info['stable_version'])
                    if ssh_handle.islink(link_path) is False:
                        print red("当前没有发布版本")
                    else:
                        print green("当前已发布版本: %s") % ssh_handle.islink(link_path)
                    ssh_handle.display_history_version()
                    link_version = raw_input("选择上面显示版本号,用于正式发布: ")
                    self.server_info['link_version'] = link_version
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.release_symlink()
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'g':
                try:
                    zip_path = raw_input("请指定上传压缩包(比如./root/test.zip): ")
                    if not check_isexists(zip_path):
                        print u'目标不存在'
                        sys.exit()
                    package_path = os.path.abspath(zip_path)
                    self.server_info['package_name'] = os.path.basename(zip_path)
                    for item in os.listdir(self.server_info['local_path']):
                        print "本地已有版本: " + item
                    self.server_info['release_version'] = raw_input("定义压缩包上传版本: ")
                    self.server_info['zip_upload_path'] = os.path.join(self.server_info['local_path'],
                                                                       self.server_info['release_version'])
                    if not check_isexists(self.server_info['zip_upload_path']):
                        os.makedirs(self.server_info['zip_upload_path'])
                        print self.server_info['zip_upload_path'] + u'目录创建成功'
                    else:
                        print u'目录已经存在'
                    abs_package_path = os.path.join(self.server_info['zip_upload_path'],
                                                    self.server_info['package_name'])
                    if not os.path.exists(abs_package_path):
                        shutil.copy(package_path, self.server_info['zip_upload_path'])
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.full_upload(self.server_info['release_version'])
                    ssh_handle.display_packages()
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'h':
                try:
                    self.server_info['Extract_directory'] = self.server_info['release_version']
                    self.server_info['package_name'] = self.server_info['package_name']
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.extract()
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'f':
                try:
                    command = raw_input("输入要执行的命令,远程服务器将运行这条命令(比如hostname): ")
                    ssh_handle = ReleaseCode(**self.server_info)
                    ssh_handle.check_ssh_connect()
                    ssh_handle.run_command(command)
                except(KeyboardInterrupt, EOFError):
                    break

if __name__ == '__main__':
    run = Main()
    run.displayserver()
    run.choiceserver()
    run.choicetype()
