import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
import queue
import ConcurrentQueue
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket

import threading,time


HOST,PORT = '',8090


#cond = threading.Condition()

#dataQue = queue.Queue(100)
dataQue = ConcurrentQueue.ConcQueue(100)
class DataHelper:

    @staticmethod
    def pushData(data):
        #print('start push')

        try:
            dataQue.put(data)
        except Exception as e:
            print('pushData Error:', e)
        finally:
            print('push data ok')
            pass

    @staticmethod
    def PopData():

        try:
            #print('PopData get data')
            #data = dataQue.get(block=True)
            data = dataQue.get()
        except Exception as e:
            print('PopData Error:', e)
            return None
        finally:
            #print('Pop data ok:',data)
            return data

    @staticmethod
    def clearData():
        dataQue.clear()

    @staticmethod
    def isEmpty():
        return dataQue.empty()







class TodoHandler(BaseHTTPRequestHandler):

    # def __init__(self,parent = None):
    #     super(TodoHandler, self).__init__(parent)
    #     print('TodoHandler __init__')

    def do_GET(self):
        self.send_error(415, 'Only post is supported')

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        #ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        print("111",ctype, pdict)
        #token = self.headers['X-Auth-Token']
        #print("222",token)

        if(ctype == 'multipart/form-data'):
            path = str(self.path)  # 获取请求的url
            #if path == '/v1/people/add_by_base64img':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
            postvars = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = postvars.get('person_uuid')
            print(messagecontent)


        if ctype == 'application/json':

            path = str(self.path)  # 获取请求的url
            #print("url:"+path)
            if path == '/heatbeat':
                #print(path)
                dictHeart = dict()
                length = int(self.headers['content-length'])  # 获取除头部后的请求参数的长度
                datas = self.rfile.read(length)  # 获取请求参数数据，请求数据为json字符串
                #print(datas)
                rjson = json.loads(datas.decode())
                print(rjson,type(rjson))


                dictHeart['heatbeat']=rjson

                DataHelper.pushData(dictHeart)

                # self.send_response(200)
                # self.send_header('Content-type', 'application/json')
                # self.end_headers()
                # self.wfile.write(json.dumps({'message':' ',"resout":0}).encode())

            elif path == '/record':
                # print(path)
                dictRecord = dict()
                length = int(self.headers['content-length'])  # 获取除头部后的请求参数的长度
                datas = self.rfile.read(length)  # 获取请求参数数据，请求数据为json字符串
                # print(datas)
                rjson = json.loads(datas.decode())
                print(rjson,type(rjson))
                dictRecord['record']=rjson
                DataHelper.pushData(dictRecord)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message':'ok',"resout":0}).encode())

            else:
                self.send_error(404, "Not Found")
        else:
            self.send_error(415, "Only json data is supported.")





class HttpDaemon(QThread):

    def __init__(self, parent=None):
        super(HttpDaemon, self).__init__(parent)
        self.working = True

    def run(self):
        print('HttpDaemon run ',self.working)
        self._server = HTTPServer((self.__GetLocalIPByPrefix('192.168.1'), PORT), TodoHandler)
        self._server.serve_forever()  #阻塞
        print('end HttpDaemon', self.working)


    def stop(self):
        self._server.shutdown()
        self._server.socket.close()
        self.wait()
        print('stop http')

        # 多网卡情况下，根据前缀获取IP

    def __GetLocalIPByPrefix(self,prefix):
        localIP = ''
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip.startswith(prefix):
                localIP = ip
        return localIP



class RecThread(QThread):
    def __init__(self, parent=None):
        super(RecThread, self).__init__(parent)
        self.working = True
    def run(self):
        print('RecThread run ',self.working)
        while self.working:
            data = DataHelper.PopData()
            print('Recthread:',data)




if __name__ == '__main__':
    class MainWidget(QWidget):
        def __init__(self, parent=None):
            super(MainWidget, self).__init__(parent)
            self.setWindowTitle("QThread")
            self.thread = HttpDaemon()
            self.recthread =RecThread()
            self.listFile = QListWidget()
            self.btnStart = QPushButton('开始')
            layout = QGridLayout(self)
            layout.addWidget(self.listFile, 0, 0, 1, 2)
            layout.addWidget(self.btnStart, 1, 1)
            self.btnStart.clicked.connect(self.slotStart)

            print('1111')

        def slotAdd(self, file_inf):
            print('slotAdd')
            self.listFile.addItem(str(file_inf))

        def slotStart(self):
            print('slotStart')
            self.btnStart.setEnabled(False)
            self.thread.start()
            self.recthread.start()
            print('slotStart11')






    # from PyQt5.QtWidgets import QApplication
    print('=================')
    #ui= DestUi();
    app = QApplication(sys.argv)
    server = MainWidget()
    server.show()
    sys.exit(app.exec_())

    print('=================')




