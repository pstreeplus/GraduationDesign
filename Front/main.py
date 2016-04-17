#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui, QtCore


class Front(QtGui.QWidget)):
    """前端展示界面程序"""

    def __init__(self):
        super(Front, self).__init__()

    def launch(self):



if __name__ == '__main__':
    Front().launch()
