#! /usr/bin/env python  
# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from common import app
import webbrowser
import time

class NotificationPresenter(QDialog):
    
    def __init__(self):
        super(NotificationPresenter, self).__init__()
        rect = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(rect.width()-300,0,300,rect.height()))
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Popup|Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.webview = QWebView(self)
        self.webview.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, app.Debug)
        self.webview.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.webview.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        self.webview.settings().setLocalStoragePath(app.HomeDir + "/data")
        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.settings().setDefaultTextEncoding("utf-8")
        self.webview.setGeometry(0,0,self.width(),self.height())
        self.webview.setStyleSheet("QWebView{background-color: rgba(255, 193, 245, 0%); }")
        self.webview.load(QUrl.fromLocalFile(app.ViewDir + "notification.html"))
        self.webview.page().linkClicked.connect(self.linkClicked)        
        self.webview.page().mainFrame().javaScriptWindowObjectCleared.connect(self.setJavaScriptObject)
        self.webview.page().setLinkDelegationPolicy(self.webview.page().DelegateAllLinks)
        
    def linkClicked(self,url):
        webbrowser.open_new_tab(url.toString())
        
    def setJavaScriptObject(self):
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_notifications_", self)
        
    @pyqtSlot('QString,QString,QString,int')
    def showNotification(self,title,flag,html,delay):
        self.show()
        self.webview.page().mainFrame().evaluateJavaScript('showNotification("%s","%s","%s",%d)' %(title,flag,html,delay))
        
    @pyqtSlot('QString')
    def cleanNotification(self,flag):
        self.webview.page().mainFrame().evaluateJavaScript('removeNotice("%s")' %(flag))
        
    @pyqtSlot('int')
    def sleep(self,ms):
        time.sleep(ms/1000)