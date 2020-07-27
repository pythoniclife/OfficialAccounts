# -*- coding: utf-8 -*-
# 本次案例，其实是两个相对独立的小案例的叠加。本身完全是可以作为两篇原创案例文章出现的，为了和前期的数学、英语案例保持一致，所以选择了将二者整合在一起发布
# Idiom和Poem两个类有些方法是重叠的，有些臃肿，目的是为了方便后期的移植和拆分。
# 为了方便阅读，也未将两个类作为单独模块存在，而是一个py文件到底。

import re
import os
import math
import time
import random


class Idiom:
    """对成语源文件读入后，对原始数据进行清洗、格式化，放入字典。然后根据不同的用户输入需求（题目的范围、难度、数量）进行逻辑处理，最后格式化输出到屏幕和文件"""

    def __init__(self, filename):
        # self.screen_start_info()  # 单独移植出去的话，这行代码可以保留，作为程序运行时的屏幕提示信息，增强用户体验
        self.filename = filename  # 接收源文件名
        self.output_dir = 'output\\idiom\\'  # 用于存放目标文件的路径
        self.dic_idiom_key_is_grade = {}  # 初始化存放所有数据的字典

        self.which_book = self.input_serial_get_book()  # 接收表示成语范围的序号
        self.how_level = self.input_level_serial()  # 接收表示难易程序的序号
        if self.which_book == '全册':
            """根据序号（键）对应的关键字（值），决定生成成语检测题的数量"""
            self.how_many = self.input_test_number(sum([len(v) for v in self.file_to_dic().values()]))  # 遍历所有成语句子，将各数量求和
        else:
            self.how_many = self.input_test_number(len(self.file_to_dic()[self.which_book]))  # 返回某个范围的成语句子数量

        """下面4行，对存放输出内容的文件的文件名进行预格式化"""
        self.time_now = time.strftime('%y-%m-%d %H-%M-%S', time.localtime())  # 当前时间
        self.part_filename = '{}_{}_{}道'.format(self.which_book, {1: '简单(有释义)', 2: '一般(有释义)', 3: '困难(有释义)', 4: '简单(无释义)', 5: '一般(无释义)', 6: '困难(无释义)'}.get(self.how_level), self.how_many) + '.txt'
        self.question_filename = self.time_now + '_成语检测题_' + self.part_filename
        self.answer_filename = self.time_now + '_答案_' + self.part_filename

    @staticmethod
    def screen_start_info():
        """程序运行时的屏幕提示信息，增强用户体验"""
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
              '软件名称：小学语文成语、古诗词抽测题生成器\n'
              '实现功能：根据给定的难易级别随机选定部分内容变成空白，答题者补充完整，从而达到巩固记忆的目的\n'
              '软件作者：野生的我\n'
              '作者微信：(ID) youandpython\n'
              '作者公号：(ID) pythonic__life\n'
              '开发环境：Python 3.7 + PyCharm 2020.1 + Win10/64\n'
              '运行环境：Win7、Win10/32/64\n'
              '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')

    @staticmethod
    def input_serial_get_book():
        """输入要检测的成语的课本范围对应的序号"""
        dic_serial_and_book = {1: '一年级', 2: '二年级', 3: '三年级', 4: '四年级', 5: '五年级', 6: '六年级', 7: '全册'}

        while True:
            """正确输入对应序号后退出循环"""
            try:
                input_serial_number = int(input(
                    '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                    '1.小学一年级\n'
                    '2.小学二年级\n'
                    '3.小学三年级\n'
                    '4.小学四年级\n'
                    '5.小学五年级\n'
                    '6.小学六年级\n'
                    '7.小学一到六年级全册\n'
                    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                    '请输入要考查记忆的成语所在课本范围对应的序号，输入‘0’退出程序：'))

                if 1 <= input_serial_number <= 7:
                    return dic_serial_and_book[input_serial_number]
                if input_serial_number == 0:
                    exit()
            except ValueError:
                pass

    @staticmethod
    def input_level_serial():
        """输入检测难度对应的序号"""
        while True:
            """正确输入对应序号后退出循环"""
            try:
                input_level_number = int(input('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                               '1.容易（带成语释义）\n'
                                               '2.一般（带成语释义）\n'
                                               '3.困难（带成语释义）\n'
                                               '4.容易（不带成语释义）\n'
                                               '5.一般（不带成语释义）\n'
                                               '6.困难（不带成语释义）\n'                                               
                                               '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                               '请输入要生成的测试题的难易级别（1-6）,输入‘0’退出程序：'))
                if 0 < input_level_number < 7:
                    return input_level_number
                if input_level_number == 0:
                    exit()
            except ValueError:
                pass

    @staticmethod
    def input_test_number(len_list):
        """输入指定范围内要检测成语的数量"""
        while True:
            """正确输入对应序号后退出循环"""
            try:
                input_words_number = int(input('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                               '请输入要检测的成语的数量(1-{}),输入‘0’退出程序：\n'.format(len_list)))
                if 0 < input_words_number <= len_list:
                    return input_words_number
                if input_words_number == 0:
                    exit()
            except ValueError:
                pass

    @staticmethod
    def idiom_to_question_and_answer(str_data, level_data):
        """将成语（加释义）原始字符串，格式化为题目、答案，并以元组类型返回"""

        idiom_str = str_data[:4]  # 取前4个汉字（四字成语）
        level_number = level_data

        rate = level_data - 3 if level_data > 3 else level_number + 1  # 对level等级进行处理

        idiom_to_list = list(idiom_str)  # 字符串打散为列表类型
        random_list_index = random.sample(range(0, 4), rate)  # 随机抽取列表索引，放在列表中

        answer_str = ''  # 初始化答案变量
        for index in sorted(random_list_index):  # 遍历排序后的存放随机抽取的列表索引的列表
            """格式化输出的内容"""
            answer_str += idiom_to_list[index] + ','
            idiom_to_list[index] = '（   ）'

        list_to_idiom = ''.join(idiom_to_list)  # 列表转换为字符串

        if level_data > 3:  # 针对level级别对输出结果进行相应处理
            return list_to_idiom, answer_str.strip()[:-1]  # [：-1]是去掉末尾标点符号（逗号）

        return list_to_idiom + str_data[4:], answer_str.strip()[:-1]  # 针对level级别对输出结果进行相应处理

    def file_to_dic(self):
        """将原始文件读入，对脏数据进行清洗、格式化处理，以字典类型返回函数值"""

        with open(self.filename, 'r', encoding='gbk') as read_file:
            for line in read_file.readlines():
                """对源文件进行遍历，动态生成包含格式化数据的字典"""

                if '年级' in line:
                    key = line.strip()
                    self.dic_idiom_key_is_grade[key] = []
                    continue
                if '：' in line:
                    self.dic_idiom_key_is_grade[key].append(line.strip())
        return self.dic_idiom_key_is_grade

    def output_to_screen_and_file(self):
        """基于上面file_to_dic()方法动态生成的放有格式化数据的字典，根据用户需求进行逻辑处理，最后格式化输出到屏幕和文件中"""

        if self.which_book == '全册':
            """如果成语范围选定为’全册‘，则将字典的键（各年级）对应的值（成语句子列表）进行遍历，并再分别遍历每个列表（包含各年级成语句子的），达到降维目的"""
            idiom_list = [index for v in self.dic_idiom_key_is_grade.values() for index in v]
        else:
            idiom_list = self.dic_idiom_key_is_grade[self.which_book]  # 将年级对应的各成语句子放入列表

        random_list_index = random.sample(range(len(idiom_list)), self.how_many)  # 根据要生成的题目数量，对每个成语句子对应的索引值进行随机抽取，放入列表

        serial_counter = 0  # 输出题目的序号变量，初始化为0
        for index in sorted(random_list_index):
            """遍历排序后的存放随机抽取的列表索引的列表，将索引对应的成语句子进行清洗、格式化，输出到屏幕和文件"""

            serial_counter += 1  # 用于题目前的序号

            clean_sentence = re.sub(r'[0-9]\.?', '', idiom_list[index])  # 清洗掉成语句子前面的数字和实心句点
            result = self.idiom_to_question_and_answer(clean_sentence.strip(), self.how_level)  # 调用上面方法，返回题干和答案
            print('\n' + str(serial_counter) + '、' + result[0])  # 上面方法返回值是元组，所以要切片
            print('答案：' + result[1])

            if not os.path.exists(self.output_dir):  # 如果不存在用于存放输出文件的’output\idiom‘文件夹，则创建
                os.makedirs(self.output_dir)

            with open(self.output_dir + self.question_filename, 'a', encoding='utf-8') as question_file, open(self.output_dir + self.answer_filename, 'a', encoding='utf-8') as answer_file:

                question_file.write(str(serial_counter) + '、' + result[0] + '\n')  # 将输出内容格式化写入文件中
                answer_file.write(str(serial_counter) + '、' + result[1] + '\t\t')
                if serial_counter % 3 == 0:  # 如果一行内写满三次，则换行
                    answer_file.write('\n')

    def screen_end_info(self):
        """格式化输出相关信息到屏幕"""
        print('\n\n' + '#' * 120
              + '\n恭喜你！成语检测题和答案文件已生成完毕，您可到当前目录打开output文件夹进行查看，建议将内容复制到word中，居中、四号字打印，效果不错。'
              + '\n\n古诗词源文件是： {}'.format(self.filename)
              + '\n检测题目标文件是： {}\n答案目标文件是： {}'.format(self.question_filename, self.answer_filename)
              + '\n\n题目范围： {}\n生成时间： {}\n难易程序： {}\n题目数量： {}'.format(self.which_book, self.time_now, self.how_level, self.how_many)
              + '\n' + '#' * 120)

    @staticmethod
    def timer():
        """显示10秒倒计时"""
        for i in range(10, 0, -1):
            print('\rWarning！如果您不关闭程序，{} 秒后重新进入检测题文件生成模式！'.format(i), end='')
            time.sleep(1)
        print('\n')


class Poem:
    """对古诗词源文件读入后，对原始数据进行清洗、格式化，放入字典。然后根据不同的用户输入需求（题目的范围、难度、数量）进行逻辑处理，最后格式化输出到屏幕和文件"""

    def __init__(self, filename):
        # self.screen_start_info()  # 这个类单独移植出去的话，这行代码可以保留，作为程序运行时的屏幕提示信息，增强用户体验
        self.filename = filename # 接收源文件名
        self.output_dir = 'output\\poem\\'  # 用于存放目标文件的路径
        self.clean_file_to_list = self.clean_file_to_list()  # 接收清洗函数返回的去掉杂质的数据
        self.dic_poem_key_is_grade = {}  # 初始化存放所有数据的字典

        self.which_book = self.input_serial_get_book()  # 接收表示古诗词范围的序号
        self.how_level = self.input_level_serial()  # 接收表示难易程序的序号
        if self.which_book == '全册':
            """根据序号（键）对应的关键字（值），决定生成古诗词检测题的数量"""
            self.how_many = self.input_test_number(sum([len(v) for v in self.file_to_dic().values()]))  # 遍历所有古诗词，将各数量求和
        else:
            self.how_many = self.input_test_number(len(self.file_to_dic()[self.which_book]))  # 返回某个范围的古诗词数量

        """下面4行，对存放输出内容的文件的文件名进行预格式化"""
        self.time_now = time.strftime('%y-%m-%d %H-%M-%S', time.localtime())
        self.part_filename = '{}_{}_{}道古诗词题'.format(self.which_book, {1: '简单', 2: '一般', 3: '困难'}.get(self.how_level), self.how_many) + '.txt'
        self.question_filename = self.time_now + '_古诗词检测题_' + self.part_filename
        self.answer_filename = self.time_now + '_答案_' + self.part_filename

    @staticmethod
    def screen_start_info():
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
              '软件名称：小学语文成语、古诗词抽测题生成器\n'
              '实现功能：根据设置的难易级别将选定部分内容随机变成空白，答题者补充完整，从而达到巩固记忆的目的\n'
              '软件作者：野生的我\n'
              '作者微信：(ID) youandpython\n'
              '作者公号：(ID) pythonic__life\n'
              '开发环境：Python 3.7 + PyCharm 2020.1 + Win10/64\n'
              '运行环境：Win7、Win10/32/64\n'
              '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')

    def clean_file_to_list(self):
        """对源文件中的脏数据进行初步清洗（只保留包含汉字的行）"""
        with open(self.filename, 'r', encoding='gbk') as read_file:
            return [item for item in read_file.readlines() if self.is_chinese(item)]  # 调用is_chinese方法，返回所有含有汉字的行

    @staticmethod
    def input_serial_get_book():
        """输入要检测的古诗词的课本范围对应的序号"""
        dic_serial_and_book = {
            1: '一年级上册',
            2: '一年级下册',
            3: '二年级上册',
            4: '二年级下册',
            5: '三年级上册',
            6: '三年级下册',
            7: '四年级上册',
            8: '四年级下册',
            9: '五年级上册',
            10: '五年级下册',
            11: '六年级上册',
            12: '六年级下册',
            13: '全册'}

        while True:
            """正确输入对应序号后退出循环"""
            try:
                input_serial_number = int(input(
                    '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                    '1.小学一年级上册\n'
                    '2.小学一年级下册\n'
                    '3.小学二年级上册\n'
                    '4.小学二年级下册\n'
                    '5.小学三年级上册\n'
                    '6.小学三年级下册\n'
                    '7.小学四年级上册\n'
                    '8.小学四年级下册\n'
                    '9.小学五年级上册\n'
                    '10.小学五年级下册\n'
                    '11.小学六年级上册\n'
                    '12.小学六年级下册\n'
                    '13.小学一至六年级全册\n'
                    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                    '请输入要考查记忆的古诗词所在课本范围对应的序号，输入‘0’退出程序：'))

                if 1 <= input_serial_number <= 13:
                    return dic_serial_and_book[input_serial_number]
                if input_serial_number == 0:
                    exit()
            except ValueError:
                pass

    @staticmethod
    def input_level_serial():
        """输入检测难度对应的序号"""
        while True:
            """正确输入对应序号后退出循环"""
            try:
                input_level_serial = int(input('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                               '1.容易\n'
                                               '2.一般\n'
                                               '3.困难\n'
                                               '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                               '请输入要生成的测试题的难易级别（1-3）,输入‘0’退出程序：'))
                if 0 < input_level_serial < 4:
                    return input_level_serial
                if input_level_serial == 0:
                    exit()
            except ValueError:
                pass

    @staticmethod
    def input_test_number(len_list):
        """输入指定范围内要检测古诗词的数量"""
        while True:
            """正确输入对应序号后退出循环"""
            try:
                input_words_number = int(input('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
                                               '请输入要检测的古诗词的数量(1-{}),输入‘0’退出程序：\n'.format(len_list)))
                if 0 < input_words_number <= len_list:
                    return input_words_number
                if input_words_number == 0:
                    exit()
            except ValueError:
                pass

    @staticmethod
    def poem_to_question_and_answer(list_data, level_data):
        """读取存有古诗词的原始列表，进行逻辑处理，格式化为题目、答案，并以元组类型返回"""

        if list_data is []:
            return None

        rate = level_data / 3  # 对level等级进行处理
        # 随机抽取列表索引，放在列表中，将level关联的预随机抽取的索引数量进行收尾取整处理
        random_list_index = random.sample(range(len(list_data)), math.ceil(len(list_data) * rate))

        answer_str = '答案：'  # 初始化答案变量
        for random_index in sorted(random_list_index):  # 遍历排序后的存放随机抽取的列表索引的列表
            """格式化输出的内容"""
            answer_str += list_data[random_index] + ' '
            list_data[random_index] = '_' * 26 + list_data[random_index][-1:]  # 将原始汉字用 ‘_’代替，通过切片保留末尾标点符号

        list_to_str = ''  # 初始化题干变量
        i = 0
        for list_index in list_data:
            """遍历存放题干和答案的列表，进行格式化处理后，将题干和答案转成字符串类型"""
            i += 1
            if i % 2 == 0:  # 一行显示两句诗词
                list_index += '\n'
            list_to_str += list_index

        if i % 2 == 1:  # 末尾新增一个空行，增强用户体验
            answer_str = '\n' + answer_str
        return list_to_str, answer_str

    @staticmethod
    def is_punctuation(line_data):
        """判断字符串中是否含有以下4种中文标点符号"""
        for char in line_data.strip():
            if char in ['，', '。', '！', '？']:
                return True
        return False

    @staticmethod
    def is_chinese(line_data):
        """判断字符串中是否含有汉字"""
        chinese_word_list = re.findall(r'[\u4e00-\u9fa5]', line_data.strip())

        if chinese_word_list:
            return True
        else:
            return False

    def file_to_dic(self):
        """读入已被初步清洗的以列表类型存在的数据，进行格式化处理，以字典类型返回函数值"""

        list_poem = self.clean_file_to_list  # 接收初步清洗后的数据
        key_title = None
        key_grade = None
        for index in range(len(list_poem)):
            """对初步清洗后的列表数据进行遍历，动态生成包含格式化数据的字典"""

            if '年级' in list_poem[index]:
                """动态添加字典的键值对"""
                key_grade = list_poem[index].strip()
                self.dic_poem_key_is_grade[key_grade] = {}
                continue

            if (not self.is_punctuation(list_poem[index])) and (not self.is_punctuation(list_poem[index+1])):
                """如果当前行没有4种标点符号并且下一行也没有4种标点符号，程序就认为这是古诗词的标题行和作者朝代行，则将此2行合并，作为字典的值的键，形成一新键值对"""
                key_title = list_poem[index].strip() + '\n' + list_poem[index + 1].strip() + '\n'  # 将标题行和作者朝代行合并，作为字典的键
                self.dic_poem_key_is_grade[key_grade][key_title] = []  # 动态生成键值对

            if self.is_punctuation(list_poem[index]):
                """如果当前行包含符合规则的汉字和标点符号组合，则添加到字典的值中"""
                split_element_to_list = re.findall(r'[\u4e00-\u9fa5]*[，？！。]', list_poem[index].strip())  # 返回符合规则的内容
                self.dic_poem_key_is_grade[key_grade][key_title].extend(split_element_to_list)  # 添加到以列表类型存在的字典值中

        return self.dic_poem_key_is_grade  # 返回格式化后的字典类型的数据

    def output_to_screen_and_file(self):
        """基于上面file_to_dic()方法动态生成的放有格式化数据的字典，根据用户需求进行逻辑处理，最后格式化输出到屏幕和文件中"""

        if self.which_book == '全册':
            """如果古诗词范围选定为’全册‘，则遍历字典的值，并再分别遍历每个值中的键值对，降维，将全册所有古诗词放入一维列表中"""
            poem_dic_to_list = [index for v in self.dic_poem_key_is_grade.values() for index in v.items()]
        else:
            poem_dic_to_list = list(self.dic_poem_key_is_grade[self.which_book].items())  # 将某年级对应的所有古诗词放入列表中

        # 根据要生成的题目数量，对每个古诗词对应的索引值进行随机抽取，放入列表
        random_list_index = random.sample(range(len(poem_dic_to_list)), self.how_many)

        serial_counter = 0  # 输出题目的序号变量，初始化为0
        for index in sorted(random_list_index):
            """遍历排序后的存放随机抽取的列表索引的列表，将索引对应的古诗词进行清洗、格式化，输出到屏幕和文件"""

            serial_counter += 1  # 用于题目前的序号

            result = self.poem_to_question_and_answer(poem_dic_to_list[index][1], self.how_level)  # 调用上面方法，返回题干和答案
            print(str(serial_counter) + '\n' + poem_dic_to_list[index][0])  # 这里先输出古诗词的标题和作者朝代，下面一行输出诗词句子
            print(result[0])  # 上面方法返回值是元组，所以要切片

            print(result[1] + '\n')

            if not os.path.exists(self.output_dir):  # 如果不存在用于存放输出文件的’output\poem‘文件夹，则创建
                os.makedirs(self.output_dir)

            with open(self.output_dir + self.question_filename, 'a', encoding='utf-8') as question_file, open(self.output_dir + self.answer_filename, 'a', encoding='utf-8') as answer_file:

                question_file.write(str(serial_counter) + '\n' + poem_dic_to_list[index][0])  # 将输出内容格式化写入文件中
                question_file.write(result[0] + '\n')

                answer_file.write(str(serial_counter) + '、' + result[1].strip() + '\n')

    def screen_end_info(self):
        """格式化输出相关信息到屏幕"""
        print('\n\n' + '#' * 120
              + '\n恭喜你！古诗词检测题和答案文件已生成完毕，您可到当前目录打开output文件夹进行查看，建议将内容复制到word中，居中、四号字打印，效果不错。'
              + '\n\n古诗词源文件是： {}'.format(self.filename)
              + '\n检测题目标文件是： {}\n答案目标文件是： {}'.format(self.question_filename, self.answer_filename)
              + '\n\n题目范围： {}\n生成时间： {}\n难易程序： {}\n题目数量： {}'.format(self.which_book, self.time_now, self.how_level, self.how_many)
              + '\n' + '#' * 120)

    @staticmethod
    def timer():
        """显示10秒倒计时"""
        for i in range(10, 0, -1):
            print('\rWarning！如果您不关闭程序，{} 秒后重新进入检测题文件生成模式！'.format(i), end='')
            time.sleep(1)
        print('\n')


while True:
    """输入对应序号进入相应内容生成模式，输入‘0’退出程序"""
    Idiom.screen_start_info()  # 程序运行时的屏幕提示信息，增强用户体验。这里也可以调用Poem类的具备同样功能的方法
    try:
        input_level_number = int(input('\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
                                       '1.随机生成成语抽测题\n'
                                       '2.随机生成古诗词抽测题\n'
                                       '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
                                       '请输入要生成的测试题对应的序号（1-2）, 输入‘0’退出程序：'))
        if 0 < input_level_number < 3:
            if input_level_number == 1:
                """序号1调用Idiom类"""
                print('\n下面进入成语检测题生成模式：')
                idiom = Idiom('idiom.txt')  # 实例化对象
                idiom.output_to_screen_and_file()  # 调用方法输出相关信息到屏幕和文件
                idiom.screen_end_info()  # 调用方法输出相关信息到屏幕
                idiom.timer()  # 调用方法进行倒计时
            if input_level_number == 2:
                """序号2调用Poem类"""
                print('\n下面进入古诗词检测题生成模式：')
                poem = Poem('poem.txt')  # 实例化对象
                poem.output_to_screen_and_file()  # 调用方法输出相关信息到屏幕和文件
                poem.screen_end_info()  # 调用方法输出相关信息到屏幕
                poem.timer()  # 调用方法进行倒计时

        if input_level_number == 0:
            exit()
    except ValueError:
        pass


