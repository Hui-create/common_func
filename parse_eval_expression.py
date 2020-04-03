# -*- coding: utf-8 -*-
"""
@Time ： 2020/4/3 9:16
@Auth ： 罗国辉
@File ：parse_eval_expression.py
@IDE ：PyCharm
"""


class EvalExpression(object):

    def __init__(self, eval_exp):
        self.eval_exp = eval_exp
        self.middle_exp = None
        self.behind_exp = None
        self.result_list = []
        self.symbol_list = []
        self.number_list = [str(i) for i in range(10)]
        self.operator = ['+', '-', '*', '/']
        self.low_priority = ['+', '-']
        self.middle_priority = ['*', '/']

    def get_char(self, high_priority, char):
        while True:
            try:
                get_char = self.symbol_list.pop()
            except IndexError:
                get_char = ''
            if get_char and get_char not in high_priority:
                self.result_list.append(get_char)
                continue
            elif char == ')' and get_char == '(':
                return
            elif char != ']' and get_char == '[':
                self.symbol_list.append(get_char)
                return
            elif not bool(get_char) or get_char in high_priority:
                return

    def judge_priority(self, char):
        """判断优先级"""
        if len(self.symbol_list) == 0:
            self.symbol_list.append(char)
            return
        high_priority = ['[', '(']
        if char in high_priority:
            self.symbol_list.append(char)
            return
        low_priority = self.low_priority
        middle_priority = self.middle_priority
        try:
            last_item = self.symbol_list[-1]
        except IndexError:
            return
        if char in low_priority:
            if last_item in low_priority or last_item in middle_priority:
                self.get_char(high_priority, char)
                self.symbol_list.append(char)
                return
            elif last_item in high_priority:
                self.symbol_list.append(char)
                return
        elif char in middle_priority:
            if last_item in low_priority or last_item in high_priority:
                self.symbol_list.append(char)
                return
            elif last_item in middle_priority:
                self.result_list.append(self.symbol_list.pop())
                self.symbol_list.append(char)
                return
        end_priority = [']', ')']
        if char in end_priority:
            self.get_char(high_priority, char)

    def to_behind(self):
        """
        将中缀表达式转为后缀表达式
        :return: 后缀表达式
        """
        temp_list = self.number_list
        eval_exp = str(self.eval_exp)
        for item in eval_exp:
            item = item.strip()
            if not item:
                continue
            if item in temp_list:
                self.result_list.append(item)
                continue
            self.judge_priority(item)
        self.get_char(['[', '('], '')
        return ' '.join(self.result_list)

    def check_length(self, char, symbol):
        """根据长度情况，判断是否需要加括号"""
        # char = '(3-2)'
        length = len(char)
        if length == 1:
            return char
        else:
            if symbol in self.low_priority:
                pass
            elif not char.startswith('(') and symbol in self.low_priority:
                pass
            elif not char.startswith('(') and symbol in self.middle_priority:
                char = '(' + char + ')'
            elif char.startswith('('):
                if length >= 3 and symbol in self.middle_priority:
                    char = '[' + char + ']'
                else:
                    pass
            # else:
            #     char = '(' + char + ')'
            return char

    def get_exp(self, data):
        """遍历列表，遇到符号，就获取符号前面的两个数字，进行组成成表达式"""
        length = len(data)
        for item in range(length):
            temp = data[item]
            if temp in self.number_list:
                continue
            elif temp in self.operator:
                symbol = data.pop(item)
                num_1 = data.pop(item - 1)
                # 获取到字符，检查是否需要加括号
                num_1 = self.check_length(num_1, symbol)
                num_2 = data.pop(item - 2)
                # 获取到字符，检查是否需要加括号
                num_2 = self.check_length(num_2, symbol)
                temp_exp = num_2 + symbol + num_1
                data.insert((item - 2), temp_exp)
                break
        return data

    def to_middle(self, behind_exp):
        """
        将后缀表达式转为中缀表达式
        :return: 中缀表达式
        """
        # 将字符串型表达式转换为列表，方便遍历使用
        behind_list = [i for i in behind_exp if bool(i.strip())]
        while True:
            # 采用递归式组装表达式
            behind_list = self.get_exp(behind_list)
            length = len(behind_list)
            if length <= 1:
                break
        return behind_list[0]


def main():
    # exp = '1+1-1+1-1'
    # exp = '(1+1-1+1)/2-(3-2)/2'
    # exp = '2*(9+6/3-5)+4'
    # exp = '2+9/3-5'
    # exp = '1+[(3-1)*(3+2)]/2'
    # exp = '1+[(3-1)*(3+2)-1]/2'
    exp = '[(3-1)*(3+2)-1]/2-(3-1)/2'
    print('原中缀表达式：', exp)
    a = EvalExpression(exp)
    behind_exp = a.to_behind()
    print('解析成的后缀表达式：', behind_exp)
    data = a.to_middle(behind_exp)
    print('解析出的中缀表达式：', data)


if __name__ == '__main__':
    main()
