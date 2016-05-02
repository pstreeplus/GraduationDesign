#! /usr/bin/env python
# -*- coding:utf-8 -*-

import util
from PIL import ImageFilter

class PreProcess(object):
    """
    图像预处理模块：
        1.图像灰度化
        2.灰度图像二值化
        3.二值图像矫正
    """

    @staticmethod
    def gray(image):
        """
        :return: self.images

        图像灰度化
        """

        image = image.convert('RGB')
        image = image.filter(ImageFilter.MedianFilter())
        r, g, b = image.split()
        x, y = image.size
        for j in xrange(x):
            for k in xrange(y):
                pixelr = r.getpixel((j, k))
                pixelg = g.getpixel((j, k))
                pixelb = b.getpixel((j, k))
                pixel = int(0.3 * pixelr + 0.59 * pixelg + 0.11 * pixelb)
                r.putpixel((j, k), pixel)
        image = r
        return image

    @staticmethod
    def binaryzation(image):
        """
        :return: ret_images

        图像二值化
        """
        x, y = image.size
        for j in xrange(x):
            for k in xrange(y):
                pixel = 0 if image.getpixel((j, k)) > 127 else 255
                image.putpixel((j, k), pixel)
        return image

    @staticmethod
    def correct(image, func=lambda a, b: b):
        """
        :param image:
        :return: image

        对整个图像进行矫正

        """

        image = util.extend_image(image)
        width = image.size[0]
        if func(1, 2) == 2:
            width = image.size[1]
        correct_image = image
        correct_image, width = PreProcess.__rotate(correct_image, width, func)
        correct_image, width = PreProcess.__rotate(correct_image, width, func, fact=-1)

        return correct_image

    @staticmethod
    def __rotate(image, width, func=lambda a, b: b, angle=46, fact=1):
        """
        :param: image
        :return: tmp_image, tmp_width

        旋转图像

        """

        tmp_image = image
        result_image = image
        for i in xrange(1, angle):
            tmp_image = image.rotate(i * fact)
            tmp_width = util.get_width(util.projection(tmp_image, func))
            if width >= tmp_width:
                width = tmp_width
                result_image = tmp_image
            else: break

        return result_image, width
