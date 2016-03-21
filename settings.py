#!/usr/bin/python
# Filename: settings.py

platform_list = [
        {
            'server_id': 1,
            'connect_params': {'hostname': '192.168.1.215',
                               'username': 'root',
                               'password': '?root?',
                               'port': 22,
                               'local_path': './code/export/',
                               'remote_path': '/home/deploy/',
                               'patch_path': './code/patch/',
                               'release_path': '/home/release/'}
        },
        {
            'server_id': 2,
            'connect_params': {'hostname': '10.16.1.150',
                               'username': 'root',
                               'password': '?root?',
                               'port': 22,
                               'local_path': './code/export/',   # full update code store local path
                               'remote_path': '/data/deploy/',
                               'patch_path': './code/patch/',
                               'release_path': '/data/release/'}
        },
        {
            'server_id': 3,
            'connect_params': {'hostname': '60.191.239.212',
                               'username': 'root',
                               'password': '?root?',
                               'port': 22,
                               'local_path': './code/export/',    # full update code store local path
                               'remote_path': '/home/deploy/',    # remote server deploy path
                               'patch_path': './code/patch/',     # patch store local path
                               'release_path': '/home/release/'}  # remote server release path
        }
]
