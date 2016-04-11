#! /usr/bin/env python
# -*- coding:utf-8 -*-


class PreProcess(object):
    """
    图像预处理模块：
        1.图像灰度化
        2.灰度图像二值化
        3.二值图像矫正
        4.单个字符切分
        5.单个字符矫正
        6.字符归一化
    """

    def __init__(self, file_names=[], conf=None):
        if not file_names:
            raise ValueError('PreProcess init, argument can not be empty.')
        if not isinstance(file_names, list):
            file_names = [file_names]
        self.file_names = file_names
        if conf:
            PreProcess.cut_dir = conf.get('PREPROCESS', 'cut_dir')
            PreProcess.char_width = conf.getint('PREPROCESS', 'char_width')
        else:
            PreProcess.char_width = 3
            PreProcess.cut_dir = '..d/ata/cut/'

    def __gray(self):
        """
        :return: self.images

        图像灰度化
        """
        for i in xrange(len(self.images)):
            self.images[i] = self.images[i].convert('RGB')
            image = self.images[i]
            r, g, b = image.split()
            x, y = image.size
            for j in xrange(x):
                for k in xrange(y):
                    pixelr = r.getpixel((j, k))
                    pixelg = g.getpixel((j, k))
                    pixelb = b.getpixel((j, k))
                    pixel = int(0.3 * pixelr + 0.59 * pixelg + 0.11 * pixelb)
                    r.putpixel((j, k), pixel)
            self.images[i] = r
        return self.images

    def __binaryzation(self):
        """
        :return: self.images

        图像二值化
        """
        from PIL import Image, ImageFilter
        self.images = [Image.open(file_name)
                for file_name in self.file_names]
        self.images = [image.filter(ImageFilter.MedianFilter()) for image in self.images]
        self.__gray()
        for i in xrange(len(self.images)):
            image = self.images[i]
            x, y = image.size
            for j in xrange(x):
                for k in xrange(y):
                    pixel = 0 if image.getpixel((j, k)) > 127 else 255
                    self.images[i].putpixel((j, k), pixel)
        return self.images

    def division(self):
        """
        :return:

        字符分割
        """
        self.__binaryzation()
        image_names = []
        for i, image in enumerate(self.images):
            image_names.extend(self.__cutting(image, i))
        return image_names

    @staticmethod
    def __projection(image, func=lambda a, b: a):
        """
        :param image:
        :return: ret

        将像素向X轴或者Y轴投影, 默认向X轴进行投影
        """
        x, y = image.size
        ret = [0] * func(x, y)
        for i in xrange(y):
            for j in xrange(x):
                pixel = 1 if image.getpixel((j, i)) == 255 else 0
                ret[func(j, i)] += pixel
        return ret

    @staticmethod
    def __get_width(bounds, get_bounds=False):
        """
        :param bounds (list of int)
        :return ret (image)

        获取数组的宽度,作为图像投影后的宽度
        """
        y1 = 0
        y2 = 0
        ret = 0
        width = 0
        minv = min(bounds)
        for i in xrange(len(bounds)):
            if bounds[i] != minv:
                width += 1
                if width == 1:
                    y1 = i + 1
            else:
                width = 0
            if ret < width:
                ret = width
                y2 = i + 1
        if not get_bounds:
            return ret
        else:
            return y1, y2

    @staticmethod
    def __correct_image(image, func=lambda a, b: a >= b):
        #TODO
        """
        :param image:
        :return: image

        对整个图像进行矫正
        """
        ret = image
        width = image.size[1]
        for i in xrange(1, 46):
            tmp_image = image.rotate(i)
            tmp_width = PreProcess.__get_width(PreProcess.__projection(tmp_image, lambda a, b: b))
            if func(width, tmp_width):
                width = tmp_width
                ret = tmp_image
            else:
                break
        for i in xrange(1, 46):
            tmp_image = image.rotate(-i)
            tmp_width = PreProcess.__get_width(PreProcess.__projection(tmp_image, lambda a, b: b))
            if func(width, tmp_width):
                width = tmp_width
                ret = tmp_image
            else:
                break
        return ret

    @staticmethod
    def __correct_char(image):
        #TODO
        """
        :param image:
        :return: image

        对整个单个字符进行矫正, 并切分出字符
        """
        image = PreProcess.__correct_image(image, lambda a, b: a <= b)
        y1, y2 = PreProcess.__get_width(PreProcess.__projection(image, lambda a, b: b), True)
        image = image.crop((0, y1, image.size[0], y2))
        return image

    @staticmethod
    def __cutting(image, pic_idx):
        """
        :param image, pic_idx:
        :return: image_names

        切分字符，并保存
        """
        image = PreProcess.__correct_image(image)
        x = PreProcess.__projection(image)
        cnt = 0
        bounds = []
        image_name = []
        x = [min(x)] + x + [max(x)]
        for i in xrange(len(x) - 1):
            if x[i] <= x[0] < x[i + 1]:
                bounds.append(i)
            elif x[i] > x[0] >= x[i + 1]:
                bounds.append(i - 1)
        for i in xrange(0, len(x), 2):
            if i + 1 < len(bounds) and bounds[i + 1] - bounds[i] >= PreProcess.char_width:
                image_char = image.crop((bounds[i], 0, bounds[i + 1], image.size[1]))
                image_name.append(PreProcess.cut_dir + '%04d%d.png' % (pic_idx, cnt))
                PreProcess.__correct_char(image_char).save(image_name[-1])
                cnt += 1
        return image_name
