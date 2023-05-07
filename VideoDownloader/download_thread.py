#!/usr/bin/env python
import requests, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk:
                    break
                self.fileobj.seek(offset)
                self.fileobj.write(chunk)
                offset += len(chunk)
                progress = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(progress))

            self.fileobj.close()
            self.exit(0)

        except Exception as e:
            print(e)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec_())

