#! /usr/bin/env python  
# -*- coding: utf-8 -*-
'''
Created on 2016-8-27

@author: xiaocaiyidie
'''
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RoundWindow import RoundWindow
from PyQt4.QtWebKit import *
from common import Utils,app
import base64
import webbrowser
from Dialog import Dialog

class Window(RoundWindow):
    DialogWindow=None
    def __init__(self,url,width,height,windowType=0,handleMethod=""):
        super(Window, self).__init__()
        # self.resize(width,height)
        # self.round()
        self.showFullScreen()
        point = Utils.getDesktopCenterPoint(self)
        self.move(point["x"],point["y"])
        self.setWindowTitle(app.AppTitle)
        self.setWindowIcon(app.AppIcon)
        self.setWindowOpacity(app.Opacity)
        self.webview = QWebView(self)
        layout = QHBoxLayout()
        layout.addWidget(self.webview)
        self.setLayout(layout)
        self.webview.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, app.Debug)
        self.webview.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.webview.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.webview.settings().setLocalStoragePath(app.HomeDir + "/data")
        self.webview.settings().setDefaultTextEncoding("utf-8")
        #定制画布大小，一般为固定大小
        # self.webview.setGeometry(1,1,self.width()-2,self.height()-2)
        self.webview.setStyleSheet("QWebView{background-color: rgba(255, 193, 245, 0%); }")
        self.webview.page().networkAccessManager().setCookieJar(app.CookieJar)
        self.webview.page().mainFrame().javaScriptWindowObjectCleared.connect(self.setJavaScriptObject)
        self.webview.page().linkClicked.connect(self.linkClicked)
        # self.webview.page().featurePermissionRequested.connect(self.permissionRequested)
        self.webview.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.handleMethod= handleMethod
        self.subUrl=url
        self.windowType=windowType
        self.url = QUrl.fromLocalFile(app.ViewDir+"window.html")
        self.webview.load(self.url)
    
    # def permissionRequested(self,frame,feature):
    #    self.webview.page().setFeaturePermission(frame, feature, QWebPage.PermissionGrantedByUser)
         
    def linkClicked(self,url):
        url =  str(url)[20:-2]
        self.webview.page().mainFrame().evaluateJavaScript('loadFrame("%s")' % (url))
        # self.webview.load(url)
        # 使用默认浏览器打开
        # webbrowser.open(url.toString())
        # self.addressBar.setText(str(url)[20:-2])
     
    def setJavaScriptObject(self):
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_window_", self)
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_notifications_", app._notifications_)

    # 如有登录功能可以实现自动登录
    # def cancelAutoLogin(self):
    #     self.webview.page().mainFrame().evaluateJavaScript("window.localStorage.autoLogin='false';")
        
    @pyqtSignature("",result="QString")
    def getUrl(self):
        return self.subUrl
    
    @pyqtSignature("",result="QString")
    def getHandleMethod(self):
        return self.handleMethod
    
    @pyqtSignature("",result="int")
    def getWindowType(self):
        return self.windowType

    @pyqtSignature("")
    def openDialogWindow(self):
        if self.DialogWindow!=None:
            self.DialogWindow.show()
            return 
        self.DialogWindow = Dialog()
        self.DialogWindow.show()
        qe = QEventLoop()
        qe.exec_()

    @pyqtSignature("QString,QString")
    def windowAlert(self,title,text):
        QMessageBox.information(self,title,text)

    @pyqtSignature("")
    def fullScreen(self):
        self.fullScreen()

    @pyqtSignature("")
    def minimize(self):
        if(self.windowType==0):
            self.hide()
        else:
            self.showMinimized()
    
    @pyqtSignature("")
    def quit(self):
        if(self.windowType==0):
            res = QMessageBox.question(self, "关闭提示", "你点击了关闭按钮\n你是想“最小化”还是“退出”？",
                                       "最小化", "退出","取消",0,2)
            if(res==1):
                QApplication.instance().quit()
            elif(res==0):
                self.hide()
        else:
            self.close()
    
    @pyqtSignature("int,int")
    def moveTo(self,offsetX,offsetY):
        self.move(self.x()+offsetX,self.y()+offsetY)
    
    @pyqtSignature("QString,int,int,int,QString")
    def open(self,url,width,height,windowType,handleMethod):
        win = Window(url,width,height,windowType,handleMethod)
        win.show()
        qe = QEventLoop()
        qe.exec_() 
    
    @pyqtSignature("",result="QString")
    def getSkinItem(self):
        path = app.ViewDir+"/imgs/skin/"
        html = ["<ul class='skin-imgs'>"]
        for file in os.listdir(path):
            html.append("<li>")
            html.append("<img  src='./imgs/skin/"+file+"'/>")
            html.append("</li>")
        html.append("</ul>")
        return ''.join(html)