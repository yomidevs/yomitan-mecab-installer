#!/usr/bin/env python3

# Copyright (C) 2019 siikamiika
# Author: siikamiika
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import json
import copy
import zipfile
if sys.version_info[0] == 3:
    from urllib.request import urlretrieve
elif sys.version_info[0] == 2:
    from urllib import urlretrieve
    input = raw_input

DIR = os.path.realpath(os.path.dirname(__file__))

NAME = 'yomitan_mecab'

MANIFEST_TEMPLATE = {
    'name': 'yomitan_mecab',
    'description': 'MeCab for Yomitan',
    'type': 'stdio',
}

BROWSER_DATA = {
    'firefox': {
        'extension_id_key': 'allowed_extensions',
        'extension_ids': ['{2d13e145-294e-4ead-9bce-b4644b203a00}'],
    },
    'chrome': {
        'extension_id_key': 'allowed_origins',
        'extension_ids': ['chrome-extension://glnaenfapkkecknnmginabpmgkenenml/'],
    },
    'chromium': {
        'extension_id_key': 'allowed_origins',
        'extension_ids': ['chrome-extension://glnaenfapkkecknnmginabpmgkenenml/'],
    },
    'edge': {
        'extension_id_key': 'allowed_origins',
        'extension_ids': ['chrome-extension://glnaenfapkkecknnmginabpmgkenenml/'],
    },
}

PLATFORM_DATA = {
    'linux': {
        'platform_aliases': ['linux', 'linux2', 'riscos', 'freebsd7', 'freebsd8', 'freebsdN', 'openbsd6'],
        'manifest_install_data': {
            'firefox': {
                'methods': ['file'],
                'path': os.path.expanduser('~/.mozilla/native-messaging-hosts/'),
            },
            'chrome': {
                'methods': ['file'],
                'path': os.path.expanduser('~/.config/google-chrome/NativeMessagingHosts/'),
            },
            'chromium': {
                'methods': ['file'],
                'path': os.path.expanduser('~/.config/chromium/NativeMessagingHosts/'),
            },
        }
    },
    'windows': {
        'platform_aliases': ['win32', 'cygwin'],
        'manifest_install_data': {
            # 'firefox': {
            #     'methods': ['file', 'registry'],
            #     'path': DIR,
            #     'registry_path': 'SOFTWARE\\Mozilla\\NativeMessagingHosts\\{}'.format(NAME),
            # },
            'chrome': {
                'methods': ['file', 'registry'],
                'path': DIR,
                'registry_path': 'SOFTWARE\\Google\\Chrome\\NativeMessagingHosts\\{}'.format(NAME),
            },
            'chromium': {
                'methods': ['file', 'registry'],
                'path': DIR,
            },
            'edge': {
                'methods': ['file', 'registry'],
                'path': DIR,
                'registry_path': 'SOFTWARE\\Microsoft\\Edge\\NativeMessagingHosts\\{}'.format(NAME),
            },
        }
    },
    'mac': {
        'platform_aliases': ['darwin'],
        'manifest_install_data': {
            'firefox': {
                'methods': ['file'],
                'path': os.path.expanduser('~/Library/Application Support/Mozilla/NativeMessagingHosts/'),
            },
            'chrome': {
                'methods': ['file'],
                'path': os.path.expanduser('~/Library/Application Support/Google/Chrome/NativeMessagingHosts/'),
            },
            'chromium': {
                'methods': ['file'],
                'path': os.path.expanduser('~/Library/Application Support/Chromium/NativeMessagingHosts/'),
            },
        }
    },
}

DICTIONARY_DATA = {
    'ipadic': {
        'url': 'https://github.com/siikamiika/yomichan-mecab-installer/releases/download/ipadic-1/ipadic.zip',
        'compression': 'zip',
        'size': '51M',
        'description': 'A basic dictionary',
    },
    'unidic-mecab-translate': {
        'url': 'https://github.com/siikamiika/unidic-mecab-translate/releases/download/1.2/unidic-mecab-translate-1.2.zip',
        'compression': 'zip',
        'size': '191M',
        'description': 'A dictionary that prefers shorter words to longer ones, is usually more accurate, and shows pronunciation instead of reading',
    }
}

def platform_data_get():
    for platform_name in PLATFORM_DATA:
        data = copy.deepcopy(PLATFORM_DATA[platform_name])
        data['platform'] = platform_name
        if sys.platform in data['platform_aliases']:
            return data
    raise Exception('Unsupported platform: {}'.format(sys.platform))

def manifest_get(browser, messaging_host_path, additional_ids=[]):
    manifest = copy.deepcopy(MANIFEST_TEMPLATE)
    data = BROWSER_DATA[browser]
    manifest['path'] = messaging_host_path
    manifest[data['extension_id_key']] = []
    for extension_id in data['extension_ids'] + additional_ids:
        manifest[data['extension_id_key']].append(extension_id)
    return json.dumps(manifest, indent=4)

def manifest_install_file(manifest, path):
    try: os.makedirs(path)
    except: pass
    with open(os.path.join(path, NAME + '.json'), 'w') as f:
        f.write(manifest)

def download_dict(url, compression):
    print('Downloading...')
    try: os.makedirs('data')
    except: pass
    tmp_path, _ = urlretrieve(url)
    if compression == 'zip':
        extract_zip(tmp_path, 'data')
    print('Done!')

def extract_zip(zip_path, extract_path):
    print('Extracting...')
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_path)


def main():
    platform_data = platform_data_get()

    # choose browser
    browsers = list(platform_data['manifest_install_data'].keys())
    for i, browser in enumerate(browsers):
        print('{}: {}'.format(i + 1, browser))
    browser = browsers[int(input('Choose browser: ')) - 1]

    # generate manifest
    print('')
    print('Using default Yomitan extension ID for {}.'.format(browser))
    print('Add more extension IDs, or press enter to continue')
    additional_extension_ids = []
    while True:
        extension_id = input('Extension ID: ')
        if not extension_id:
            break
        additional_extension_ids.append(extension_id)
    script_path = os.path.join(DIR, 'mecab.py')
    if platform_data['platform'] == 'windows':
        bat_path = os.path.join(DIR, 'mecab_yomitan.bat')
        with open(bat_path, 'w') as f:
            f.write('@echo off\n"{}" -u "{}"'.format(
                sys.executable,
                script_path
            ))
        script_path = bat_path
    manifest = manifest_get(browser, script_path, additional_extension_ids)
    manifest_install_data = platform_data['manifest_install_data'][browser]
    for method in manifest_install_data['methods']:
        if method == 'file':
            manifest_install_file(manifest, manifest_install_data['path'])
        if method == 'registry':
            if sys.version_info[0] == 3:
                import winreg
            elif sys.version_info[0] == 2:
                import _winreg as winreg
            winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                             manifest_install_data['registry_path'])
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                          manifest_install_data['registry_path'],
                                          0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, '', 0, winreg.REG_SZ,
                              os.path.join(manifest_install_data['path'], NAME + '.json'))
            winreg.CloseKey(registry_key)

    # install dictionaries
    print('')
    if input('Install a MeCab dictionary? (Y/n): ').lower() in ['', 'y']:
        mecab_dictionaries = list(DICTIONARY_DATA)
        for i, dict_name in enumerate(mecab_dictionaries):
            dict_data = DICTIONARY_DATA[dict_name]
            print('{}: {} [{}] - {}'.format(i + 1, dict_name, dict_data['size'], dict_data['description']))
        dictionary = mecab_dictionaries[int(input('Choose dictionary: ')) - 1]
        dictionary_data = DICTIONARY_DATA[dictionary]
        download_dict(dictionary_data['url'], 'zip')


if __name__ == '__main__':
    main()
