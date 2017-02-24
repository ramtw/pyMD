#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) setup
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

from setuptools import setup, find_packages

setup (
       name='pyMD',
       version='0.8',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['vlc'],

       # Fill in these to make your Egg ready for upload to
       # PyPI
       author='Anna-Sophia Schroeck',
       author_email='pba3h11aso@t-online.de',

       summary='a mini python network music deamon',
       url='',
       license='gpl',
       long_description='a mini python network music deamon',

       # could also include long_description, download_url, classifiers, etc.

  
       )
