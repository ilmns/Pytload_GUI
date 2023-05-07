#!/usr/bin/env python

import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from download_thread import downloadThread

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Download manager'
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        label_layout = QHBoxLayout()
        main_layout.addLayout(label_layout)

        label = QLabel("Paste URL page:")
        label_layout.addWidget(label)

        self.textbox = QLineEdit()
        label_layout.addWidget(self.textbox)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        self.button1 = self.create_button("Download", self.on_click1)
        button_layout.addWidget(self.button1)

        self.button2 = self.create_button("Browse", self.on_click2)
        button_layout.addWidget(self.button2)

        self.button3 = self.create_button("Abort", self.on_click3)
        button_layout.addWidget(self.button3)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        main_layout.addWidget(self.progressBar)

    def create_button(self, label, on_click):
        button = QPushButton(label)
        button.clicked.connect(on_click)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return button

    # ... (Rest of the App class definition from the previous code)


    def on_click1(self):
        textboxValue = self.textbox.text()
        the_url = textboxValue
        QMessageBox.question(self, "Message", "\n" + the_url, QMessageBox.Apply, QMessageBox.Cancel)

        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = self.get_save_file_name()

        if not the_filepath:
            return

        the_fileobj = open(the_filepath, 'wb')

        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    def get_save_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", ".mp4", "Mp4 format (.mp4);;All formats (*)", options=options)
        return fileName

    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "Tips", "Download success!")
            return

    def on_click2(self):
        fileName = self.get_save_file_name()
        if fileName:
            print(fileName)

    def on_click3(self):
        self.close()
