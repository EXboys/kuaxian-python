# -*- coding: utf-8 -*-
import socket, sys
import threading
import win32com.client
from printerClient import Printer
reload(sys)
sys.setdefaultencoding("utf-8")

class socketThread(threading.Thread):
    def __init__(self,fun_id,s,user):
        super(socketThread, self).__init__()
        self.fun_id = fun_id
        self.s = s
        self.user=user

    def run(self):
       if self.fun_id ==1:
           self.receive()
       else:
           self.sendMessage()

    def receive(self):
        while 1:
            try:
                buf = self.s.recv(1024)
                # print buf
                if len(buf):
                    print "he say: "+buf.decode('utf-8')
                    # 将接收的消息语音读出
                    # try:
                    #     import pythoncom
                    #     pythoncom.CoInitialize()
                    #     win32com.client.Dispatch("SAPI.SpVoice").Speak(str(buf).decode('utf-8'))
                    # except:
                    #     pass
                    buf = buf.replace('\r\n','')
                    if str(buf)==str('new'):
                        self.getNewOrders()
            except socket.error, e:
                print "Dialogue Over %s" % e
                pass
                # self.s.close()
                # sys.exit(0)

    def sendMessage(self):
        try:
            data = self.user + '\r\n'
            self.s.send(data)
        except socket.error, e:
            print "Dialogue Over %s" % e
            self.s.close()
            sys.exit(0)
        # 以下代码可实现聊天客户端的发送消息功能
        # while 1:
        #     try:
        #         data = raw_input('I say:')+'\r\n'
        #         self.s.send(data)
        #     except socket.error, e:
        #         print "Dialogue Over %s" % e
        #         self.s.close()
        #         sys.exit(0)

    def getNewOrders(self):
        try:
            if self.user:
                # print user
                # printer.notify()
                Printer().printerCtl('http://yii.kuaxiango.com/api/web/v1/notify/new-order', {'shop': self.user})
        except Exception:
            pass

def connectServer(host,port,user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        s.connect((host, port))
        valid = 'orAngeOfhiSpaiNtHatCanNOTgObaCk' + '\r\n'
        s.send(valid)
    except socket.error, e:
        print "Address-related error connecting to server: %s" % e
        sys.exit(1)
    thPool = []
    for i in range(2):
        thPool.append(socketThread(i,s,user))
    for th in thPool:
        th.start()
    for th in thPool:
        th.join()

if __name__ == '__main__':
    # host = '114.215.209.164'
    host = 'localhost'
    port = 1234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        s.connect((host, port))
        valid = 'orAngeOfhiSpaiNtHatCanNOTgObaCk'+'\r\n'
        s.send(valid)
    except socket.error, e:
        print "Address-related error connecting to server: %s" % e
        sys.exit(1)
    thPool = []
    for i in range(2):
        thPool.append(socketThread(i))
    for th in thPool:
        th.start()
    for th in thPool:
        th.join()

