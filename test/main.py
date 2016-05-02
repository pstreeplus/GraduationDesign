#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import glob
import sys
import ConfigParser

sys.path.append('../lib')
import PreProcess, splitNormal, featExtract
from Recognization import Recognization
from PIL import Image, ImageFilter


class Main(object):
    """
    测试主模块:
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
        self.preprocess = PreProcess.PreProcess
        self.recognize = Recognization()

    def launch(self):
        image = Image.open(self.file_name)
        image = self.preprocess.gray(image)
        image = self.preprocess.binaryzation(image)
        image = self.preprocess.correct(image)
        for lb, im in zip('2012061620',splitNormal.SplitNormal.split_char_normal(image)):
            print featExtract.FeatExtract.featExt(im, lb)

if __name__ == '__main__':
    Main().launch()
