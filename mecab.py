#!/usr/bin/python3 -u

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

from __future__ import print_function

import json
import sys
import os
import platform
import re
import shutil
import struct
import subprocess
import threading
if sys.version_info[0] == 3:
    import queue
    from itertools import zip_longest
elif sys.version_info[0] == 2:
    import Queue as queue
    from itertools import izip_longest as zip_longest

DIR = os.path.realpath(os.path.dirname(__file__))


def read_stdin(length):
    if sys.version_info[0] == 3:
        return sys.stdin.buffer.read(length)
    elif sys.version_info[0] == 2:
        return sys.stdin.read(length)

def write_stdout(data):
    if sys.version_info[0] == 3:
        return sys.stdout.buffer.write(data)
    elif sys.version_info[0] == 2:
        return sys.stdout.write(data)

def flush_stdout():
    if sys.version_info[0] == 3:
        sys.stdout.buffer.flush()
    elif sys.version_info[0] == 2:
        sys.stdout.flush()


def get_message():
    raw_length = read_stdin(4)
    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('@I', raw_length)[0]
    message = read_stdin(message_length).decode('utf-8')
    return json.loads(message)


def send_message(message_content):
    encoded_content = json.dumps(message_content).encode('utf-8')
    encoded_length = struct.pack('@I', len(encoded_content))
    write_stdout(encoded_length)
    write_stdout(encoded_content)
    flush_stdout()


class Mecab:
    dictionaries = {
        'ipadic': ['pos', 'pos2', '_', '_', '_', '_', 'expression', 'reading', 'pron'],
        'ipadic-neologd': ['pos', 'pos2', '_', '_', '_', '_', 'expression', 'reading', 'pron'],
        'unidic-mecab-translate': [
            'pos', 'pos2', 'pos3', 'pos4', 'inflection_type', 'inflection_form',
            'lemma_reading', 'lemma', 'expression', 'reading', 'expression_base', 'reading_base'
        ],
    }
    skip_patt = u'[\s\u30fb]'

    def __init__(self, dictionary_name):
        self.dictionary_name = dictionary_name
        self.dictionary = Mecab.dictionaries[dictionary_name]
        args = [self.get_executable_path(), '-d', os.path.join(DIR, 'data', dictionary_name), '-r', os.path.join(DIR, 'mecabrc')]
        self.process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            bufsize=1
        )
        self.process_output_queue = queue.Queue()

        self.stdout_thread = threading.Thread(target=self.bg_handle_stdout)
        self.stdout_thread.daemon = True
        self.stdout_thread.start()

    def get_executable_path(self):
        if os.name == 'nt':
            return self.get_nt_executable_path()
        if sys.platform == 'darwin': # macOS
            return self.get_darwin_executable_path()
        return 'mecab'

    def get_nt_executable_path(self):
        # look up from registry
        if sys.version_info[0] == 3:
            import winreg
        elif sys.version_info[0] == 2:
            import _winreg as winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\\MeCab', 0, winreg.KEY_READ)
            path, _ = winreg.QueryValueEx(reg_key, 'mecabrc')
            for _ in range(2):
                path = os.path.dirname(path)
            path = os.path.join(path, 'bin', 'mecab.exe')
            if os.path.isfile(path):
                return path
        except OSError:
            pass
        # look up from program files
        path = os.path.join(os.getenv("programfiles(x86)"), 'MeCab', 'bin', 'mecab.exe')
        if os.path.isfile(path):
            return path
        # assume it exists in %PATH%
        return 'mecab.exe'

    def get_darwin_executable_path(self):
        # check %PATH%
        if shutil.which('mecab') != None:
            return 'mecab'
        # assume mecab is installed via Homebrew
        if platform.processor() == 'arm':
            # use default Apple Silicon path
            return '/opt/homebrew/bin/mecab'
        # use default macOS Intel path
        return '/usr/local/bin/mecab'

    def parse(self, text):
        parsed_lines = []
        for text_line in text.splitlines():
            parsed_line = []
            for text_line_part in re.findall(u'{0}|.*?(?={0})|.*'.format(Mecab.skip_patt), text_line):
                if re.match(Mecab.skip_patt, text_line_part):
                    parsed_line.append(self.gen_dummy_output(text_line_part))
                    continue
                self.process.stdin.write((text_line_part + '\n').encode('utf-8'))
                self.process.stdin.flush()
                for output_part in iter(self.process_output_queue.get, 'EOS'):
                    parsed_part = {}
                    try:
                        parsed_part['source'], output_part_info = output_part.split('\t', 1)
                        output_part_info_parsed = [None if i == '*'
                                                   else re.sub(Mecab.skip_patt, '', i.split('-')[0])
                                                   for i in output_part_info.split(',')]
                        parsed_part.update(zip_longest(self.dictionary, output_part_info_parsed))
                        parsed_line.append(parsed_part)
                    except Exception as e:
                        print(e, file=sys.stderr)
            parsed_lines.append(parsed_line)
        return parsed_lines

    def gen_dummy_output(self, text):
        output = {'source': text}
        for key in self.dictionary:
            if key not in output:
                output[key] = None
        return output

    def bg_handle_stdout(self):
        for line in iter(self.process.stdout.readline, b''):
            self.process_output_queue.put(line.decode('utf-8').strip())
        self.process.stdout.close()


class MecabOrchestrator:
    def __init__(self):
        self.mecabs = {}
        self.start_mecabs()

    def parse(self, text, dictionaries=None, retry=True):
        try:
            output = {}
            if not dictionaries:
                for mecab_name in self.mecabs:
                    output[mecab_name] = self.mecabs[mecab_name].parse(text)
            else:
                for dictionary_name in dictionaries:
                    output[dictionary_name] = self.mecabs[dictionary_name].parse(text)
            return output
        except Exception as e:
            print(e, file=sys.stderr)
            if retry:
                self.reload_mecabs()
                self.parse(text, dictionaries, False)

    def reload_mecabs(self):
        self.stop_mecabs()
        self.start_mecabs()

    def stop_mecabs(self):
        for mecab_name in list(self.mecabs):
            mecab = self.mecabs[mecab_name]
            mecab.process.kill()
            del self.mecabs[mecab_name]

    def start_mecabs(self):
        for dictionary_name in Mecab.dictionaries:
            if os.path.isdir(os.path.join(DIR, 'data', dictionary_name)):
                self.mecabs[dictionary_name] = Mecab(dictionary_name)


def main():
    mecabs = MecabOrchestrator()
    while True:
        msg = get_message()
        if msg['action'] == 'get_version':
            send_message({
                'sequence': msg['sequence'],
                'data': {'version': 1},
            })
        elif msg['action'] == 'parse_text':
            text = msg['params']['text']
            dictionaries = msg['params'].get('dictionaries')
            response = mecabs.parse(text, dictionaries)
            send_message({
                'sequence': msg['sequence'],
                'data': response,
            })

if __name__ == '__main__':
    main()
