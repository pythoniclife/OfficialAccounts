# -*- coding: utf-8 -*-
import os
import time
import pandas as pd

file_dir = os.getcwd()  # 获取当前工作目录
file_list_all = os.listdir(file_dir)  # 获取目录下的所有文件名
file_list_excel = [item for item in file_list_all if ('.xlsx' in item) or ('.xls' in item)]  # 清洗非excel文件

new_list = []  # 空列表用于存放下面各个清洗后的表格
for file in file_list_excel:
    '''遍历所有excel文件，删除空行'''
    file_path = os.path.join(file_dir, file)  # 连接而成当前文件的完整路径
    df = pd.read_excel(file_path)  # 读取当前excel文件
    data = pd.DataFrame(df.iloc[:, :]).dropna(axis=0, how='any')  # 对空行进行删除
    new_list.append(data)  # 删除空行后存入列表

df_all = pd.concat(new_list)  # 将所有删除空行的表格进行合并
df_all.to_excel('new_file.xlsx', index=False)  # 将合并后的数据存到文件中

print('Ok, 3秒后退出。')
time.sleep(3)


