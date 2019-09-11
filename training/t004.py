# -*- coding:UTF-8 -*-
import re

def word_counts():
    with open('../source/T004_S.txt', 'r') as file:
        tt = file.read()
        pattern = re.compile(r'div.*?/div')
        list_str = pattern.findall(tt)
        print(list_str)

word_counts()




