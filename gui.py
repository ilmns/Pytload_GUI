import glob
import os
import queue
import sys
import bs4
import ffmpy
import requests
import urllib3
import playsound

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from ffmpy import FFmpeg
from PyQt5.QtMultimedia import QSound

options = QFileDialog.Options()
options |= QFileDialog.DontUseNativeDialog

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'Download manager'
        self.left = 10
        self.top = 10
        self.width = 370
        self.height = 450
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
        self.editBox.font()
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
        self.button1.move(0,45)
        
        self.button2 = QPushButton('Location', self)
        self.button2.move(90,45)

        self.button3 = QPushButton('Compress', self)
        self.button3.move(180,45)

        self.button4 = QPushButton('Exit', self)
        self.button4.move(270,45)

        self.button5 = QPushButton('List', self)
        self.button5.move(0,68)
      
        # connect button to function on_click
        self.button1.clicked.connect(self.on_click1)
        self.button2.clicked.connect(self.on_click2)
        self.button3.clicked.connect(self.on_click3)
        self.button4.clicked.connect(self.on_click4)

        # Increase progress bar
        self.progressBar = QProgressBar(self, minimumWidth=355)
        self.progressBar.setValue(0)
        self.progressBar.move(7.5,30)
        windowLayout.addWidget(self.progressBar)


        # Setting progress bar
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            playsound.playsound('clearly.mp3', True)
            QMessageBox.information(self, "Tips", "Download success!")
            self.progressBar.setValue(0)
            return

    def on_click1(self):
        editBoxValue = self.editBox.text
        the_url = editBoxValue()

        QMessageBox.question(self, "Message", "\n" + the_url, QMessageBox.Apply, QMessageBox.Cancel)
        fileName, _ = QFileDialog.getSaveFileName(self, "Saving file",  the_url, "Mp4 format (.mp4);;All formats (*)", options=options)

        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = fileName
        the_fileobj = open(the_filepath, 'wb')


        l = []
        l.append(the_url)
        x = 0
        y = 0

        for i in l:            
            self.table.setItem(x, y, QTableWidgetItem("{0}".format(i)))



            

        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()     

    def on_click2(self):
        editBoxValue = self.editBox.text
        the_url = editBoxValue()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",  the_url, "Mp4 format (.mp4);;All formats (*)", options=options)
        
        if fileName:
            print(fileName)

        # Compress
    def on_click3(self):

        textboxValue = self.editBox.text
        url = textboxValue()       

        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "" "(*)", "All formats (*)", options=options)
        if fileName:
            print(fileName)

        i_params={'pipe:0': '-f rawvideo -pix_fmt rgb24 -s:v 1280x720'},
        o_params={'pipe:1': '-c:v h264 -f mp4'}
        ff = ffmpy.FFmpeg(inputs=i_params, outputs=o_params) 
        print(ff.cmd)
        ff.run()

    def on_click4(self):
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

