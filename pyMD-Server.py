#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) Server
# 
# $Id: $
#
# Copyright (c) 2017 Anna-Sophia Schroeck <annasophia.schroeck at outlook.de>

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

  # 1. The origin of this software must not be misrepresented; you must not
     # claim that you wrote the original software. If you use this software
     # in a product, an acknowledgment in the product documentation would be
     # appreciated but is not required.
  # 2. Altered source versions must be plainly marked as such, and must not be
     # misrepresented as being the original software.
  # 3. This notice may not be removed or altered from any source distribution.

  

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = "annas"
__date__ = "$05.02.2017 04:39:03$"


import vlc
import os
import sys
import hashlib
import socket
import pyMD
import pyaes

from enum import Enum

if __name__ == "__main__":
    def end_callback(event, vlcplayer):
        vlcplayer.setend()
    def pos_callback(event, vlcplayer):
        vlcplayer.m_playerpos = vlcplayer.get_vlc().get_position() 


   
    
    
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
            self.m_cfg = pyMD.server_config()
            self.m_player = vlcplayer(self.m_cfg)
            self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.m_socket.bind((self.m_cfg.get_server_addr(),
                                self.m_cfg.get_server_port()))
        def start(self):
           
            print ("Listening on %s:%d...\n" % (self.m_cfg.get_server_addr(),
                       self.m_cfg.get_server_port()))
            print ("The hash for the client, check the configuration.")
            print ("Server and client must have the same hash.")
            
            _hash = self.m_cfg.get_server_hash()
            while True:
                try:
                    data, addr = self.m_socket.recvfrom(2048)
                    
                    crtxt = pyMD.hexToByte(data.decode("utf-8"))
                    crypt_aes = pyaes.AESModeOfOperationCTR(_hash)
                    plaintext = crypt_aes.encrypt(crtxt)

                    args =  plaintext.decode("utf-8").split("#") 
                    #com#argument
                    
                    if "load" in args[0]:
                        self.load(args[1], addr)
                    elif "stream" in args[0]:
                        self.stream(args[1], addr)
                    elif 'play' in args[0]:
                        self.play(addr)
                    elif 'getdb' in args[0]:
                        i = len(vlcplayer.MusicList)
                        self.sendinfos(addr, i, vlcplayer.MusicList)
                    elif 'getpos' in args[0]:
                        self.getposition(addr)
                    elif 'getstatus' in args[0]:
                        self.getstatus(addr)
                    elif 'help' in args[0]:
                        self.help(addr)
                    elif pyMD.CL_HELLO in args[0]:
                        print("Client connected ")
                        self.sendinfo(addr, pyMD.PYMDString)
                    elif pyMD.CL_EXIT in args[0]:
                        print("Client disconected ")
                        self.sendinfo(addr, "bye bye")
                    else:
                        self.help(addr)
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
            if self.m_player.get_status() == pyMD.status.STOP:
                self.sendinfo(addr, str(0))
            else:
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
            self.cryptsend(str(i), addr)
            for arg in args:
                 self.cryptsend(arg, addr)
        def sendinfo(self, addr, info):
            self.cryptsend(str(1), addr)
            self.cryptsend(info, addr)
        def cryptsend(self, plain, addr):
             _hash = self.m_cfg.get_server_hash()
             crypt_aes = pyaes.AESModeOfOperationCTR(_hash)
             ciphertext = pyMD.byteToHex(crypt_aes.encrypt(plain))
             self.m_socket.sendto(str.encode(ciphertext), addr)
        
            

    print (pyMD.PYMDString)
    print (pyMD.AUTHOR)
    print ()
    
    pm = pymusic()
    pm.start()
    
    
        
        
    
