# -*- coding: UTF-8 -*-
# Author: NagatoYou

from PIL import Image    # 请先安装Pillow库！
import os
from sys import exit

# 格式列表
FORMAT_LIST = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]


def images_to_PDF(path, mode, save_name):
    filelist = os.listdir(path)
    piclist = []
    images = []
    
    for i in filelist:    # 获取所有指定格式图像的路径
        if i.split(".")[-1] in FORMAT_LIST:
            piclist.append(i)
    if len(i) == 0:
        print("\n该目录下没有指定格式的图像！")
        return 1

    if mode != 0:    # 创建时间升序
        piclist = sorted(piclist, key=lambda files: os.path.getctime(os.path.join(path, files)))
    else:    # 文件名升序
        piclist.sort()
    max_width = 0

    for i in piclist:
        temp = Image.open(os.path.join(path, i))
        width = temp.size[0]
        if width > max_width:
            max_width = width
        if temp.mode in ["RGBA", "LA"]:    # 将带A通道转化为白底不带A通道
            temp1 = Image.new("RGB", temp.size, (255, 255, 255))
            temp1.paste(temp, mask=temp.getchannel("A"))
            temp = temp1
        images.append(temp)

    print("\n读取完毕。")
    for i in range(len(images)):
        height = images[i].size[1]
        height1 = round(max_width / images[i].size[0] * height)
        if (images[i].size[0] != max_width):
            images[i] = images[i].resize((max_width, height1), Image.ANTIALIAS)    # 按比例放大
        print("正在适配第 " + str(i + 1) + " / " + str(len(images)) + " 张图片")

    print("\n正在保存......")
    temp = images[0]
    if len(images) != 1:    # 保存为PDF
        temp.save(save_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
    else:
        temp.save(save_name, "PDF", resolution=100.0, save_all=True)
    print("\n保存成功。")
    return 0

def get_PDF_name():
    save_name = input("\n请输入保存PDF的名称(不包括后缀名，不能与该路径下已存在的PDF文件重名)：\n")
    while os.path.isfile(save_name + ".pdf"):
        print("请不要与该路径下已存在的PDF文件重名！")
        save_name = input("\n请输入保存PDF的名称(不包括后缀名，不能与该路径下的PDF文件重名)：\n")
    return save_name

if __name__ == "__main__":
    mode_valid = False
    path = input("请输入源文件的路径(空默认为工作目录)：\n")
    if path == "":
        path = os.getcwd()
    elif os.path.isfile(path):    # 单文件，单独处理，提前退出
        if path.split(".")[-1] not in FORMAT_LIST:
            print("\n该文件不是指定格式！")
            exit()
        temp = Image.open(path)
        save_name = get_PDF_name()
        print("\n正在保存......")
        temp.save(save_name + ".pdf", "PDF", resolution=100.0, save_all=True)
        print("\n保存成功。")
        exit()
    
    while not mode_valid:    # 输入模式整数
        try:
            mode = input("\n请输入模式对应的编号整数\n[0(空)：按照文件名排序 非0：按照创建日期排序]：")
            if mode == "":
                mode = 0
            mode = int(mode)
            mode_valid = True
        except ValueError:
            print("请输入一个整数！")

    save_name = get_PDF_name()
    images_to_PDF(path, mode, save_name + ".pdf")
