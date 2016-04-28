#!/usr/bin/python
# coding: utf8
# Filename: get_patch_subdir.py


def get_patch_sub_folder():
    with open('./code/last_version', 'r') as f:
        tmp_list = []
        for line in f.readlines():
            tmp_list.append(line.strip('\n'))
    if len(tmp_list) >= 2:
        patch_sub_folder = tmp_list[-2] + "_" + tmp_list[-1]
        return patch_sub_folder
    else:
        return False