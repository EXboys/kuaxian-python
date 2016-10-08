# -*- coding: utf-8 -*-
# import tempfile
import time,requests
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from PyQt4.QtWebKit import *
import mp3play
import sys,json
reload(sys)
sys.setdefaultencoding('utf-8')
# from common import Utils,app
# order 数据格式
# order = {
#     'shop':'城西银泰店',
#     'add_time' : '2016-08-18 14:09',
#     'need_time':'2016-08-18 14:09',
#     'consignee' : '***',
#     'address' :'******************************',
#     'phone' :'*****',
#     'tips' : '****************************************，****************',
#     'goods' :  [{
#           "name": "【D】加拿大北极贝S / 4个",
#           "price": "26.00",
#           "quantity": "1",
#           "reward": "0"
#         },
#         {
#           "name": "【D】日本希鲮鱼150g",
#           "price": "28.00",
#           "quantity": "3",
#           "reward": "0"
#         },
#         {
#           "name": "【D】加拿大翡翠螺4只",
#           "price": "22.00",
#           "quantity": "1",
#           "reward": "0"
#         },
#         {
#           "name": "【D】新西兰青口4只",
#           "price": "16.00",
#           "quantity": "1",
#           "reward": "0"
#         },
#         {
#           "name": "【D】刺参1条",
#           "price": "58.00",
#           "quantity": "1",
#           "reward": "0"
#         }],
#     'total' : ['8','135.55'],
# }


class Printer():
    def __init__(self):
        self.Music = mp3play.load('./view/default/assets/notify.mp3')
    # the list of printers

    def printerList(self):
        printer = []
        printerInfo = QPrinterInfo()
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
        return printer
    # print tasks

    def printing(self,printer, context):
        printerInfo = QPrinterInfo()
        p = QPrinter()
        for item in printerInfo.availablePrinters():
            if printer == item.printerName():
                p = QPrinter(item)
        doc = QTextDocument()
        doc.setHtml(u'%s' % context)
        doc.setPageSize(QSizeF(p.logicalDpiX() * (80 / 25.4),
                                      p.logicalDpiY() * (297 / 25.4)))
        p.setOutputFormat(QPrinter.NativeFormat)
        doc.print_(p)

    # Format string for print

    def printFormat(self,**kwargs):
        text = u'<html><head><meta charset="UTF-8"></head><body><div style="text-align: left">' \
               u'<h1 align="center">{}</h1>'.format(kwargs['shop'])
        text +=u'<hr style="height:2px;border:none;border-top:2px groove skyblue;"/>'
        text +=u'<p>下单时间：{}</p><p>要求时间：{}</p>'.format(kwargs['add_time'],kwargs['need_time'])
        text +=u'<table width="100%"><thead ><tr><td width="45%">商品</td><td  width="20%">价格</td>' \
               u'<td width="20%">数量</td><td  width="15%">备注</td></tr></thead>' \
               u'<hr style="height:1px;border:none;border-top:1px dashed #CCC;"/><tbody>'
        for item in kwargs['goods']:
            text +=u'<tr><td width="45%">{}</td><td  width="20%">{}</td><td width="20%">{}</td>' \
                   u'<td  width="15%"></td></tr>'.format(item['name'],item['price'],item['quantity'],item['reward'])
        text +=u'</tbody></table>'
        text +=u'<hr style="height:1px;border:none;border-top:1px dashed #CCC;"/><p>客户：{}</p>' \
               u'<p>电话：{}</p><p>地址：{}</p>'.format(kwargs['consignee'],kwargs['phone'],kwargs['address'])
        text +=u'<hr style="height:1px;border:none;border-top:1px dashed #CCC;"/>'
        text +=u'<p>合计：{}份  ￥{}</p>'.format(*kwargs['total'])
        text +=u'<p>备注：{}</p>'.format(kwargs['tips'])
        text+= u'<hr style="height:2px;border:none;border-top:2px groove skyblue;" />' \
               u'<p align="center">外卖热线：400-161-1198</p></div></body></html>'
        return text

    def printerCtl(self,url, params, method='get'):
        if method == 'get':
            orders = requests.get(url, params)
        else:
            orders = requests.post(url, params)
        orders = json.loads(orders.text)['data']
        # print orders
        if orders:
            try:
                self.Music.play()
                import pythoncom, win32com.client
                pythoncom.CoInitialize()
                win32com.client.Dispatch("SAPI.SpVoice").Speak(u'您有新的订单，请及时确认')
            except:
                pass
            for data in orders:
                # Change the remind status if the order infomation has been printed
                requests.get('http://yii.kuaxiango.com/api/web/v1/notify/received',
                             {'order_id': data['order_id']})
                for i in range(2):
                    html = Printer().printFormat(**data)
                    p = "defaultPrinter"  # 打印机名称
                    Printer().printing(p, html)
                    time.sleep(1)
        else:
            try:
                # self.Music.play()
                import pythoncom, win32com.client
                pythoncom.CoInitialize()
                win32com.client.Dispatch("SAPI.SpVoice").Speak(u'暂时还没有订单')
            except:
                pass
