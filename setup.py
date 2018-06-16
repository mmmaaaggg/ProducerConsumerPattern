#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/14 16:07
@File    : setup.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as rm:
    long_description = rm.read()

setup(name='prodconpattern',
      version='0.2.0',
      description='通过装饰器方式实现生产者消费者模式。可以作用于函数、类的方法上，使其变为异步调用，同时，转变为逐次调用，批量执行。方便将零碎的调用转变为批量形势进行统一执行。',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='MG',
      author_email='mmmaaaggg@163.com',
      url='https://github.com/mmmaaaggg/ProducerConsumerPattern',
      packages=find_packages(),
      python_requires='>=3.4',
      classifiers=(
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Development Status :: 5 - Production/Stable",
          "Environment :: No Input/Output (Daemon)",
          "Intended Audience :: Developers",
          "Natural Language :: Chinese (Simplified)",
          "Topic :: Software Development",
      ),
      install_requires=[])
