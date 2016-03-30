#! /usr/bin/env python
# -*- coding:utf-8 -*-


class PreProcess(object):

    def __init__(self, file_names=[]):
        if not file_names:
            raise ValueError('PreProcess init, argument can not be empty.')
        if not isinstance(file_names, list):
            file_names = [file_names]
        self.file_names = file_names

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
        self.gray()
        for i in xrange(len(self.images)):
            image = self.images[i]
            x, y = image.size
            for j in xrange(x):
                for k in xrange(y):
                    pixel = 255 if image.getpixel((j, k)) > 127 else 0
                    self.images[i].putpixel((j, k), pixel)
        return self.images

    def division(self):
        self.binaryzation()
        for image in self.images:
            image.show()
            self.__cutting(image)

    @staticmethod
    def __projection(image):
        x, y = image.size
        xs = [0] * x
        ys = [0] * y
        for i in xrange(y):
            for j in xrange(x):
                pixel = 1 if image.getpixel((j, i)) == 0 else 0
                xs[j] += pixel
                ys[i] += pixel
        return xs, ys

    @staticmethod
    def __cutting(image):
        x, y = PreProcess.__projection(image)
        cnt = 0
        bounds = []
        """
        all_pixel = float(sum(x))
        x = [value / all_pixel for value in x]
        minx = min(x)
        x = [minx if v <= 0.01 else v for v in x]
        print x
        """
        x = [2 * min(x)] + x + [max(x)]
        for i in xrange(len(x) - 1):
            if x[i] <= x[0] < x[i + 1]:
                bounds.append(i)
            elif x[i] > x[0] >= x[i + 1]:
                bounds.append(i - 1)
        for i in xrange(0, len(x), 2):
            if i + 1 < len(bounds) and bounds[i + 1] - bounds[i] >= 4:
                image.crop((bounds[i], 0, bounds[i + 1], image.size[1])).save('../data/cut/cut_%d.png' % cnt)
                cnt += 1

