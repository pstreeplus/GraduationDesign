#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


OCR = 'StuNoOcr'
NAME = "Ans.bmp"
NAME_ROOT = "Ans"


def call_tesseract(input_filename, output_filename):
    args = [OCR, input_filename, output_filename]
    proc = subprocess.Popen(args, stderr=subprocess.PIPE)
    proc.wait()


def image_to_string(im):
    try:
        image_to_scratch(im)
        call_tesseract(NAME, NAME_ROOT)
        text = get_text()
    finally:
        clean_up()
    return text


def image_file_to_string(filename):
    try:
        try:
            call_tesseract(filename, NAME_ROOT)
            text = get_text()
        except Exception as e:
            e = '[FATAL]: Format Error'
            print >> sys.stderr, e
    finally:
        clean_up()
    return text


def image_to_scratch(im):
    im.save(NAME, dpi=(200, 200))


def get_text():
    inf = file(NAME_ROOT + '.txt')
    text = inf.read()
    inf.close()
    return text


def clean_up():
    for name in (NAME, NAME_ROOT + '.txt'):
        try:
            os.remove(name)
        except OSError:
            pass
