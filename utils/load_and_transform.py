#-*- coding:utf-8 -*-
import re
'''
    导入与分割SQL文本。
    split_to_statement() 实现语句分割 ';'
    cut_sub() 实现 , 号分割 ','
'''
# @property 控制读写
class load_sql():
    def __init__(self):
        self._sql = ''                              # 原SQL脚本
        self._sql_no_note = ''
        self._statement = []                        #分割后的所有语句

    def load_sql_origin(self, filepath):             #导入SQL文本，不做处理。
        self._sql = ''                              #字符串置空。
        with open(filepath, 'rb') as f:
            for line in f:
                self._sql = f"{self._sql} {line.decode('utf8').strip()}"
        if not self._sql:
            raise(Exception('loading error!'))   # 导入SQL脚本异常。
        return self._sql

    def load_delete_note(self, filepath):
        self._sql_no_note = ''
        with open(filepath, 'rb') as f:
            for line in f:
                pattern = '--.*?\n'                #懒惰匹配注释
                i = re.sub(pattern, '', line.decode('utf8','ignore'))
                self._sql_no_note = f'{self._sql_no_note} {i.strip()}'
        if not self._sql_no_note:
            raise(Exception('loading error!'))   # 导入SQL脚本异常。
        return self._sql_no_note

    def split_to_statement(self):                   # 文本划分为语句。
        self._statement = self._sql.split(';')

    def split_to_field(self):                       # ToDo 语句划分为字段。
        pass

    @property
    def sql(self):
        return self._sql

    @property
    def statement(self):
        return self._statement



