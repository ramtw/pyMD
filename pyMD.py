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
import random
import binascii

ERR_PASSWD = "__err_passwd__"
INF_SERDOWN = "__info_serverdown__"

CL_HELLO = "__client_hello__"
CL_EXIT = "__client_bye__"

VERSION = '0.91.5 AES'
CODENAME = 'Pockenberg'
AUTHOR = 'Anna-Sophia Schroeck <pba3h11aso@t-online.de>'
PYMDString = 'pyMD ' + VERSION + ' ' + CODENAME

def get_hashfrompass(passwd):
    salt = str(random.getrandbits(128))
    dk = hashlib.sha256(str.encode(passwd + salt)).digest()
    return dk


def byteToHex(byteHash):
    return binascii.hexlify(byteHash).decode("utf-8")
def hexToByte(hexHash):
    return binascii.unhexlify(str.encode(hexHash))

def get_config_path(file):
    if sys.platform.startswith('linux'):
        return "/etc/" + file
    elif sys.platform.startswith('win'):
        return file
    elif sys.platform.startswith('darwin'):
        return "/etc/" + file

def get_log_path():
    if sys.platform.startswith('linux'):
        return "/var/log/pymd.log"
    elif sys.platform.startswith('win'):
        return "pymd.log"
    elif sys.platform.startswith('darwin'):
        return "/var/log/pymd.log"
class client_config:
    def __init__(self):
        self.m_path = get_config_path("pyMDClient.ini")
        self.m_config = configparser.ConfigParser()
        if os.path.isfile(self.m_path) == True :
            self.m_config.read(self.m_path)
        else:
            print("[Client First run] Create config")
            
            host = input("Host: ")
            port = input("Port: ")
            has = input("hash: ")
            self.m_config['client'] = {'hash': has,
                                       'port': port,
                                       'addr': host }
            self.save()
            self.m_config.read(self.m_path)

    def save(self):
        with open(self.m_path, 'w') as configfile:
            self.m_config.write(configfile)
    def get_server_port(self):
        return int(self.m_config['client']['port'])
    def get_server_addr(self):
        return self.m_config['client']['addr']
    def get_server_hash(self):
        hexhash = self.m_config['client']['hash']
        return hexToByte(hexhash)
      
        
class server_config: 
    def __init__(self):
        self.m_path = get_config_path("pyMDServer.ini")
        self.m_config = configparser.ConfigParser()
        if os.path.isfile(self.m_path) == True :
            self.m_config.read(self.m_path)
        else:
            print("[First run] Create config")
            
            passwd = input("Please enter the server password: ")
            temp = get_hashfrompass(passwd)
            
            self.m_config['music'] = {'path': 'data',
                                      'volume': '80',
                                      'soundcard': '0'}
            self.m_config['server'] = {'hash': byteToHex(temp),
                                       'port': '8089',
                                       'bind': 'localhost',
                                       'loggingLevel': '0',
                                       'loggingFile': get_log_path() }

            
            self.save()
            self.m_config.read(self.m_path)


            
    def get_music_path(self):
        return self.m_config['music']['path']
    def get_music_volume(self):
        return int(self.m_config['music']['volume'])
    def get_server_hash(self):
        hexhash =  self.m_config['server']['hash']
        return hexToByte(hexhash)
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
        self.m_config['server']['hash'] = get_hashfrompass(passwd)
    def set_server_port(self, port):
        self.m_config['server']['port'] = port
    def save(self):
        with open(self.m_path, 'w') as configfile:
            self.m_config.write(configfile)
