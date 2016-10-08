#! /usr/bin/env python  
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QSystemTrayIcon,QApplication

#根据字符串，获得QT的托盘图标
def getQtTrayIconFromString(str):
    if(str=="info"):
        return QSystemTrayIcon.Information
    if(str=="warn"):
        return QSystemTrayIcon.Warning
    if(str=="error"):
        return QSystemTrayIcon.Critical
    return QSystemTrayIcon.NoIcon

def getDesktopCenterPoint(frame):
    desktop = QApplication.desktop()
    x = (desktop.width() - frame.width())/2
    y = (desktop.height() - frame.height())/2
    return {"x":x,"y":y}
