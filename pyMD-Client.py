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
import signal

def recive(s):
    data, addr = s.recvfrom(2048)
    len = int(data)
    for i in range(len):
        data, addr = s.recvfrom(2048)
        msg = data.decode("utf-8")
        if pyMD.ERR_PASSWD in msg:
            print("Wrong password bye bye ....")
            sys.exit(1)
        else:
            print(msg)
def send(s, msg):
    msg = str(passwd) + "#" + str(msg)
    s.sendto(str.encode(msg), (host, int(port)))
    recive(s)
def exit(s, c):
    try:
        if input("Really quit? (y/n)> ").lower().startswith('y'):         
            sys.exit(c)
    except KeyboardInterrupt:   
        sys.exit(c)
    
def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    signal.signal(signal.SIGINT, original_sigint)

    exit(s, 1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)
        
if __name__ == "__main__":
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    
    host = input("Server adress: ")
    port = input("Port: ")
    passwd = pyMD.get_hashfrompass(input("Server password: "))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send(s, pyMD.CL_HELLO)
        while True:
            msg = input(host + ":" + port + " > ")
            if 'exit' in msg:
                exit(s, 0)
            else:
                send(s, msg)
    except:
        print("Conection error")
