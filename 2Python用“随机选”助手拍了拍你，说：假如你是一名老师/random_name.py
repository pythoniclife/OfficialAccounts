# -*- coding: utf-8 -*-
import random

names = []  # 创建空列表
with open('names.txt', 'r') as f:
    '''对文件中的姓名进行读取并放入空列表中'''
    for i in f.readlines():
        names.append(i[:-1])  # 记事本文件中，每行姓名后面隐藏着一个回车符，用这个切片方式，可以去掉

random_names = names.copy()  # 用列表的copy方法，对存放原始数据的列表names进行深拷贝，赋值给临时列表random_names，防止原始数据丢失

num = 0  # 打印到屏幕的每个姓名前面的序号，初始化为0
while True:
    '''实现选取任意数量的姓名（数），打印到屏幕。当所有姓名被选完后，姓名名单恢复初始值，进入新一轮随机选状态。'''
    try:
        '''为避免在输入姓名数量的时候可能会输入非数字值，这里用异常处理语句处理'''
        if len(random_names) == 0:
            '''当所有姓名被选完后，初始化各项数值，进入新一轮随机选状态。'''
            print('\n' + '+' * 100 + '\n上一轮随机抽取已经结束，下一轮开始了：\n' + '+' * 100 + '\n')
            num = 0
            random_names = names.copy()

        random_number = int(input('请从' + str(len(random_names)) + '人中输入要随机抽取的数量：'))
        if random_number > len(random_names):
            '''当输入的姓名数值大于存量数值时，跳到下轮循环'''
            continue

        print('-' * 100)
        for i in range(random_number):
            '''选取指定数量的姓名，打印到屏幕'''
            index = random.randint(0, len(random_names) - 1)
            num += 1
            print(num, random_names[index])
            del random_names[index]  # 上面被随机选中的姓名打印完后即从列表中删除，防止干扰下次随机选取
        print('-' * 100)

    except ValueError:
        pass
