#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) Common File
# 
# $Id: $
#
# Authors: Anna-Sophia Schroeck <annasophia.schroeck at outlook.de>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301 USA
import os
import sys
import hashlib
import configparser

def get_hashfrompass(passwd):
    return hashlib.sha256(str.encode(passwd)).hexdigest()

def get_config_path():
    if sys.platform.startswith('linux'):
        return "/etc/pymd.ini"
    elif sys.platform.startswith('win'):
        return "pymd.ini"
    elif sys.platform.startswith('darwin'):
        return "/etc/pymd.ini"
class config: 
    def __init__(self):
        self.m_path = get_config_path()
        self.m_config = configparser.ConfigParser()
        if os.path.isfile(self.m_path) == True :
            self.m_config.read(self.m_path)
        else:
            print("config not found: create std config - please restart!")
            self.m_config['music'] = {'path': 'data',
                                      'volume': '80',
                                      'soundcard': '0'}
            self.m_config['server'] = {'pass': get_hashfrompass("admin"),
                                       'port': '8089',
                                       'bind': 'localhost',
                                       'loggingLevel': '0',
                                       'loggingFile': '/var/log/pyMD'}
            self.save()
            sys.exit(-1)
            
    def get_music_path(self):
        return self.m_config['music']['path']
    def get_music_volume(self):
        return int(self.m_config['music']['volume'])
    def get_server_pass(self):
        return self.m_config['server']['pass']
    def get_server_port(self):
        return int(self.m_config['server']['port'])
    def get_server_addr(self):
        return self.m_config['server']['bind']
    def get_server_loggingLevel(self):
        return int(self.m_config['server']['loggingLevel'])
    def get_server_loggingFile(self):
        return self.m_config['server']['loggingFile'] 

    def set_music_path(self, path):
        self.m_config['music']['path'] = path
    def set_music_volume(self, volume):
        self.m_config['music']['volume'] = volume
    def set_server_pass(self, passwd):
        self.m_config['server']['pass'] = get_hashfrompass(passwd)
    def set_server_port(self, port):
        self.m_config['server']['port'] = port
    def save(self):
        with open(self.m_path, 'w') as configfile:
            self.m_config.write(configfile)
