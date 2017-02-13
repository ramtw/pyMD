#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythenMusicDeamon (pyMD) setup
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
