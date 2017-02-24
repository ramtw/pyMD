#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) Client
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
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pyMD
import socket
import sys
import signal
import pyaes

def recive(s, _hash):
    data, addr = s.recvfrom(2048)
    crtxt = pyMD.hexToByte(data.decode("utf-8"))
    crypt_aes = pyaes.AESModeOfOperationCTR(_hash)
    msg = crypt_aes.encrypt(crtxt)

    len = int(msg)
    
    for i in range(len):
        data, addr = s.recvfrom(2048)
        crtxt = pyMD.hexToByte(data.decode("utf-8"))
        crypt_aes = pyaes.AESModeOfOperationCTR(_hash)
        msg = crypt_aes.encrypt(crtxt).decode("utf-8")
        
        if pyMD.ERR_PASSWD in msg:
            input("Wrong hash bye bye ....")
            sys.exit(1)
        else:
           print("\t" + msg)
def send(s, msg, _hash):
    msg = str(msg)
    crypt_aes = pyaes.AESModeOfOperationCTR(_hash)
    ciphertext = pyMD.byteToHex(crypt_aes.encrypt(msg))
    s.sendto(str.encode(ciphertext), (host, int(port)))
    
    recive(s, _hash)
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
    cfg = pyMD.client_config()
    
    
    host = cfg.get_server_addr()
    port = cfg.get_server_port()
    _hash = cfg.get_server_hash()
    
    

# try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #send(s, pyMD.CL_HELLO, _hash)
    while True:
        msg = input(str(host) + ":" + str(port) + " > ")
        if 'exit' in msg:
            exit(s, 0)
        else:
            send(s, msg, _hash)
   # except:
     #   print("Conection error")
