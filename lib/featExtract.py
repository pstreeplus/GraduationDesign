#! /usr/bin/env python
# -*- coding:utf-8 -*-

import util

class FeatExtract(object):
    """
    特征提取模块:

    """


    @staticmethod
    def featExt(image, label, width=16, height=16):
        """
        :param: image
        :return: feat

        提取特征值
        """

        x, y = image.size
        bound_x = util.projection(image)
        bound_y = util.projection(image, lambda a, b: b)
        feat.append(util.get_max_min(bound_x)[1])
        feat.append(util.get_max_min(bound_y)[1])
        for i in xrange(x / width):
            for j in xrange(y / height):
                x1 = j * height
                x2 = x1 + height
                y1 = i * width
                y2 = y1 + width
                local_image = image.crop((x1, y1, x2, y2))
                feat.append(sum(util.projection(local_image)))

        feat.append(label)
        return feat
