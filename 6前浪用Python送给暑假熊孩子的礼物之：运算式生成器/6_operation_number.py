# -*- coding: utf-8 -*-
import random


def generate_two_random_numbers(digit_number):
    """生成两个不超过最高位数的随机数"""
    return random.randint(2, 10**digit_number - 1), random.randint(2, 10**digit_number - 1)


def two_numbers_expression_result(num_x, num_y, operator):
    """求两个数对应运算的结果"""
    if operator == '+':
        return num_x + num_y
    elif operator == '-':
        return 0 if num_x - num_y < 1 else num_x - num_y  # 如果差为负数，函数值返回0
    elif operator == '*':
        return num_x * num_y
    elif operator == '/':
        return 0 if (num_x % num_y != 0) or (num_x == num_y) else num_x / num_y  # 如果不能整除或者两数相等，函数值返回0


counter_file = 0  # 生成文件的计数器
# 字典中每个序号对应不同运算符的运算式
dic_serial_number_for_operation = {
    0: '二运算数加法',
    1: '二运算数减法',
    2: '二运算数乘法',
    3: '二运算数除法',
    4: '二运算数加减法',
    5: '二运算数乘除法',
    6: '二运算数加减乘除法'}
while True:
    while True:
        """正确输入对应序号后退出循环"""
        try:
            serial_number = int(input(
                '\n'
                '*****************************************************\n'
                '0.生成两个运算数的加法运算\n'
                '1.生成两个运算数的减法运算\n'
                '2.生成两个运算数的乘法运算\n'
                '3.生成两个运算数的除法运算\n'
                '4.生成两个运算数的随机加减运算\n'
                '5.生成两个运算数的随机乘除运算\n'
                '6.生成两个运算数的随机加减乘除运算\n'
                '*****************************************************\n'
                '请根据以上需求输入相应的序号，输入‘19’退出程序：'))
            if (serial_number >= 0) and (serial_number <= 6):
                break
            if serial_number == 19:
                exit()
        except ValueError:
            pass

    while True:
        """正确输入对应序号后退出循环"""
        try:
            digit = int(input('*****************************************************\n'
                              '请输入要生成的运算数的最高位数（不超过四位）：'))
            if (digit > 0) and (digit < 5):
                break
        except ValueError:
            pass

    while True:
        """正确输入对应序号后退出循环"""
        try:
            output_expressions_number = int(input('*****************************************************\n'
                                                  '请输入要生成的运算式的数量(最好不超过一万道)：'))
            if (output_expressions_number > 0) and (output_expressions_number <= 10000):
                break
        except ValueError:
            pass

    dic_operator = {0: '+', 1: '-', 2: '*', 3: '/'}  # 与上面序号对应的运算符，放在字典中

    expression_counter = 1  # 要输出的运算式计数器初始化为1
    dic_key = serial_number  # 初始化运算符对应的序号
    dic_operator_counter = {0: 0, 1: 0, 2: 0, 3: 0}  # 各运算符计数器初始化为0，放在字典中
    while expression_counter <= output_expressions_number:  # 要输出的运算式计数器没达到用户输入值的时候一直循环
        """根据不同序号代表的运算式需求，生成符合条件的运算式"""
        num_a, num_b = generate_two_random_numbers(digit)  # 调用自定义函数，生成两个随机数

        if serial_number == 4:
            """按要求随机产生加减运算符"""
            dic_key = random.randint(0, 1)
            dic_key = 1 if dic_operator_counter[0] > dic_operator_counter[1] else 0  # 均衡随机产生不同运算符
        elif serial_number == 5:
            """按要求随机产生乘除运算符"""
            dic_key = random.randint(2, 3)
            dic_key = 3 if dic_operator_counter[2] > dic_operator_counter[3] else 2  # 均衡随机产生不同运算符
        elif serial_number == 6:
            """按要求随机产生加减乘除运算符"""
            dic_key = min(dic_operator_counter, key=dic_operator_counter.get)  # 均衡随机产生不同运算符

        result = int(two_numbers_expression_result(num_a, num_b, dic_operator.get(dic_key)))  # 调用自定义函数，求运算式的运算结果
        if not result:  # 如果上面运算式的结果result为0，则直接跳到下次循环
            continue

        dic_operator_counter[dic_key] += 1  # 对随机产生的运算符进行计数，更新到字典中
        print(f'{num_a:4}', dic_operator.get(dic_key), f'{num_b:4}', '=', f'{result:8}', end='    ')  # 将运算式格式化输出到屏幕
        if expression_counter % 3 == 0:
            """每行输出3个运算式"""
            print('')

        """下面三行，格式化文件名"""
        expression_filename = '{}_{}_最高位数{}_{}道'.format(counter_file, dic_serial_number_for_operation[serial_number], digit, output_expressions_number)
        expression_filename += '.txt'
        answer_filename = '答案_' + expression_filename
        with open(expression_filename, 'a', encoding='utf-8') as expression_file, open(answer_filename, 'a', encoding='utf-8') as answer_file:
            """将无答案运算式和答案，分别格式化写入不同文件中"""
            # 格式化要写入文件的内容
            expression = str(num_a).rjust(digit) + dic_operator.get(dic_key).rjust(2) + str(num_b).rjust(digit + 1) + '='.rjust(2)
            expression_file.write(expression + ' ' * 10)  # 写入格式化内容到文件
            answer_file.write(str(result).rjust(8) + ',' + '\t\t')  # 写入格式化内容到文件
            if expression_counter % 3 == 0:
                """每行写入3个运算式或答案"""
                expression_file.write('\n')
                answer_file.write('\n')

        expression_counter += 1  # 要输出的运算式计数

    """下面，格式化输出相关信息"""
    print('\n\n' + '='*116)
    print('{}道最高位数是{}的{}运算式已生成完毕，您可到当前目录查看文件，内容复制到word中用四号字打印效果最佳哟。'.format(output_expressions_number, digit, dic_serial_number_for_operation[serial_number]))
    print('其中：加法{}道、减法{}道、乘法{}道、除法{}道。'.format(dic_operator_counter[0], dic_operator_counter[1], dic_operator_counter[2], dic_operator_counter[3]))
    print('='*116)

    counter_file += 1  # 计数器，用于文件的命名
