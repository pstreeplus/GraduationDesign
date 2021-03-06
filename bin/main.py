#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import glob
import sys
import ConfigParser

sys.path.append('../lib')
import PreProcess
from Recognization import Recognization


class Main(object):
    """
    核心模块:
        1.预处理
        2.特征提取
        3.训练模型
        4.识别
        5.后处理
        6.模型评估
    """

    def __init__(self, cfg='../conf/main.cfg'):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(cfg)
        self.data_dir = self.conf.get('DEFAULT', 'data_dir')
        self.pic_dir = self.conf.get('DEFAULT', 'pic_dir')
        self.pre_dir = self.conf.get('DEFAULT', 'pre_dir')
        train_pic = self.conf.get('PREPROCESS', 'train_pic')
        self.file_name = os.path.join(self.pic_dir, train_pic)
        self.preprocess = PreProcess.PreProcess(self.file_name, self.conf)
        self.recognize = Recognization()


if __name__ == '__main__':
    pass
