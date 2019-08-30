# -*- coding:utf-8 -*-
# 第 0000 题： 将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。 类似于图中效果
from PIL import Image, ImageDraw, ImageFont

def answer_1(img):
    draw = ImageDraw.Draw(img)
    my_font = ImageFont.truetype('C:/windows/fonts/Arial.ttf',size=20)
    fill_color = "#ff0000"
    draw.text((20, 20), 'Alan', font=my_font, fill=fill_color)
    img.save('../source/T000_R.jpg', 'jpeg')
    return 0

if __name__ == '__main__':
    image = Image.open('../source/T000_S.jpg')
    answer_1(image)

