#!/usr/bin/python
# Filename: get_patch_subdir.py
# coding: utf8

#!/usr/bin/python
# Filename: get_patch_subdir.py
# coding: utf8

import subprocess


def get_patch_sub_folder():
    '''get the sub folder of patch path '''
    command = "tail -n 2 ./code/last_version"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    tmp_list = []
    for line in stdout.split('\n'):
        tmp_list.append(line)
    if len(tmp_list) == 1:
        patch_sub_folder = tmp_list[0]
        return patch_sub_folder
    else:
        patch_sub_folder = tmp_list[0] + "_" + tmp_list[1]
        return patch_sub_folder

