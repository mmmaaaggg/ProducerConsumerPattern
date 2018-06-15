# ProducerConsumerPattern
[![Build Status](https://travis-ci.org/mmmaaaggg/ProducerConsumerPattern.svg?branch=master)](https://travis-ci.org/mmmaaaggg/ProducerConsumerPattern)

通过装饰器方式实现生产者消费者模式。
可以作用于函数、类的方法上，使其变为异步调用，同时，转变为逐次调用，批量执行。方便将零碎的调用转变为批量形势进行统一执行。

[Github 地址：ProducerConsumerPattern](https://github.com/mmmaaaggg/ProducerConsumerPattern)

### 安装
> pip install prodconpattern

### 示例代码

函数调用：逐次调用 -> 异步逐次调用
```python
from prodconpattern import ProducerConsumer

@ProducerConsumer(threshold=3)
def method_single_invoke(n):
    """函数调用：逐次调用 -> 异步逐次调用"""
    print('method_single_invoke ->', n)

import time

# 函数调用：逐次调用 -> 异步逐次调用
for n in range(10):
    print("call -> method_single_invoke(%d)" % n)
    method_single_invoke(n)

time.sleep(6)
```

函数调用：逐次调用 -> 异步批量调用
```python
from prodconpattern import ProducerConsumer

@ProducerConsumer(threshold=3, pass_arg_list=True)
def method_list_invoke(n):
    """函数调用：逐次调用 -> 异步批量调用"""
    print('method_list_invoke ->', n)

import time

# 函数调用：逐次调用 -> 异步批量调用
for n in range(10):
    # time.sleep(1)
    print("call -> method_list_invoke(%d)" % n)
    method_list_invoke(n)

time.sleep(6)
```

对象方法调用：逐次调用 -> 异步批量调用
```python
from prodconpattern import ProducerConsumer

class AClass:

    @ProducerConsumer(threshold=3, pass_arg_list=True, is_class_method=True)
    def class_method_list_invoke(self, n):
        """对象方法调用：逐次调用 -> 异步批量调用"""
        print(self.__class__.__name__, "print_method", n)

import time

# 对象方法调用：逐次调用 -> 异步批量调用
aaa = AClass()
for n in range(10):
    print("call -> class_method_list_invoke(%d)" % n)
    aaa.class_method_list_invoke(n)

time.sleep(6)
```

更多例子参考
[example.py 文件](https://github.com/mmmaaaggg/ProducerConsumerPattern/blob/master/example.py)
