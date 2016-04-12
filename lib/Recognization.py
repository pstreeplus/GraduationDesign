#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


class Recognization(object):
    """识别模块"""

    def __init__(self, ocr='StuNoOcr', name='Ans.bmp'):
        self.OCR = ocr
        self.NAME = name
        self.NAME_ROOT = os.path.splitext(name)[0]

    def call_my_model(self, file_name):
        args = [self.OCR, file_name, self.NAME_ROOT]
        proc = subprocess.Popen(args, stderr=subprocess.PIPE)
        return proc.wait()

    def recognize_from_im(self, im):
        try:
            self.image_to_scratch(im)
            self.call_my_model(self.NAME)
            text = self.get_text()
        finally:
            self.clean_up()
        return text

    def recognize_from_file_name(self, file_name):
        try:
            self.call_my_model(file_name)
            text = self.get_text()
        finally:
            self.clean_up()
        return text

    def image_to_scratch(self, im):
        im.save(self.NAME, dpi=(200, 200))

    def get_text(self):
        inf = file(self.NAME_ROOT + '.txt')
        text = inf.read()
        inf.close()
        return text

    def clean_up(self):
        for name in (self.NAME, self.NAME_ROOT + '.txt'):
            try:
                os.remove(name)
            except OSError:
                pass
