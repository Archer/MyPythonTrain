# coding=utf-8
# 第 0001 题： 做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券）
# ，使用 Python 如何生成 200 个激活码（或者优惠券）？
import random, string

def answer_1(length):
    for_select = string.ascii_letters + "0123456789"
    str = ""
    for y in range(length):
        str += random.choice(for_select)
    return str

def answer_2(length):
    s = string.ascii_letters + "0123456789" + "!@#$%&*_+"
    return "".join(random.sample(s, length))


if __name__ == "__main__":
    print(answer_2(30))


