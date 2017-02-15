#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) Client
# 
# $Id: $
#
# Authors: Anna-Sophia Schroeck <annasophia.schroeck at outlook.de>
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

import pyMD
import socket
import sys

if __name__ == "__main__":
    host = input("Server adress: ")
    port = input("Port: ")
    passwd = pyMD.get_hashfrompass(input("Server password: "))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input(host + ":" + port + " > ")
        msg = str(passwd) + "#" + str(msg)
        s.sendto(str.encode(msg), (host, int(port)))
        
        data, addr = s.recvfrom(2048)
        len = int(data)
        for i in range(len):
            data, addr = s.recvfrom(2048)
            print(data.decode("utf-8"))
