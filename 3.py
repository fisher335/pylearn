# coding:utf-8
import os, sys

li = []
for root, dirs, files in os.walk('c:/pylearn'):
    for i in files:
        li.append(i.decode('GBK'))
print li
