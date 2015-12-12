#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
用于版本比较的对象
"""


class Version(object):
    """版本对象, 可以参与比较
    因为业务逻辑, 暂时只考虑纯数字版本号

    1.2.3 > 1.2.2
    1.2.3 < 1.2.3.0 < 1.2.3.4
    """

    def __init__(self, ver_str):
        try:
            self.__ver_nums = self.__parse_ver_str(ver_str)
        except:
            self.__ver_nums = self.__parse_ver_str("0.0")

    def __getitem__(self, index):
        return self.__ver_nums[index]

    def __len__(self):
        return len(self.__ver_nums)

    def __parse_ver_str(self, ver_str):
        if ver_str is None:
            return [0]

        ver_nums = ver_str.split(".")
        for index, num in enumerate(ver_nums):
            num = int(num)
            if num < 0:
                raise ValueError('version number must be positive integer')
            ver_nums[index] = num
        return ver_nums

    def __str__(self):
        return ".".join([str(x) for x in self.__ver_nums])

    def __repr__(self):
        return repr(self.__ver_nums)

    def __cmp(self, other):
        """类似字符串比较

        返回:
            大于 返回大于0的值,
            等于 0,
            小于 返回小于0 的值
        """
        length = min(len(self), len(other))
        for i in xrange(length):
            res = self[i] - other[i]
            if res != 0:
                return res
        else:
            # 版本好如果字段不存在则认为是无穷小, 例如
            # 1.2.3 < 1.2.3.1
            return len(self) - len(other)

    def __gt__(self, other):
        return self.__cmp(other) > 0

    def __lt__(self, other):
        return self.__cmp(other) < 0

    def __ge__(self, other):
        return self.__cmp(other) >= 0

    def __le__(self, other):
        return self.__cmp(other) <= 0

    def __eq__(self, other):
        return self.__cmp(other) == 0

    def __ne__(self, other):
        return self.__cmp(other) != 0
