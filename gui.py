import glob
import os
import queue
import bs4
import ffmpy
import ffmpeg
import requests
import urllib3
import playsound
import sys 

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from ffmpy import FFmpeg
from PyQt5.QtMultimedia import QSound


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyToolkit'
        self.left = 10
        self.top = 10
        self.width = 370
        self.height = 460
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        windowLayout = QHBoxLayout()
        self.setLayout(windowLayout)

        self.listWidget = QListWidget()
        self.listWidget.resize(300, 50)

        # Edit box with drag 
        self.editBox = QLineEdit(self)
        self.editBox.setDragEnabled(True)
        self.editBox.move(10, 10)
        self.editBox.resize(350,30)

        # Set data
        self.table = QTableWidget(self)
        self.tableItem = QTableWidgetItem()
        self.table.move(5,100)
        self.table.resize(360, 325)
        self.table.setRowCount(10)
        self.table.setColumnCount(1)
        self.table.setColumnWidth(50, 200)

        self.table.setHorizontalHeaderLabels(("Downloaded media;").split(";"))
        self.table.setVerticalHeaderLabels(("1;2;3;4;5;6;7;8;9;10;").split(";"))
        
        # Create a button in the window
        self.button1 = QPushButton('Download', self)
        self.button1.move(0,46)
        
        self.button2 = QPushButton('Location', self)
        self.button2.move(90,46)

        self.button3 = QPushButton('Compress', self)
        self.button3.move(180,46)

        self.button4 = QPushButton('Exit', self)
        self.button4.move(270,46)

        self.button5 = QPushButton('List', self)
        self.button5.move(0,70)
        
        self.button6 = QPushButton('Stream', self)
        self.button6.move(90,70)

        self.button7 = QPushButton('Meta', self)
        self.button7.move(180,70)
      
        # connect button to function on_click
        self.button1.clicked.connect(self.on_click1)
        self.button2.clicked.connect(self.on_click2)
        self.button3.clicked.connect(self.on_click3)
        self.button4.clicked.connect(self.on_click4)
        self.button5.clicked.connect(self.on_click5)
        self.button6.clicked.connect(self.on_click6)
        self.button7.clicked.connect(self.on_click7)

        
        # Increase progress bar
        self.progressBar = QProgressBar(self, minimumWidth=355)
        self.progressBar.setValue(0)
        self.progressBar.move(7.5,30)
        windowLayout.addWidget(self.progressBar)



        # Setting progress bar
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.setValue(0)
            QMessageBox.information(self, "Tips", "Download success!", playsound.playsound('/Users/nazgul/Projects/Python/Downloader/clearly.mp3', True))
            return

    def openFile(self):
        editBoxValue = self.editBox.text

        the_url = editBoxValue()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getSaveFileName(self, "SaveFileName", the_url, "Mp4 format (.mp4);;All formats (*)", options=options)

        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = fileName
        the_fileobj = open(the_filepath, 'wb')

        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()
        
        return the_url

    def tableContent(self, table):

        the_url = App.openFile(the_url)

        l = []

        rows = 0
        columns = 0
        for x in l:
            for i in x:
                newItem = QTableWidgetItem(i)
                self.tableWidget.setItem(rows, columns, newItem)
                rows += 1
            rows = 0
            columns += 1
                


        # l.append(the_url)
        # for i in range(len(l)):
        #     l.append(i)
        #     for j in range(len(l)):
        #         l.append(j)
        #         for item in l:
        #             item = QTableWidgetItem(the_url)
        #             setItem = self.table.setItem(i, j, item)
        #             break


    def on_click1(self):

        App.openFile(self)  


    def on_click2(self):

        App.openFile(self)
        the_url = App.openFile(the_url)
        fileName, _ = App.openFile(fileName)
        the_filesize = App.openFile(the_filesize)
        the_filepath = App.openFile(the_filepath)
        the_fileobj = App.openFile(the_fileobj)

        # Compress
    def on_click3(self):

        fileName, _ = App.openFile(fileName)
        name = fileName
        
        print(name)
        inp={name:None}
        outp = {"compressed1.mp4": "-vcodec h264 -crf 24"}

        ff=ffmpy.FFmpeg(inputs=inp,outputs=outp)
        print(ff.cmd)
        ff.run()

    def on_click4(self):
        sys.exit(app.exec_())

    def on_click5(self):
        editBoxValue = self.editBox.text
        the_url = editBoxValue()
        r = requests.get(the_url)
        http_encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(r.content, from_encoding=http_encoding)

        for link in soup.find_all('a', href=True):
            links = (link['href'])
            print(links)


    def on_click6(self):
        sys.exit(app.exec_())

    def on_click7(self):
        sys.exit(app.exec_())

    

#Download thread
class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)                        #Create signal

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)                #Streaming download mode
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)                            #Setting Pointer Position
                self.fileobj.write(chunk)                            #write file
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))        #Sending signal

            self.fileobj.close()    #Close file
            self.exit(0)            #Close thread

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    app.quit()
    sys.exit(app.exec_())

