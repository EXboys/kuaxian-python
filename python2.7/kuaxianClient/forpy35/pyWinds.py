#! /usr/bin/env python  
# -*- coding: utf-8 -*-
'''
Created on 2016-8-24
@author: xiaocaiyidie
'''
import json
import sys
from os import getcwd

# from PyQt5.QtCore import QTextCodec
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QSystemTrayIcon,QApplication,QSplashScreen,QAction,QMenu
from common import app
from core.lib.Window import Window
from PyQt5.QtNetwork import QNetworkCookieJar
from core.lib.Notification import NotificationPresenter


def main(args):  
    App = QApplication(args)
    splash = QSplashScreen(QPixmap("./view/default/imgs/splash.jpg"))
    splash.show()
    App.processEvents()
    # QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
    initProperty()
    app.MainWin = Window(app.MainSrc, app.WinWidth, app.WinHeight)
    app.MainWin.show()
    splash.finish(app.MainWin)
    createTray()
    App.exec_()
    
def createTray():
    #托盘 
    app.TrayIcon=QSystemTrayIcon(app.AppIcon, app.MainWin)
    app.TrayIcon.activated.connect(trayClick)
    app.TrayIcon.setToolTip("pyWinds for PC")
    app.TrayIcon.setContextMenu(createTrayMenu(app.TrayIcon))
    app.TrayIcon.show()

def trayClick(reason):
    if(reason==3):
        if app.MainWin.isHidden():
            app.MainWin.show()
        app.MainWin.activateWindow()
    
def createTrayMenu(trayIcon):
    trayIconMenu = QMenu()
    action = QAction("主界面",trayIcon)
    action.triggered.connect(lambda:trayClick(3))
    trayIconMenu.addAction(action)
    action = QAction("退出",trayIcon)
    action.triggered.connect(QApplication.instance().quit)
    trayIconMenu.addAction(action)
    return trayIconMenu
    
    
def initProperty():
    manifest = json.load(open('./view/app.json'))
    app.AppTitle = manifest['name'] if manifest['name'] else app.AppTitle
    app.HomeDir = getcwd()
    app.Template = manifest['app'] if manifest['app'] else app.Template
    app.ViewDir = app.HomeDir+'/view/'+app.Template+'/'
    app.AppIcon = QIcon(app.ViewDir + (manifest['ico'] if manifest['ico'] else app.AppIcon))
    #主页面配置
    app.MainSrc = manifest['main']['url'] if manifest['main']['url'] else app.MainSrc
    app.WinWidth = manifest['main']['width'] if manifest['main']['width'] else app.WinWidth
    app.WinHeight = manifest['main']['height'] if manifest['main']['height'] else app.WinHeight
    app.Opacity = manifest['opacity'] if manifest['opacity'] else app.Opacity
    #对话框配置
    app.DialogSrc = manifest['dialog']['url'] if manifest['dialog']['url'] else app.DialogSrc
    app.DialogCon = manifest['dialog']['content'] if manifest['dialog']['content'] else app.DialogCon
    app.DialogWidth = manifest['dialog']['width'] if manifest['dialog']['width'] else app.DialogWidth
    app.DialogHeight = manifest['dialog']['height'] if manifest['dialog']['height'] else app.DialogHeight
    app.DialogOpacity = manifest['dialog']['opacity'] if manifest['dialog']['opacity'] else app.DialogOpacity

    app._notifications_ = NotificationPresenter()
    app.CookieJar = QNetworkCookieJar()

    
if __name__ == "__main__":  
    main(sys.argv)