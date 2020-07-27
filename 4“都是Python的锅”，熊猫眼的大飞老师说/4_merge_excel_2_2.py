# -*- coding: utf-8 -*-
import os
import time
import pandas as pd

old_file_name = input('请输入原始空白表格的文件名（包含扩展名）：')  # 其它填写过数据的文件与这个原始文件进行比对
list_old = [str(row) for row in pd.read_excel(old_file_name).itertuples(index=False)]  # 将原始表格按行遍历并存入列表

file_dir = os.getcwd()  # 获取当前工作目录
file_list_all = os.listdir(file_dir)  # 获取目录下的所有文件名
# 清洗掉非excel文件和原始空白文件，将剩余的电子表格文件存入列表中
file_list_excel = [item for item in file_list_all if (('.xlsx' in item) or ('.xls' in item)) and (old_file_name not in item)]

list_new = []  # 空列表用于存放下面各个表格中新增的内容
for file in file_list_excel:
    '''遍历所有excel文件，把基于原始空白表格新增的内容过滤出来'''
    file_path = os.path.join(file_dir, file)  # 连接而成当前文件的完整路径
    list_file = [ro for ro in pd.read_excel(file_path).itertuples(index=False)]  # 将当前表格按行遍历并存入列表
    [list_new.append(r) for r in list_file if str(r) not in list_old]  # 当前文件与原始文件进行比对，筛选出的新增内容存入列表

df = pd.DataFrame(list_new)  # 将存有所有新内容的列表进行合并
df.to_excel('new_file.xlsx', index=False)  # 将合并后的数据存到文件中

print('Ok, 3秒后退出。')
time.sleep(3)

