#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import glob
import sys
import ConfigParser

sys.path.append('../lib')
import PreProcess


class Main(object):

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
        self.preprocess = PreProcess.PreProcess(self.file_names)

    def lauch(self):
        self.preprocess.division()
        """
        self.images = self.preprocess.binaryzation()
        for (image, file_name) in zip(self.images, self.file_names):
            file_name = '_bin'.join(os.path.splitext(file_name))
            image.save(file_name)
        """

if __name__ == '__main__':
    Main().lauch()