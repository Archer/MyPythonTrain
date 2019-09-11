# -*- coding:utf-8 -*-
'''
操作目录
 '''
import os

def test_walk():
    for paths, dirs, files in os.walk("..", topdown=False):
        print("this paths:")
        print(paths)
        print("this dirs:")
        print(dirs)
        print("this files:")
        print(files)

def test_listdir():
    for paths in os.listdir(".."):
        print(paths)

print(os.getcwd())
print(os.path)
