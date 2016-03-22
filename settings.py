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
                               'local_path': './code/export/', 
                               'remote_path': '/data/deploy/',
                               'patch_path': './code/patch/',
                               'release_path': '/data/release/'}
        },
        {
            'server_id': 3,
            'connect_params': {'hostname': '60.191.239.212',      # remote server's ip
                               'username': 'root',                # remote user
                               'password': 'S+VQILVLH0w/QLVQ1Wlv',              # remote password
                               'port': 22,                        # remote server ssh port
                               'local_path': './code/export/',    # local code folder
                               'remote_path': '/home/deploy/',    # remote deploy folder
                               'patch_path': './code/patch/',     # local patch folder
                               'release_path': '/home/release/'}  # remote release folder
        }
]
