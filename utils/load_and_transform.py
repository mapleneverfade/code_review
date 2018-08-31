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
        self._sql_no_note = ''                      # 去掉注释后脚本
        self._statement = []                        # 无注释分割后的所有语句

    @property
    def sql(self):
        return self._sql
    @sql.setter
    def sql(self,sql_):
        self._sql = sql_
    @property
    def sql_no_note(self):
        return self._sql_no_note
    @sql_no_note.setter
    def sql_no_note(self,sql_):
        self._sql_no_note = sql_

    def load_sql_origin(self, filepath):                  # 导入SQL文本，不做处理
        sql = ''                                          # 字符串置空
        with open(filepath, 'rb') as f:
            for line in f:
                sql = f"{sql} {line.decode('utf8','ignore')}"    # 不去除空白字符
        if not sql:
            raise(Exception('loading error!'))         # 导入SQL脚本异常
        self.sql = sql
        return sql

    def load_delete_note(self, filepath):
        sql_no_note = ''
        with open(filepath, 'rb') as f:
            for line in f:
                pattern = '--.*?\n'                #懒惰匹配注释
                i = re.sub(pattern, '', line.decode('utf8','ignore'))
                sql_no_note = f'{sql_no_note} {i.strip()}'
        if not sql_no_note:
            raise(Exception('loading error!'))   # 导入SQL脚本异常。
        self.sql_no_note = sql_no_note
        return sql_no_note

    def split_to_statement(self):                         # 文本划分为语句
        self._statement = self.sql.split(';')

    def split_to_field(self):                             # ToDo 语句划分为字段。
        pass

    @property
    def statement(self):
        return self._statement



