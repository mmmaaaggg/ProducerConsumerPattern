#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/14 15:32
@File    : example.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from prodconpattern import ProducerConsumer


@ProducerConsumer(threshold=3)
def method_single_invoke(n):
    """函数调用：逐次调用 -> 异步逐次调用"""
    print('method_single_invoke ->', n)


@ProducerConsumer(threshold=3, pass_arg_list=True)
def method_list_invoke(n):
    """函数调用：逐次调用 -> 异步批量调用"""
    print('method_list_invoke ->', n)


class AClass:

    @ProducerConsumer(threshold=3, pass_arg_list=True, is_class_method=True)
    def class_method_list_invoke(self, n):
        """对象方法调用：逐次调用 -> 异步批量调用"""
        print(self.__class__.__name__, "print_method", n)


if __name__ == "__main__":
    import time

    # 函数调用：逐次调用 -> 异步逐次调用
    for n in range(10):
        print("call -> method_single_invoke(%d)" % n)
        method_single_invoke(n)

    # 函数调用：逐次调用 -> 异步批量调用
    # for n in range(10):
    #     time.sleep(1)
    #     print("call -> method_list_invoke(%d)" % n)
    #     method_list_invoke(n)

    # 对象方法调用：逐次调用 -> 异步批量调用
    aaa = AClass()
    for n in range(10):
        print("call -> class_method_list_invoke(%d)" % n)
        aaa.class_method_list_invoke(n)

    time.sleep(6)
