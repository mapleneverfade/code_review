#-*- coding:utf-8 -*-
import sys
content = ['..\\err',  '..\\utils']
import os
import banVoc as ban
from error import *
'''
    分割文本
    cut_statement()实现语句分割 ';'
    cut_sub() 实现 , 号分割 ','
'''
# @property 控制读写
class cut_statement():
    def __init__(self):
        self._sql = ''
        self._statement = []  # 分割后的所有语句

    def load_sql(self,filepath):
        self._sql = ''                  #字符串置空。
        with open(filepath, 'rb') as f:
            for line in f:
                self._sql = '{} {}'.format(self._sql, line.decode('utf8').strip())

    def split_to_statement(self): #文本划分为语句。
        self._statement = self._sql.split(';')

    def split_to_field(self):    #语句划分为字段。
        pass

    @property
    def sql(self):
        return self._sql

    @property
    def statement(self):
        return self._statement



if __name__ == '__main__':
    filename_1 = 'D:\\项目管理\\venv\\code-review\\test\\tmp_1.sql'
    filename_2 = 'D:\\项目管理\\venv\\code-review\\test\\tmp_2.sql'

    finetuning = cut_statement()

    finetuning.load_sql(filename_1)
    finetuning.split_to_statement()

    excep = exception_detect()
    excep.get_statement(finetuning.statement)  #传入statement
    excep.global_exception_detect()            #异常检测
    excep.print_exception()                    #输出异常

    print(excep.local_table_name)

