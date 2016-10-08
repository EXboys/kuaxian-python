#! /usr/bin/env python
# -*- coding: utf-8 -*-
try:
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    pass
import py2exe,os
from glob import glob
from distutils.core import setup
path = sys.executable
path = path[0:path.rfind(os.sep)]
imageformats = path+os.sep+"Lib\site-packages\PyQt4\plugins\imageformats\*.*"

includes = ["encodings", "encodings.*", "sip"]
packages = ["lxml", "gzip"]

options = {"py2exe":
           { "compressed": 1,
             "optimize": 2,
             "includes": includes,
             "packages": packages,
             # "dll_excludes": ["MSVCP90.dll"],# msvcp90.dll
             # "typelibs": [("{A435DD76-804E-4475-8FAB-986EACD1C6BE}", 0x0, 1, 0), ],
             "bundle_files": 1}
          }
setup(
    version="0.1.0",
    description="pyWinds",
    name="Powered py Chen",
    author="xiaocaiyidie",
    options=options,
    zipfile=None,
    data_files=[
        ("view/default/imgs", glob(r"view/default/imgs/*.*")),
        ("view/default/imgs/skin", glob(r"view/default/imgs/skin/*.*")),
        ("view/default/css", glob(r"view/default/css/*.*")),
        ("view/default/js", glob(r"view/default/js/*.*")),
        ("view/default", glob(r"view/default/*.*")),
        ("view", glob(r"view/*.*")),
        ('imageformats', glob(imageformats))
    ],
windows=[{
        "script":"index.py",
        'icon_resources': [(1, 'view/default/imgs/icon.ico')]
    }],
    # windows=["index.py"],
)

