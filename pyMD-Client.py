#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) Client
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

import pyMD
import socket
import sys

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input('Enter player Command: ')
        s.sendto(str.encode("0:" + msg), ('localhost', 8089))
        
        data, addr = s.recvfrom(2048)
        len = int(data)
        for i in range(len):
            data, addr = s.recvfrom(2048)
            print(data)
