#! /usr/bin/env python
# -*- coding:utf-8 -*-


class PreProcess(object):

    def __init__(self, file_names=[], conf=None):
        if not file_names:
            raise ValueError('PreProcess init, argument can not be empty.')
        if not isinstance(file_names, list):
            file_names = [file_names]
        self.file_names = file_names
        if conf:
            PreProcess.cut_dir = conf.get('DEFAULT', 'cut_dir')
        else:
            PreProcess.cut_dir = '../data/cut/'

    def gray(self):
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

    def binaryzation(self):
        from PIL import Image, ImageFilter
        self.images = [Image.open(file_name)
                for file_name in self.file_names]
        self.images = [image.filter(ImageFilter.MedianFilter()) for image in self.images]
        self.images = [image.convert('RGB') for image in self.images]
        self.gray()
        for i in xrange(len(self.images)):
            image = self.images[i]
            x, y = image.size
            for j in xrange(x):
                for k in xrange(y):
                    pixel = 0 if image.getpixel((j, k)) > 127 else 255
                    self.images[i].putpixel((j, k), pixel)
        return self.images

    def division(self):
        self.binaryzation()
        for image in self.images:
            self.__cutting(image)

    @staticmethod
    def __projection(image):
        x, y = image.size
        xs = [0] * x
        ys = [0] * y
        for i in xrange(y):
            for j in xrange(x):
                pixel = 1 if image.getpixel((j, i)) == 255 else 0
                xs[j] += pixel
                ys[i] += pixel
        return xs, ys

    @staticmethod
    def __correct(image):
        x = []
        y = []

        return image, x, y

    @staticmethod
    def __cutting(image):
        image, x, y = PreProcess.__correct(image)
        x, y = PreProcess.__projection(image)
        image.show()
        cnt = 0
        bounds = []
        x = [min(x)] + x + [max(x)]
        for i in xrange(len(x) - 1):
            if x[i] <= x[0] < x[i + 1]:
                bounds.append(i)
            elif x[i] > x[0] >= x[i + 1]:
                bounds.append(i - 1)
        for i in xrange(0, len(x), 2):
            if i + 1 < len(bounds) and bounds[i + 1] - bounds[i] >= 4:
                image.crop((bounds[i], 0, bounds[i + 1], image.size[1]))\
                    .save(PreProcess.cut_dir + '%d.png' % cnt)
                cnt += 1