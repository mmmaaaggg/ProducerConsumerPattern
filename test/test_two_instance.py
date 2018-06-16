#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/16 10:01
@File    : test_duplicate_obj.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from prodconpattern import ProducerConsumer
import time

class AClass:

    def __init__(self, name):
        self.name = name

    @ProducerConsumer(threshold=3, pass_arg_list=True, is_class_method=True)
    def class_method_list_invoke(self, n):
        """对象方法调用：逐次调用 -> 异步批量调用"""
        print(self.name, "print_method", n)


# 对象方法调用：逐次调用 -> 异步~批量调用
aaa = AClass('aaa')
bbb = AClass('bbb')
for n in range(10):
    print("call -> class_method_list_invoke(%d)" % n)
    aaa.class_method_list_invoke(n)
    bbb.class_method_list_invoke(n)

time.sleep(20)