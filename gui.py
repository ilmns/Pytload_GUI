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
from PyQt5.QtMultimedia import QSound, QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget



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
        self.textBox = QLineEdit(self)
        self.textBox.setDragEnabled(True)
        self.textBox.move(10, 10)
        self.textBox.resize(350,30)

        # Set data
        self.table = QTableWidget(self)
        self.tableItem = QTableWidgetItem()
        self.table.move(0,100)
        self.table.resize(370, 325)
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
        
        self.button6 = QPushButton('Player', self)
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

    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.setValue(0)
            QMessageBox.information(self, "Tips", "Download success!", )
            playsound.playsound('/Users/nazgul/Projects/Python/Downloader/clearly.mp3', True)
            return

    def openFileNameDialog(self):

        textBoxValue = self.textBox.text
        the_url = textBoxValue()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", the_url ,"All Files (*)", options=options)
        if fileName:
            print(fileName)
        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = fileName
        the_fileobj = open(the_filepath, 'wb')
        fileName, _ = QFileDialog.getSaveFileName(self, "SaveFileName", the_url, "Mp4 format (.mp4);;All formats (*)", options=options)

        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = fileName
        the_fileobj = open(the_filepath, 'wb')
        

        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()
        
    
    def saveFileDialog(self):

        textBoxValue = self.textBox.text
        the_url = textBoxValue()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", the_url ,"All Files (*)", options=options)

        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = fileName
        the_fileobj = open(the_filepath, 'wb')
        
        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    def tableContent(self, table):

        textBoxValue = self.textBox.text
        the_url = textBoxValue()

        l = []

        rows = 0
        columns = 0
        for rows in l:
            for columns in l:
                newItem = QTableWidgetItem(rows)
                self.tableWidget.setItem(rows, columns, newItem)
                rows += 1
                return l.sort()
            rows = 0
            columns += 1


    
    def on_click1(self):

        App.saveFileDialog(self)
        

    
    def on_click2(self):

        App.openFile(self)
        the_url = App.openFile(the_url)
        fileName, _ = App.openFile(fileName)
        the_filesize = App.openFile(the_filesize)
        the_filepath = App.openFile(the_filepath)
        the_fileobj = App.openFile(the_fileobj)

       # Compress
    def on_click3(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        the_url = ""

        fileName, _ = QFileDialog.getSaveFileName(self, "SaveFileName", the_url, "All formats (*)", options=options)
        name = fileName
        print(name)
        inp={name:None}
        outp = {"/Users/nazgul/Movies/compressed1.mp4": "-vcodec h264 -crf 20"}

        ff=ffmpy.FFmpeg(inputs=inp,outputs=outp)
        ff.run()

    
    def on_click4(self):
        sys.exit(app.exec_())
    
    def on_click5(self):

        textBoxValue = self.textBox.text
        the_url = textBoxValue()
        r = requests.get(the_url)
        http_encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
        #soup = BeautifulSoup(r.content, from_encoding=http_encoding)
        soup = BeautifulSoup(r.content, features="html.parser")

        # for link in soup.find_all('a', href=True):
        #     links = (link['href'])

        html = bs4.BeautifulSoup(r.text, features="html.parser")
        print(html.title.text)

    
    def on_click6(self):

        self.player = VideoWindow()
        self.player.size()
        self.player.resize(1280, 720)
        self.player.show()
        
    
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


class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 720

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action

        newAction = QAction(QIcon('save.png'), '&Save', self)
        newAction.setShortcut('Ctrl+O')
        newAction.setStatusTip('New movie')
        newAction.triggered.connect(self.openFile)

        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)


        self.button8 = QPushButton('openFile', self)
        self.button8.move(0,450)
        
        self.button9 = QPushButton('exitCall', self)
        self.button9.move(90,450)

        self.button10 = QPushButton('play', self)
        self.button10.move(180,450)


        self.button8.clicked.connect(self.openFile)
        self.button9.clicked.connect(self.exitCall)
        self.button10.clicked.connect(self.play)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):

        
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())
        

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    app.quit()
    sys.exit(app.exec_())

