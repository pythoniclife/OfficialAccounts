# -*- coding: utf-8 -*-  # python默认不支持中文，通过这种方式声明编码格式为UTF-8，这样本程序就支持中文编码了
import os  # 本程序用于处理文件和目录
import time  # 本程序用于实现倒计时，增强用户体验
import win32com.client  # 本程序用于调用windows中的word，需要安装pywin32库

print('程序运行中，请安静、耐心地等待，全部转换完成会有提示，在此之前，请不要操作电脑上的Word程序。。。')  # 增强用户体验
print('_' * 118)  # 增强用户体验

file_dir = os.getcwd()  # 获取当前目录
file_list_all = os.listdir(file_dir)  # 返回上行代码拿到的当前目录下的文件或文件夹的名字的列表
file_list_pdf = [item for item in file_list_all if '.pdf' in item]  # 采取列表推导式的方式，对上行代码拿到的列表中的文件和文件夹进行清洗，只留下pdf文件

word_app = win32com.client.Dispatch('Word.Application')  # 调用当前系统的word程序，本程序仅在word 2016及以上版本调试通过

if len(file_list_pdf) == 0:
    """如果第11行代码清洗数据后返回的放有pdf文件的列表为空，则输出提示信息后程序退出"""
    for i in range(8, 0, -1):  # 以下几行代码，格式化输出信息到屏幕，增强用户体验
        """显示8秒倒计时"""
        print('\rWarning！当前目录下没有可供转换的pdf文件，{} 秒后自动退出！'.format(i), end='')
        time.sleep(1)
    exit()

serial_number = 0  # 计数器，用于输出到屏幕的每个文件前的序号
for file in file_list_pdf:
    """遍历每个pdf文件，并用win32com.client调用系统中的word程序打开pdf文件，并将每个pdf文件另存为word文件"""
    file_path = os.path.join(file_dir, file)  # 返回每个pdf文件的绝对路径
    try:  # 用try...except语句能捕获各种莫名其妙的错误，否则运行时会出现各种不可描述情况
        document = word_app.Documents.Open(file_path)  # 用word程序打开当前遍历到的pdf文件
        document.SaveAs(file_path[:-3] + 'docx')  # 将上行代码打开的pdf文件，另存为word文件
        document.Close()  # 关闭上行代码形成的word文件
        serial_number += 1  # 计数器加1
        print('第{}个文件转换完成： {}'.format(serial_number, file[:-3] + 'docx'))  # 格式化输出到屏幕文件转换的完成情况
    except BaseException:  # 捕获异常
        pass  # 不作任何处理

word_app.Quit()  # 上面循环遍历完所有pdf文件并转换完成后，将打开的word程序关闭

# 以下几行代码，格式化输出信息到屏幕，增强用户体验
print('_' * 118)
for i in range(8, 0, -1):
    """显示8秒倒计时"""
    print('\rWarning！所有文件转换完成，如果您不关闭程序，{} 秒后自动退出！'.format(i), end='')
    time.sleep(1)
