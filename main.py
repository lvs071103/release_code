#!/usr/local/python
# coding: utf8
# Filename: display_format.py

from settings import *
from resource_release import *
from call_bash import *
from display_format import *
from get_patch_subdir import *
import sys

class main():

    def dispaly_server_list(self):
        DisplayFormat().display_line()
        DisplayFormat().head()
        DisplayFormat().display_line()
        for line in range(len(platform_list)):
            print DisplayFormat().formatstring % (
                platform_list[line]['server_id'],
                platform_list[line]['connect_params']['hostname'],
                platform_list[line]['connect_params']['username'],
                platform_list[line]['connect_params']['password'],
                platform_list[line]['connect_params']['port'],
                platform_list[line]['connect_params']['local_path'],
                platform_list[line]['connect_params']['remote_path'],
                platform_list[line]['connect_params']['patch_path'],
                platform_list[line]['connect_params']['release_path']
            )
        print DisplayFormat().display_line()

    def showmenu(self):
        prompt = """
        (A)全量更新(上传至部署目录)
        (B)差异更新(上传补丁至部署目录)
        (C)校验MD5(全目录校验(更新最新代码至本地export目录,此目录与服务器对应版本目录对比操作,不对比补丁包目录),正确无误后，方可发布操作)
        (D)发布操作(创建软链至发布目录)
        (E)版本回退(删除现有软链,选择先以版本创建软链至发布目录)
        (F)执行命令
        (Q)退出
        Enter choice: """

        while True:
            while True:
                try:
                    choice = raw_input(prompt).strip()[0].lower()
                except (EOFError, KeyboardInterrupt):
                    choice = 'q'

                print 'You picked: [%s]' % choice
                if choice not in 'abcdefq':
                    print 'invalid option... try again'
                else:
                    break

            if choice == 'q':
                break

            if choice == 'a':
                try:
                    select_id = int(raw_input("选择更进行更新的服务器: "))
                    for line in range(len(platform_list)):
                        if platform_list[line]['server_id'] == select_id:
                            server_connect_info  = platform_list[line]['connect_params']
                    release_version = raw_input("定义一个版本号或者补丁号，远程服务器将以目录的形式存在,比如输入v1,远程服务器上将创建远程地址加v1[ /home/deploy/v1 ]: ")
                    server_connect_info['release_version'] = release_version
                    command = "bash svn_export_version.sh %s" % server_connect_info['release_version']
                    CallBash(command).bash_process()
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.full_upload()    
                except (KeyboardInterrupt, EOFError):
                    break

            if choice == 'b':
                try:
                    select_id = int(raw_input("选择更进行更新的服务器: "))
                    for line in range(len(platform_list)):
                        if platform_list[line]['server_id'] == select_id:
                            server_connect_info  = platform_list[line]['connect_params']
                    release_version = raw_input("定义一个版本号或者补丁号，远程服务器将以目录的形式存在,比如输入v1,远程服务器上将创建远程地址加v1[ /home/deploy/v1 ]: ")
                    server_connect_info['release_version'] = release_version
                    command = "bash svn_diff_version.sh"
                    CallBash(command).bash_process()
                    patch_sub_folder = get_patch_sub_folder()
                    server_connect_info['patch_sub_folder'] = patch_sub_folder
                    if server_connect_info['patch_sub_folder'] == '':
                        print "没有取得更新补丁，更新将退出"
                        break
                    else:
                        ssh_handle = ReleaseCode(**server_connect_info)
                        ssh_handle.check_sshconnect()
                        ssh_handle.increment_upload()
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'c':
                try:
                    select_id = int(raw_input("选择需要校验的服务器: "))
                    for line in range(len(platform_list)):
                        if platform_list[line]['server_id'] == select_id:
                             server_connect_info  = platform_list[line]['connect_params']
                    release_version = raw_input("输入要比对的目录，比如v1[ /home/deploy/v1 ]: ")
                    server_connect_info['release_version'] = release_version
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.check_md5()
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'd':
                try:
                    select_id = int(raw_input("选择发布服务器: "))
                    for line in range(len(platform_list)):
                        if platform_list[line]['server_id'] == select_id:
                            server_connect_info  = platform_list[line]['connect_params']
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.list_last_version()
                    release_version = raw_input("输入已部署的版本号，比如v1[ /home/deploy/v1 ]: ")
                    server_connect_info['release_version'] = release_version
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.release_symlink()
                except(KeyboardInterrupt, EOFError):
                    break
           
            if choice == 'e':
                try:
                    select_id = int(raw_input("选择回滚服务器: "))
                    for line in range(len(platform_list)):
                        if platform_list[line]['server_id'] == select_id:
                            server_connect_info  = platform_list[line]['connect_params']
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.list_last_version()
                    server_connect_info['last_version'] = raw_input("选择先前的一个版本,进行回滚操作: ")
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.rollback()  
                except(KeyboardInterrupt, EOFError):
                   break

            if choice == 'f':
                try:
                    select_id = int(raw_input("选择服务器: "))
                    for line in range(len(platform_list)):
                        if platform_list[line]['server_id'] == select_id:
                            server_connect_info  = platform_list[line]['connect_params']
                    server_connect_info['command'] = raw_input("输入要执行的命令如[ /etc/init.d/php restart ]: ")
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.run_command()
                except(KeyboardInterrupt, EOFError):
                   break

if __name__ == '__main__':
    main().dispaly_server_list()
    main().showmenu()
