#!/usr/bin/python
# Filename: settings.py

svn_url = {'url': "https://", 'username': '', 'password': ''}
git_url = {'url': 'https://', 'username': '', 'password': ''}


platform_list = [
        {
            'server_id': 1,
            'connect_params': {'hostname': '60.191.239.212',      # remote server's ip
                               'username': 'root',                # remote user
                               'password': '?root?',              # remote password
                               'port': 22,                        # remote server ssh port
                               'local_path': './code/export',     # local code folder
                               'remote_path': '/data/deploy/',    # remote deploy folder
                               'patch_path': './code/patch/',     # local patch folder
                               'release_path': '/data/release/',  # remote release folder
                               'stable_version': 'android'}
        }
]
