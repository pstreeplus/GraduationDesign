#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore
sys.path.append('../bin')
sys.path.append('../lib')
import coreApi
from Recognization import Recognization


class Front(QtGui.QWidget):
    """前端展示界面程序"""

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('OCR Model')
        self.hbox = QtGui.QHBoxLayout(self)
        self.pic_lb = QtGui.QLabel(self)
        self.pic_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.hbox.addWidget(self.pic_lb)
        self.setLayout(self.hbox)
        start = QtGui.QPushButton('Start', self)
        start.setGeometry(185, 10, 60, 40)
        start.clicked.connect(self.launch)
        self.next_pic = QtGui.QPushButton('Next', self)
        self.prev_pic = QtGui.QPushButton('Prev', self)
        self.next_pic.setGeometry(265, 10, 60, 40)
        self.prev_pic.setGeometry(345, 10, 60, 40)

    def launch(self):
        self.pic_index = -1
        self.pic_paths = []
        self.core = coreApi.Main.get_inter_pics(core.Main())
        self.next_pic.clicked.connect(self.show_next_pic)
        self.prev_pic.clicked.connect(self.show_prev_pic)
        self.show_next_pic()

    def show_next_pic(self):
        self.pic_index += 1
        if self.pic_index == len(self.pic_paths):
            try:
                self.pic_paths.append(self.core.next())
            except StopIteration:
                self.pic_index -= 1
                return
        pic_path = self.pic_paths[self.pic_index]
        pixmap = QtGui.QPixmap(pic_path)
        self.pic_lb.setPixmap(pixmap)

    def show_prev_pic(self):
        self.pic_index -= 1
        if self.pic_index < 0:
            self.pic_index += 1
            return
        pic_path = self.pic_paths[self.pic_index]
        pixmap = QtGui.QPixmap(pic_path)
        self.pic_lb.setPixmap(pixmap)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    front = Front()
    front.show()
    sys.exit(app.exec_())
