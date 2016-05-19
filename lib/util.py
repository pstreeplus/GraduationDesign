#! /usr/bin/env python
# -*- coding:utf-8 -*-

import math
from PIL import Image


def get_width(bounds, get_bounds=False):
    """
    :param bounds (list of int)
    :return ret (image)

    获取数组的宽度, 作为图像投影后的宽度

    """

    y2 = 0
    ret = 0
    width = 0
    minv = min(bounds)
    for i in xrange(len(bounds)):
        if bounds[i] != minv:
            width += 1
        else:
            width = 0
        if ret < width:
            ret = width
            y2 = i + 1
    if not get_bounds:
        return ret
    else:
        return y2 - ret, y2


def projection(image, func=lambda a, b: a):
    """
    :param image:
    :return: retsult

    将像素向X轴或者Y轴投影, 默认向X轴进行投影

    """

    x, y = image.size
    result = [0] * func(x, y)
    for i in xrange(y):
        for j in xrange(x):
            pixel = 1 if image.getpixel((j, i)) == 255 else 0
            result[func(j, i)] += pixel
    return result


def extend_image(image, delta_w = 40, delta_h = 40):
    """
    :param：image：
    ：return：new_image：

    对原图像进行扩展

    """

    x, y = image.size
    new_image = Image.new('L', (x + delta_w, y + delta_h))
    new_image.paste(image, (delta_w / 2, delta_h / 2, x + delta_w / 2, y + delta_h / 2))
    return new_image

def get_max_min(arr, func=lambda a, b: a < b):
    position = 1
    value = arr[0]
    for i in xrange(1, len(arr)):
        if func(value, arr[i]):
            value = arr[i]
            position = i + 1
    return position, value

def normal(arr):
    length = 0
    for value in arr:
        length += value * value
    length = math.sqrt(length * 1.0)
    for i in xrange(len(arr)):
        arr[i] = int(arr[i]/ length * 10000)