import glob
import os
import queue
import sys

import ffmpy
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'Download manager'
        self.left = 10
        self.top = 10
        self.width = 350
        self.height = 300
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        windowLayout = QHBoxLayout()
        self.setLayout(windowLayout)

        #Labels
        label = QLabel("Paste url page:", self)
        label.move(120,5)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(10, 40)
        self.textbox.resize(330,30)
        
        # Create a button in the window
        self.button1 = QPushButton('Download', self)
        self.button1.move(10,75)
        
        self.button2 = QPushButton('Browse', self)
        self.button2.move(120,75)

        self.button3 = QPushButton('Abort', self)
        self.button3.move(230,75)

        # self.button4 = QPushButton('Compress', self)
        # self.button4.move(250,75)
      
        # connect button to function on_click
        self.button1.clicked.connect(self.on_click1)
        self.button2.clicked.connect(self.on_click2)
        self.button3.clicked.connect(self.on_click3)
        #self.button4.clicked.connect(self.on_click3)

        # Increase progress bar
        self.progressBar = QProgressBar(self, minimumWidth=335)
        self.progressBar.setValue(0)
        self.progressBar.move(8,60)
        windowLayout.addWidget(self.progressBar)

        # Download button event
    def on_click1(self):
        textboxValue = self.textbox.text
        the_url = textboxValue()

        #print(the_url.split(" ", 1)[2])

        #print(textboxValue, the_url)

        QMessageBox.question(self, "Message", "\n" + the_url, QMessageBox.Apply, QMessageBox.Cancel)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",  the_url, ".mp4", "Mp4 format (.mp4);;All formats (*)", options=options)

        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = fileName
        the_fileobj = open(the_filepath, 'wb') 

        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    # Setting progress bar
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "Tips", "Download success!")
            self.progressBar.setValue(0)
            return

    def on_click2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", ".mp4", "Mp4 format (.mp4);;All formats (*)", options=options)
        if fileName:
            print(fileName)


    def on_click3(self):
         self.downloadThread.terminate() 
         self.close()

    # def compressing(self):

    #     files = {}
    #     for f in file_names:
    #         print("")
    #         outfile_name 

    #     original_files = []
    #     compressed_files = []
    #     for f in files:
    #         outfile_name = files[f]
    #         if outfile_name != "":
    #             outfile = "%s\\%s" % (the_filepath, outfile_name)
    #         try:
    #             os.remove(outfile)
    #         except:
    #             pass
    #         input_params={f:None}
    #         output_params = {outfile: '-vcodec libx264 -crf %s'}
    #         ff = ffmpy.FFmpeg(inputs=input_params,outputs=output_params)
    #         print(ff.cmd)
    #         ff.run()
    #         original_files.append(f)
    #         compressed_files.append(outfile)
    #         print("Done")

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
