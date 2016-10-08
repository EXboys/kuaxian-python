#! /usr/bin/env python  
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import os,sys
from glob import glob  

path = sys.executable
path = path[0:path.rfind(os.sep)]
imageformats = path+os.sep+"Lib\site-packages\PyQt4\plugins\imageformats\*.*"

setup(  
    options = {  
      "py2exe": {  
        # "dll_excludes": ["MSVCP90.dll"],
        "includes":["sip"],
        "compressed": 1,
        "optimize": 2,
      }  
    },
    name = 'pyWinds',
    version = '0.1 beta',
    author="小菜一碟",
    windows = [
        {
            'script':'pyWinds.py',
            'icon_resources': [(1, 'view/default/imgs/icon.ico')]
        }
    ],
    data_files = [
        ("view/default/imgs", glob(r"view/default/imgs/*.*")),
        ("view/default/imgs/skin", glob(r"view/default/imgs/skin/*.*")),
        ("view/default/css", glob(r"view/default/css/*.*")),
        ("view/default/js", glob(r"view/default/js/*.*")),
        ("view/default", glob(r"view/default/*.*")),
        ("view", glob(r"view/*.*")),
        ('imageformats', glob(imageformats))
    ] 
)

