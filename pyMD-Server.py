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

if __name__ == "__main__":
    def end_callback(event, vlcplayer):
        print('End of media stream (event %s)' % event.type)
    def pos_callback(event, vlcplayer):
        vlcplayer.m_playerpos = vlcplayer.get_vlc().get_position() * 100


        
    
    
    class vlcplayer:
        MusicList = []
        
        def __init__(self,config):
            print("Start vlc system")
            self.m_data = config.get_music_path()
            self.m_playerpos = 0
            self.m_player =  vlc.Instance().media_player_new()
            self.event_manager =self.m_player.event_manager()
            self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, end_callback, self)
            self.event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, pos_callback, self)
            self.m_player.audio_set_volume(config.get_music_volume())
            print("Create music list")
            vlcplayer.MusicList = [f for f in os.listdir(self.m_data) if os.path.isfile(os.path.join(self.m_data, f))]
        def setfile(self,name):
            file = os.path.join(self.m_data,name) 
            Media =  vlc.Instance().media_new(str(file))
            self.m_player.set_media(Media)
            return "load file: " + file
        def play(self):
            self.m_player.play()
            return "play file"
        def get_vlc(self):
            return self.m_player
        def list_music(self):
            for title in vlcplayer.MusicList:
                print( title)
            
    

    class pymusic:
        def __init__(self):
            self.m_cfg = pyMD.config()
            self.m_player = vlcplayer(self.m_cfg)
            self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.m_socket.bind(('localhost', self.m_cfg.get_server_port()))
        def start(self):
            print ("Listening on %s:%d..." % ("localhost",
                       self.m_cfg.get_server_port()))
            while True:
                data, addr = self.m_socket.recvfrom(2048)
                args = data.decode("utf-8").split(":") 
                
                #pass:com:argument

                if "load" in args[1]:
                    ex = self.m_player.setfile(args[2])
                    self.sendinfo(addr, ex)
                elif 'play' in args[1]:
                    ex = self.m_player.play()
                    self.sendinfo(addr, ex)
                elif 'getdb' in args[1]:
                    i = len(vlcplayer.MusicList)
                    self.sendinfos(addr, i, vlcplayer.MusicList)

        def sendinfos(self, addr, i, args):
            self.m_socket.sendto(str.encode(str(i)), addr)
            for arg in args:
                self.m_socket.sendto(str.encode(arg), addr)
        def sendinfo(self, addr, info):
            self.m_socket.sendto(str.encode(str(1)), addr)
            self.m_socket.sendto(str.encode(info), addr)
    
    pm = pymusic()
    pm.start()
    
    #pl.setfile('music.ogg')
    #pl.play()
    
        
        
    
