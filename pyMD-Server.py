#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) Server
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

__author__ = "annas"
__date__ = "$05.02.2017 04:39:03$"


import vlc
import os
import sys
import hashlib
import socket
import pyMD
from enum import Enum

if __name__ == "__main__":
    def end_callback(event, vlcplayer):
        vlcplayer.setend()
    def pos_callback(event, vlcplayer):
        vlcplayer.m_playerpos = vlcplayer.get_vlc().get_position() 


    VERSION =  '0.8.23' 
    CODENAME = 'Desenberg'
    AUTHOR = 'Anna-Sophia Schroeck <pba3h11aso@t-online.de>'
    PYMDString = "pyMD " + VERSION + ' ' + CODENAME 
    
    
    class status(Enum):
        INIT = 1
        LOAD = 2
        PLAY = 3
        PAUSED = 4
        STOP = 5
                
    
    class vlcplayer:
        MusicList = []
        
        def __init__(self,config):
            print("Start vlc system")
            self.m_data = config.get_music_path()
            self.m_playerpos = 0
            self.m_vlc = vlc.Instance("--no-xlib")
            self.m_player =  self.m_vlc.media_player_new()
            self.event_manager =self.m_player.event_manager()
            self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, end_callback, self)
            self.event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, pos_callback, self)
            self.m_player.audio_set_volume(config.get_music_volume())
            self.m_status = status.INIT
            print("Create music list")
            vlcplayer.MusicList = [f for f in os.listdir(self.m_data) if os.path.isfile(os.path.join(self.m_data, f))]
        def setfile(self,name):
            file = os.path.join(self.m_data,name) 
            Media =  self.m_vlc.media_new(str(file))
            self.m_player.set_media(Media)
            self.m_status = status.LOAD
            return "load file: " + file
        def stream(self, file):
            Media =  self.m_vlc.media_new(str(file))
            self.m_player.set_media(Media)
            self.m_status = status.LOAD
            return ""
        def play(self):
            self.m_player.play()
            self.m_status = status.PLAY
            return "play file"
        def get_vlc(self):
            return self.m_player
        def get_status(self):
            return self.m_status
        def list_music(self):
            for title in vlcplayer.MusicList:
                print( title)
        def setend(self):
            self.m_status = status.STOP
            
    

    class pymusic:
        def __init__(self):
            self.m_cfg = pyMD.config()
            self.m_player = vlcplayer(self.m_cfg)
            self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.m_socket.bind((self.m_cfg.get_server_addr(),
                                self.m_cfg.get_server_port()))
        def start(self):
           
            print ("Listening on %s:%d..." % ("localhost",
                       self.m_cfg.get_server_port()))
            while True:
                try:
                    data, addr = self.m_socket.recvfrom(2048)
                    args = data.decode("utf-8").split("#") 
                
                    #pass#com#argument
                    if args[0] in self.m_cfg.get_server_pass():
                        if "load" in args[1]:
                            self.load(args[2], addr)
                        elif "stream" in args[1]:
                            self.stream(args[2], addr)
                        elif 'play' in args[1]:
                            self.play(addr)
                        elif 'getdb' in args[1]:
                            i = len(vlcplayer.MusicList)
                            self.sendinfos(addr, i, vlcplayer.MusicList)
                        elif 'getpos' in args[1]:
                            self.getposition(addr)
                        elif 'getstatus' in args[1]:
                            self.getstatus(addr)
                        elif 'help' in args[1]:
                            self.help(addr)
                        elif pyMD.CL_HELLO in args[1]:
                            print("Client connected ")
                            self.sendinfo(addr, PYMDString)
                        elif pyMD.CL_EXIT in args[1]:
                            print("Client disconected ")
                            self.sendinfo(addr, "bye bye")
                        else:
                            self.help(addr)
                    else:
                        self.sendinfo(addr, pyMD.ERR_PASSWD)
                except:
                    pass
        def load(self, cmd, addr):
            self.sendinfo(addr, self.m_player.setfile(cmd))
            return ex
        def play(self, addr):
            self.sendinfo(addr, self.m_player.play())
            return ex
        def stream(self, link, addr):
            self.sendinfo(addr, self.m_player.stream(link))
        def getposition(self, addr):
            self.sendinfo(addr, str(self.m_player.m_playerpos))
        def getstatus(self, addr):
            self.sendinfo(addr, str(self.m_player.get_status()))
        def getlenght(self):
            pass
        def help(self, addr):
            msg = ["getdb = get the current files in directory data",
                   "load#{music title} = load music file from db example: load#music.ogg",
                   "stream#{http addr}",
                   "getpos = get current play position",
                   "play = start the music",
                   "getstatus = get current status"]
            i = len(msg)
            self.sendinfos(addr, i, msg)
        def sendinfos(self, addr, i, args):
            self.m_socket.sendto(str.encode(str(i)), addr)
            for arg in args:
                self.m_socket.sendto(str.encode(arg), addr)
        def sendinfo(self, addr, info):
            self.m_socket.sendto(str.encode(str(1)), addr)
            self.m_socket.sendto(str.encode(info), addr)

    print (PYMDString)
    print (AUTHOR)
    print ()
    
    pm = pymusic()
    pm.start()
    
    #pl.setfile('music.ogg')
    #pl.play()
    
        
        
    
