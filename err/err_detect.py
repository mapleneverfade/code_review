#-*- utf-8 -*-
import re
import sys
from .err_define import error_define
'''
    code review异常检测。
'''
class error_detect():
    def __init__(self):
        self.isRight = True
        self._statement = []
        self._field = []
        self.global_exception ={              #统计全局错误
                'select *':                  0,
                'create multi-table':      0,
                'drop table':               0,
                'insert target':           0,
                'flag_distinct':         False
        }
        self.local_table_name = {}           #记录目标表名与写入次数。
        self.local_exception = {}
        self.target_table_statement = []     #记录包含目标表的语句，后续处理。
        self.err = error_define()

    def get_statement(self, statement):
        self._statement = statement

    def get_field(self, field):
        self._field = field

    def global_exception_detect(self):   #检测全局异常
        for i in self._statement:
            #select, create, drop, table_name, flag_distinct = detect_keyword(i)
            select, create, drop, table_name, flag_distinct = self.detect_keyword(i)
            self.global_exception['select *']                += select
            self.global_exception['create multi-table']    += create
            self.global_exception['drop table']             += drop
            if flag_distinct:
                self.global_exception['flag_distinct']      = True

            if table_name and not table_name.startswith('tmp'):          #统计目标表数与写入次数。
                if table_name not in self.local_table_name:
                    self.target_table_statement.append(i)                  #记录插入目标表语句，后续处理。
                    self.local_table_name[table_name] = 1
                else:
                    self.local_table_name[table_name] += 1

    def detect_keyword(self, sql):  # 针对单语句正则匹配相应关键字。
        select_pattern = 'select\s*\\*'  # 正则匹配模式
        create_pattern = 'create'
        drop_pattern = 'drop'
        distinct_pattern = 'distinct'
        flag_distinct = False

        result_select = re.findall(select_pattern, sql, re.IGNORECASE)  # 匹配 'select'
        result_create = re.findall(create_pattern, sql, re.IGNORECASE)  # 匹配 'create'
        result_drop = re.findall(drop_pattern, sql, re.IGNORECASE)      # 匹配 'drop'

        if len(re.findall(distinct_pattern, sql, re.IGNORECASE)) > 3:  # 对于distinct关键字的检测，以flag_distinct为标志。
            flag_distinct = True
        #tmp_table = extract_table_name(sql)
        tmp_table = self.extract_table_name(sql)
        return len(result_select), len(result_create), len(result_drop), tmp_table, flag_distinct

    def extract_table_name(self, sql):
        pattern = '(?<=insert into ).*?(?=\()'  # 提取表名，前向界定、后向界定、懒惰匹配。
        result = re.findall(pattern, sql.lower(), re.DOTALL)
        if len(result) > 0:
            return result[0]  # 返回表名
        else:
            return False


    #清除err_detector结果，扫描下一个文件。
    def clear(self):
        self.isRight = True
        self._statement = []
        self._field = []
        self.global_exception = {  # 统计全局错误
            'select *': 0,
            'create multi-table': 0,
            'drop table': 0,
            'insert target': 0,
            'flag_distinct': False
        }
        self.local_table_name = {}  # 记录目标表名与写入次数。
        self.local_exception = {}
        self.target_table_statement = []  # 记录包含目标表的语句，后续处理。

    def setWrong(self):
        self.isRight = False

    #输出异常检测结果
    def print_exception(self):
        if self.global_exception['select *'] > 0:
            self.err.select_error()
            self.setWrong()
        if self.global_exception['create multi-table'] > 2:
            self.err.multi_temp_table_error()
            self.setWrong()
        if self.global_exception['create multi-table']>=2 and self.global_exception['drop table']==0:
            self.err.no_drop_error()
            self.setWrong()
        sort_table = sorted(self.local_table_name.items(), key=lambda x: x[1], reverse=True)

        if len(self.local_table_name)>1:
            self.err.multi_target_error()
            self.setWrong()

        try :
            if sort_table[0][1]>1:
                self.err.multi_write_error()
                self.setWrong()
        except IndexError as i:
            print('No target table!')

        if self.global_exception['flag_distinct']:
            self.err.over_distinct_error()
            self.setWrong()

        if self.isRight:
            print('     扫描完毕，未发现错误！')

