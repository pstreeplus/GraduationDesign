#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
核心模块API, 前端调用接口:
"""

import os
import glob
import sys
import ConfigParser
from PIL import Image

import PreProcess, splitNormal
from Recognization import Recognization



class CoreAPI(object):
    def __init__(self, cfg='../conf/main.cfg'):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(cfg)
        self.data_dir = self.conf.get('DEFAULT', 'data_dir')
        self.pic_dir = self.conf.get('DEFAULT', 'pic_dir')
        self.pre_dir = self.conf.get('DEFAULT', 'pre_dir')
        train_pic = self.conf.get('PREPROCESS', 'train_pic')
        self.file_name = os.path.join(self.pic_dir, train_pic)
        self.preprocess = PreProcess.PreProcess()
        self.split_normal = splitNormal.SplitNormal()
        self.recognize = Recognization()

def get_inter_pics(coreAPI):
    yield coreAPI.file_name
    im = Image.open(coreAPI.file_name)
    im = coreAPI.preprocess.gray(im)
    image_name = coreAPI.pre_dir + 'gray.png'
    im.convert('RGB').save(image_name)
    yield image_name
    im = coreAPI.preprocess.binaryzation(im)
    image_name = coreAPI.pre_dir + 'binary.png'
    im.convert('RGB').save(image_name)
    yield image_name
    im = coreAPI.preprocess.correct(im)
    image_name = coreAPI.pre_dir + 'correct.png'
    im.convert('RGB').save(image_name)
    yield image_name
    im = coreAPI.split_normal.split_char_normal(im)[-1]
    image_name = coreAPI.pre_dir + 'line.png'
    im.convert('RGB').save(image_name)
    yield image_name


def get_text(img_path):
    return Recognization().recognize_from_file_name(img_path)


if __name__ == '__main__':
    get_inter_pics(CoreAPI())