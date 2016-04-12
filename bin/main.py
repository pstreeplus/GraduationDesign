#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import glob
import sys
import ConfigParser

sys.path.append('../lib')
import PreProcess
import Recognization

class Main(object):
    """
    主模块:
        1.预处理
        2.特征提取
        3.训练模型
        4.识别
        5.后处理
        6.模型评估
    """

    def __init__(self, file_names=[], cfg='../conf/main.cfg'):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(cfg)
        self.data_dir = self.conf.get('DEFAULT', 'data_dir')
        self.pic_dir = self.conf.get('DEFAULT', 'pic_dir')
        train_pic = self.conf.get('PREPROCESS', 'train_pics').strip(',')
        if not isinstance(file_names, list):
            file_names = [file_names]
        self.file_names = [os.path.join(self.pic_dir, file_name)
                            for file_name in file_names]
        if train_pic:
            self.file_names += [os.path.join(self.pic_dir, file_name.strip())
                                for file_name in train_pic.split(',')]
        if not self.file_names:
            self.file_names += glob.glob(
                os.path.join(self.pic_dir, self.conf.get('PREPROCESS', 'extend_name')))
        if not self.file_names:
            raise ValueError('no files are specifed.')
        self.preprocess = PreProcess.PreProcess(self.file_names, self.conf)

    def lauch(self):
        self.preprocess.division()

if __name__ == '__main__':
    Main().lauch()
    #print '1244q324'
    #print Recognization.image_file_to_string('../data/resource/3.png').strip()
