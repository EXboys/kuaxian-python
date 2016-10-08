#! /usr/bin/env python  
# -*- coding: utf-8 -*-
from common import Utils,app
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Dialog(QWidget):
    def __init__(self):  
        super(Dialog, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Popup|Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.setWindowOpacity(app.DialogOpacity)
        self.resize(app.DialogWidth,app.DialogHeight)
        point = Utils.getDesktopCenterPoint(self)
        self.move(point["x"],point["y"])
        self.webview = QWebView(self)
        self.webview.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, app.Debug)
        self.webview.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.webview.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        self.webview.settings().setLocalStoragePath(app.HomeDir + "/data")
        #self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.settings().setDefaultTextEncoding("utf-8")
        self.webview.setGeometry(1,1,self.width()-2,self.height()-2)
        self.webview.page().mainFrame().javaScriptWindowObjectCleared.connect(self.setJavaScriptObject)
        self.webview.setStyleSheet("QWebView{background-color: rgba(255, 193, 245, 0%); }")
        self.webview.page().networkAccessManager().setCookieJar(app.CookieJar)
        self.webview.load(QUrl.fromLocalFile(app.ViewDir+app.DialogSrc))
        
    def setJavaScriptObject(self):
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_window_", self)
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_notifications_", app._notifications_)
          
    @pyqtSlot()
    def quit(self):
        self.close()
    
    @pyqtSlot("int,int")
    def moveTo(self,offsetX,offsetY):
        self.move(self.x()+offsetX,self.y()+offsetY)
    
    @pyqtSlot(result="QString")
    def loadHtml(self):
        if app.NewDialogHtml!= "":
            return app.NewDialogHtml

        file_object = open(app.ViewDir+app.DialogCon)
        try:
            dialogHtml = file_object.read()
        finally:
            file_object.close()
        app.NewDialogHtml = dialogHtml
        return dialogHtml