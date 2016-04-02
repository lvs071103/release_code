#!/usr/local/python
# coding: utf8
# Filename: display_format.py

from settings import *
from resource_release import *
from call_bash import *
from display_format import *
from get_patch_subdir import *
from colors import red, green


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
        
    def select_server(self):
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
                            server_connect_info = platform_list[item]['connect_params']
                            ssh_handle = ReleaseCode(**server_connect_info)
                            ssh_handle.check_sshconnect()
                            ssh_handle.display_last_version()
                            return server_connect_info

    def select_type(self, **kwargs):
        prompt = """
        (A)全量更新(上传至部署目录)
        (B)差异更新(上传补丁至部署目录)
        (C)指定版本校验MD5(本地./code/export/版本目录与远程部署目录进行比对,比对后,可发布操作)
        (D)发布操作(创建软链部署目录至发布目录)
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

                print green('You picked: [%s]') % choice
                if choice not in 'abcdefq':
                    print red('invalid option... try again')
                else:
                    break

            if choice == 'q':
                break

            if choice == 'a':
                try:
                    release_version = raw_input("输入一个版本号，远程服务器将创建以这个版本号命名的目录: ")
                    server_connect_info['release_version'] = release_version
                    command = "bash svn_export_version.sh %s" % release_version
                    CallBash(command).bash_process()
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.full_upload(release_version)
                except (KeyboardInterrupt, EOFError):
                    break

            if choice == 'b':
                try:
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.display_last_version()
                    release_version = raw_input("输入一个版本号，进行更新: ")
                    server_connect_info['release_version'] = release_version
                    command = "bash svn_diff_version.sh"
                    CallBash(command).bash_process()
                    patch_sub_folder = get_patch_sub_folder()
                    if patch_sub_folder == '':
                        print red("没有取得更新补丁，更新将退出")
                        break
                    else:
                        ssh_handle = ReleaseCode(**server_connect_info)
                        ssh_handle.check_sshconnect()
                        ssh_handle.increment_upload(patch_sub_folder)
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'c':
                try:
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.display_last_version()
                    release_version = raw_input("输入列出的版本号，比如v1, 本地将拉取svn最新代码,与远程版本目录进行md5对比: ")
                    server_connect_info['release_version'] = release_version
                    command = "bash svn_export_version.sh %s" % server_connect_info['release_version']
                    CallBash(command).bash_process()
                    print green("本地%s已更新") % server_connect_info['release_version']
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.check_md5()
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'd' or choice == 'e':
                try:
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    link_path = os.path.join(server_connect_info['release_path'], "stable")
                    if ssh_handle.islink(link_path) is False:
                        print red("当前没有发布版本")
                    else:
                        print green("当前已发布版本: %s") % ssh_handle.islink(link_path)
                    ssh_handle.display_last_version()
                    link_version = raw_input("输入上面显示版本号, 系统将远程部署目录/版本号与发布目录/stable建立软链接: ")
                    server_connect_info['link_version'] = link_version
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.release_symlink()
                except(KeyboardInterrupt, EOFError):
                    break

            # if choice == 'e':
            #     try:
            #         ssh_handle = ReleaseCode(**server_connect_info)
            #         ssh_handle.check_sshconnect()
            #         print green("当前发布版本: "),green(ssh_handle.islink(
            #                 os.path.join(server_connect_info['release_path'], "stable")))
            #         ssh_handle.display_last_version()
            #         server_connect_info['link_version'] = raw_input("输入上面显示的任一版本, 进行回滚操作: ")
            #         ssh_handle = ReleaseCode(**server_connect_info)
            #         ssh_handle.check_sshconnect()
            #         ssh_handle.rollback()
            #     except(KeyboardInterrupt, EOFError):
            #        break

            if choice == 'f':
                try:
                    command = raw_input("输入要执行的命令,远程服务器将运行这条命令(比如hostname): ")
                    ssh_handle = ReleaseCode(**server_connect_info)
                    ssh_handle.check_sshconnect()
                    ssh_handle.run_command(command)
                except(KeyboardInterrupt, EOFError):
                   break

if __name__ == '__main__':
    run = main()
    run.dispaly_server_list()
    server_connect_info = run.select_server()
    run.select_type(**server_connect_info)
