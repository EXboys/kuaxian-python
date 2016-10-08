# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'browser.ui'
#
# Created: Fri Aug 19 17:07:42 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(640, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("65b9816egw1f6575nda98j20dw08pgmh.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setWindowOpacity(0.95)
        self.webView = QtWebKit.QWebView(Form)
        self.webView.setGeometry(QtCore.QRect(10, 60, 621, 411))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Forward = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Forward.setObjectName(_fromUtf8("Forward"))
        self.horizontalLayout.addWidget(self.Forward)
        self.Back = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Back.setObjectName(_fromUtf8("Back"))
        self.horizontalLayout.addWidget(self.Back)
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.Go = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Go.setObjectName(_fromUtf8("Go"))
        self.horizontalLayout.addWidget(self.Go)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.Forward, QtCore.SIGNAL(_fromUtf8("clicked()")), self.webView.forward)
        QtCore.QObject.connect(self.Back, QtCore.SIGNAL(_fromUtf8("clicked()")), self.webView.back)
        QtCore.QObject.connect(self.Go, QtCore.SIGNAL(_fromUtf8("clicked()")), self.webView.reload)
        QtCore.QObject.connect(self.Go, QtCore.SIGNAL(_fromUtf8("pressed()")), self.webView.reload)
        QtCore.QObject.connect(self.Back, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit.selectAll)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit, self.Go)
        Form.setTabOrder(self.Go, self.Back)
        Form.setTabOrder(self.Back, self.Forward)
        Form.setTabOrder(self.Forward, self.webView)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.Forward.setText(_translate("Form", "Forward", None))
        self.Back.setText(_translate("Form", "Back", None))
        self.Go.setText(_translate("Form", "Go", None))

from PyQt4 import QtWebKit

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
