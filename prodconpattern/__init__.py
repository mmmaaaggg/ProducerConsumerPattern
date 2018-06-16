#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/14 15:26
@File    : __init__.py.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime


class ProducerConsumer(Thread):
    """
    实现生产者-消费者模式，被装饰函数将变为被异步调用
    """

    def __init__(self, threshold=100, interval=3, pass_arg_list=False, is_class_method=False, queue_timeout=5):
        super().__init__(daemon=True)
        self.queue = Queue()
        self.lock = Lock()
        self.threshold = threshold
        self.interval = interval
        self.pass_arg_list = pass_arg_list
        self.is_class_method = is_class_method
        self.func = []
        self.queue_timeout = queue_timeout

    def __call__(self, func):
        # 通过 [func] 方式进行保存，是为了防止调用的时候讲当前对象传递进去
        self.func = [func]
        self.name = func.__name__

        def _call(*args, **kwargs):
            # print('call ', func.__name__, *args, **kwargs)
            with self.lock:
                if not self.is_alive():
                    # print('start worker thread')
                    self.start()
            self.queue.put_nowait((args, kwargs))
            # self._func(*args, **kwargs)

        return _call

    def run(self):
        if len(self.func) != 1:
            return

        func = self.func[0]
        if self.pass_arg_list:
            # 类方法对象为key 而进行分组调用
            class_method_args_dic, self_obj_key = {}, ''

            datetime_last_invoke = datetime.now()
            while True:
                try:
                    args_tmp, kwargs_tmp = self.queue.get(timeout=self.queue_timeout)
                    # 获取对象
                    if self.is_class_method:
                        self_obj_key = args_tmp[0]
                        args_tmp = args_tmp[1:]

                    # 获取相关参数列表
                    args_list, kwargs_list_dic, args_len, datetime_last_invoke = class_method_args_dic.setdefault(
                        self_obj_key, [[], {}, 0, datetime.now()])
                    # args_len = len(args_list)
                    # print("queue get args:", args_tmp)
                    for num, arg in enumerate(args_tmp):
                        # print(num, ")arg:", arg, "|", len(args), ')args:', args)
                        if len(args_list) <= num:
                            # 保持所有参数对齐，避免出现新增参数，与旧参数错位的情况
                            new_arg = [None for _ in range(args_len)]
                            new_arg.append(arg)
                            args_list.append(new_arg)
                        else:
                            args_list[num].append(arg)

                    for key, arg in kwargs_tmp.items():
                        # 保持所有参数对齐，避免出现新增参数，与旧参数错位的情况
                        kwargs_list_dic.setdefault(key, [None for _ in range(args_len)]).append(arg)

                    args_len += 1

                    # print('args_list:', args_list, "threshold", self.threshold, args_len >= self.threshold)
                    if args_len > 0 and (args_len >= self.threshold or (
                            datetime.now() - datetime_last_invoke).seconds >= self.interval):
                        # print('start real call -> self_obj_key, args_list, kwargs_list_dic:',
                        #       self_obj_key, args_list, kwargs_list_dic)
                        if self.is_class_method:
                            func(self_obj_key, *args_list, **kwargs_list_dic)
                        else:
                            func(*args_list, **kwargs_list_dic)
                        args_list.clear()
                        for _, v in kwargs_list_dic.items():
                            v.clear()
                        args_len = 0
                        # 更新 args_len, 最近执行时间
                        class_method_args_dic[self_obj_key] = [args_list, kwargs_list_dic, args_len, datetime.now()]
                    else:
                        # 更新 args_len
                        class_method_args_dic[self_obj_key][2] = args_len
                except Empty:
                    for num, (k, v) in enumerate(kwargs_list_dic.items()):
                        print('timeout check : %d) [%s] %s ' % (num, k, v))

                    for num, self_obj_key in enumerate(list(class_method_args_dic.keys())):
                        args_list, kwargs_list_dic, args_len, datetime_last_invoke = class_method_args_dic[self_obj_key]
                        # print('args_list:', args_list, "threshold", self.threshold, args_len >= self.threshold)
                        if args_len > 0 and (args_len >= self.threshold or (
                                datetime.now() - datetime_last_invoke).seconds >= self.interval):
                            # print('start real call -> self_obj_key, args_list, kwargs_list_dic:',
                            #       self_obj_key, args_list, kwargs_list_dic)
                            if self.is_class_method:
                                func(self_obj_key, *args_list, **kwargs_list_dic)
                            else:
                                func(*args_list, **kwargs_list_dic)
                            args_list.clear()
                            for _, v in kwargs_list_dic.items():
                                v.clear()
                            args_len = 0
                            # 更新 args_len, 最近执行时间
                            class_method_args_dic[self_obj_key] = [args_list, kwargs_list_dic, args_len, datetime.now()]
                        else:
                            # 更新 args_len
                            class_method_args_dic[self_obj_key][2] = args_len

        else:
            args_list = []
            kwargs_list = []
            args_len = 0
            datetime_last_invoke = datetime.now()
            while True:
                try:
                    args_tmp, kwargs_tmp = self.queue.get(timeout=self.queue_timeout)
                    # print("args_tmp:", args_tmp)
                    args_list.append(args_tmp)
                    kwargs_list.append(kwargs_tmp)

                    args_len += 1

                except Empty:
                    pass

                if args_len > 0 and (args_len >= self.threshold or (
                        datetime.now() - datetime_last_invoke).seconds >= self.interval):
                    # print("args_list, kwargs_list", args_list, kwargs_list)
                    for args, kwargs in zip(args_list, kwargs_list):
                        # print("args, kwargs", args, kwargs)
                        func(*args, **kwargs)
                        args_list = []
                        kwargs_list = []
                        args_len = 0
                        datetime_last_invoke = datetime.now()
