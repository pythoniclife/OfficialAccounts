# -*- coding: utf-8 -*-
import os
import pandas as pd

excel_list = []
for dir_paths, dir_names, file_names in os.walk(os.getcwd()):  # 遍历各文件夹、子文件夹内的所有文件
    '''将筛选出的各电子表格文件，分别添加到列表中'''
    [excel_list.append(pd.read_excel(os.path.join(dir_paths, filename))) for filename in file_names if (('.xlsx' in filename) or ('.xls' in filename))]

pd.concat(excel_list).to_excel('new_file.xlsx', index=False)  # 连接列表内的各个表格，并保存到新文件中


