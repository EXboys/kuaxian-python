# -*- coding: utf-8 -*-
import os
import time
import json
import urllib2,urllib
import sys
import wave,base64
from pyaudio import PyAudio, paInt16
reload(sys)
sys.setdefaultencoding('utf-8')

class recgnition:
    def __init__(self):
        self.pa = PyAudio()
        self.NUM_SAMPLES = 2000  # pyaudio内置缓冲大小
        self.SAMPLING_RATE = 8000  # 取样频率
        self.LEVEL = 1500  # 声音保存的阈值
        self.COUNT_NUM = 20  # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
        self.SAVE_LENGTH = 20  # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
        self.TIME_COUNT = 60  # 录音时间，单位s
        self.Voice_String = []

    def getToken(self,type):
        if not os.path.exists('./temp'+str(type)+'.txt'):
            token,expires = self.requestToken(type)
        else:
            f = open('./temp'+str(type)+'.txt','r').readlines()
            if float(list(f)[1].replace('\n',''))> time.time():
                token = list(f)[0].replace('\n','')
            else:
                token,_=self.requestToken(type)
        return token


    def requestToken(self,type=0):
        url = "https://openapi.baidu.com/oauth/2.0/token"
        if type == 0:
            values = {
                'grant_type': 'client_credentials',
                'client_id': 'gD5I9FwGLvIdcX55jXZrzT0Y',
                'client_secret': 'Sh43Mr460Kwh2ibHNPlwkzwBltfYiG1T'
            }
        else:
            values = {
                'grant_type': 'client_credentials',
                'client_id': 'MbktLVPac7Ywh8v8FlHqNUIL',
                'client_secret': 'REGs8YHi9nDg9HGnGv8mYLFSafoTQ6Tv'
            }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        resp = urllib2.urlopen(req)
        result = resp.read()
        json_data = json.loads(result)
        token = json_data['access_token']
        expires = json_data['expires_in'] + time.time()
        f = open('./temp'+str(type)+'.txt', 'w')
        f.write(str(token) + '\n')
        f.write(str(expires) + '\n')
        f.close()
        return token, expires

    # def dump_res(self,buf):
    #     print buf
    def savewav(self, filename):
        wf = wave.open(filename, 'wb')
        # print self.Voice_String
        wf.setnchannels(1)
        wf.setsampwidth(self.pa.get_sample_size(paInt16))
        wf.setframerate(self.SAMPLING_RATE)
        # wf.writeframes("".join(self.Voice_String))
        wf.writeframes(self.Voice_String)
        # wf.writeframes(self.Voice_String)
        wf.close()

    def speech(self,text,cuid):
        token = self.getToken(0)
        url = "http://tsn.baidu.com/text2audio?tex=" + text.decode(
            'utf-8') + "&lan=zh&per=0&pit=1&spd=7&rate=8000&cuid=" + cuid + "&ctp=1&tok=" + token
        os.system('mpg123 "%s"' % (url))
        # req = urllib2.Request(url)
        # self.Voice_String = base64.b64encode(urllib2.urlopen(req).read())
        # print self.Voice_String
        # self.savewav('speak.wav')

if __name__ == '__main__':
    cuid = '68-F7-28-B8-68-EC'
    recoder = recgnition()
    recoder.speech(u'你好！你好',cuid)
    # wav =  recoder.getBase64Str()
    # print wav
    # recgnition = recgnition()
    # recgnition.recg_cloud(cuid)
