# -*- coding: utf-8 -*-
import random
import math
import time
import os


def str_to_test(str_data, level_number=3):
    """将一个字符串按照level，随机把相应字符替换成‘ _ ’，返回一个元组类型（被替换字符后的字符串，被替换掉的字符）。"""
    rate = level_number / 3  # 根据level的不同，关联难易程度的rate相应变化
    str_to_list = list(str_data)  # 将字符串类型转换成列表类型
    # 清洗干扰元素对应的索引，将可用元素的索引放入新列表
    letter_list_index = [index for index in range(len(str_to_list)) if str_to_list[index] not in ' .!\'-=()']
    # 随机选出跟level对应的元素索引，放入新列表
    random_list_index = random.sample(letter_list_index, math.ceil(len(letter_list_index) * rate))

    answer_str = ''  # 初始化存放被’ _ ‘替换的字符（答案）的变量
    for index in sorted(random_list_index):  # 对列表进行排序
        """将相应字符替换成’ _ ‘，将被替换的字符保存到’答案‘变量中"""
        answer_str += str_to_list[index] + ',\t'  # 将被替换字符格式化并保存到变量中
        str_to_list[index] = ' _ '  # 将字符串相应字符替换成’ _ ‘

    list_to_str = ''.join(str_to_list)  # 将被替换元素的列表内容转成字符串类型
    return list_to_str, answer_str  # 函数返回一个元组类型（被替换字符后的字符串，被替换掉的字符）


def input_book_serial():
    """输入要检测英语单词的范围对应的序号"""
    while True:
        """正确输入对应序号后退出循环"""
        try:
            input_serial_number = int(input(
                '\n'
                '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                '1.外研社小学三年级上册\n'
                '2.外研社小学三年级下册\n'
                '3.外研社小学四年级上册\n'
                '4.外研社小学四年级下册\n'
                '5.外研社小学五年级上册\n'
                '6.外研社小学五年级下册\n'
                '7.外研社小学六年级上册\n'
                '8.外研社小学六年级下册\n'
                '9.外研社小学三至六全册\n'
                '10.手动输入自定义英语词库对应文件名\n'
                '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                '请输入要考查记忆的单词所在范围对应的序号，输入‘0’退出程序：'))
            if 0 < input_serial_number <= 10:
                return input_serial_number
            if input_serial_number == 0:
                exit()
        except ValueError:
            pass


def input_level_serial():
    """输入检测难度对应的序号"""
    while True:
        """正确输入对应序号后退出循环"""
        try:
            input_level_number = int(input('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                           '1.容易\n'
                                           '2.一般\n'
                                           '3.困难\n'
                                           '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                           '请输入要生成的测试题的难易级别（1-3）,输入‘0’退出程序：'))
            if 0 < input_level_number < 4:
                return input_level_number
            if input_level_number == 0:
                exit()
        except ValueError:
            pass


def input_test_number(len_list):
    """输入指定范围内要检测英语单词的数量"""
    while True:
        """正确输入对应序号后退出循环"""
        try:
            input_words_number = int(input('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                           '请输入要测试单词的数量(1-{}),输入‘0’退出程序：'.format(len_list)))
            if 0 < input_words_number <= len_list:
                return input_words_number
            if input_words_number == 0:
                exit()
        except ValueError:
            pass


print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
      '软件名称：小学英语单词检测题生成器\n'
      '实现功能：按照难易级别随机将选定数量单词的字母用下划线替换，答题者补充完整，从而达到巩固记忆的目的\n'
      '软件作者：野生的我\n'
      '作者微信：(ID) youandpython\n'
      '作者公号：(ID) pythonic__life\n'
      '开发环境：Python 3.7 + PyCharm 2020.1 + Win10/64\n'
      '运行环境：Win7、Win10/32/64\n'
      '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')


# 单词关联的源文件与对应序号放入字典中
dic_words_book = {
    1: 'THIRD_GRADE_A.txt',
    2: 'THIRD_GRADE_B.txt',
    3: 'FOURTH_GRADE_A.txt',
    4: 'FOURTH_GRADE_B.txt',
    5: 'FIFTH_GRADE_A.txt',
    6: 'FIFTH_GRADE_B.txt',
    7: 'SIXTH_GRADE_A.txt',
    8: 'SIXTH_GRADE_B.txt',
    9: 'ALL_BOOKS',
    10: 'MANUAL_FILE'}

dic_level = {1: '简单', 2: '一般', 3: '困难'}  # level与对应序号放入字典中


while True:
    """本while循环：调用自定义函数，根据不同触发条件，完成相应需求，并格式化输出到屏幕和文件"""
    serial_number = input_book_serial()  # 调用自定义函数，返回单词范围对应的序号
    level = input_level_serial()  # 调用自定义函数，返回难度level

    list_words = []  # 初始化盛放相应范围内的单词的列表
    if serial_number == 10:
        while True:
            """手动输入英文单词文件"""
            manual_filename = input('+++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                    '请输入要要测试的单词所在的文件名称，输入‘0’退出程序：')
            if os.path.exists(manual_filename):
                """如果手动输入的文件存在，则执行文件读操作"""
                with open(manual_filename, 'r', encoding='gbk') as manual_file:
                    list_words = manual_file.readlines()  # 将手动输入的文件的内容放入列表中
                    break
            if manual_filename == str(0):
                exit()
    else:
        """下面5行代码：根据单词范围对应的序号，分别进行不同的文件读操作"""
        list_range_start = 1 if serial_number == 9 else serial_number
        list_range_end = 8 if serial_number == 9 else serial_number
        for item in range(list_range_start, list_range_end + 1):
            with open(dic_words_book[item], 'r', encoding='gbk') as source_file:
                list_words.extend(source_file.readlines())  # 将文件内容放入列表中

    output_words_number = input_test_number(len(list_words))  # 调用自定义函数，返回要检测英语单词（含中文翻译）的数量
    random_list_words = random.sample(list_words, output_words_number)  # 随机从相应单词列表中选取对应数量的单词（含中文翻译）

    """下面四行，格式化文件名"""
    time_now = time.strftime('%m-%d %H-%M-%S', time.localtime())
    str_filename = '{}_{}_{}个单词'.format(dic_words_book[serial_number][:-4], dic_level[level], output_words_number) + '.txt'
    test_filename = time_now + '_题目_' + str_filename
    answer_filename = time_now + '_答案_' + str_filename

    counter = 0  # 计数器，用于输出的每行前的序号
    for line in random_list_words:
        """遍历前面生成的单词（含中文翻译）列表，分离中文翻译和英文内容，调用自定义函数对英文进行处理，将结果格式化输出到屏幕和文件"""
        try:  # 捕获IndexError异常
            english = line.split('\t')[0].strip()  # 从列表内每行中英文混合内容中提取英文内容
            chinese = line.split('\t')[1].strip()  # 从列表内每行中英文混合内容中提取中文翻译内容
            output_path = 'output\\'
            if not os.path.exists(output_path):  # 如果不存在用于存放输出文件的’output‘文件夹，则创建
                os.makedirs(output_path)
            with open(output_path + test_filename, 'a', encoding='utf-8') as test_file, open(output_path + answer_filename, 'a', encoding='utf-8') as answer_file:
                tuple_test_and_answer = str_to_test(english, level)  # 调用自定义函数，对英文字符串进行处理
                counter += 1
                counter_str = str(counter).rjust(2) + '、 '  # 格式化序号
                print(counter_str + chinese + '\t' + tuple_test_and_answer[0])  # 格式化输出到屏幕
                test_file.write(counter_str + chinese + '\t' + tuple_test_and_answer[0] + '\n')  # 格式化写入对应文件
                answer_file.write(counter_str + tuple_test_and_answer[1] + '\n')  # 格式化写入对应文件
        except IndexError:
            pass

    """下面6行代码，格式化输出相关信息到屏幕"""
    print('\n\n' + '='*100
          + '\n题目和答案文件已生成完毕，您可到当前目录打开output文件夹进行查看，建议将内容复制到word中，用四号字打印，效果不错。'
          + '\n\n单词源文件是： {}'.format(dic_words_book[serial_number])
          + '\n单词目标文件（题目）是： {}\n单词目标文件（答案）是： {}'.format(test_filename, answer_filename)
          + '\n\n生成时间： {}\n难易程序： {}\n题目数量： {}'.format(time_now, dic_level[level], output_words_number)
          + '\n' + '='*100)

    """下面代码，显示9秒倒计时"""
    for i in range(9, 0, -1):
        print('\r{} 秒后重新进入测试题文件生成模式！'.format(i), end='')
        time.sleep(1)

