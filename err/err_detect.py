#-*- utf-8 -*-
import re
import sys
from .err_define import error_define
'''
    code review异常检测。
'''

global_exception = {                                    #统计全局错误
                'select *':                  0,
                'create multi-table':      0,
                'drop table':               0,
                'insert target':           0,
                'update target':           0,         #采用update更新目标表
                'flag_distinct':         False,
                'etl_tms'       :            0         #是否显式更新etl_tms
        }

class error_detect():
    def __init__(self):
        self.isRight = True
        self._statement = []
        self._field = []
        self.global_exception =global_exception.copy()
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

        self.detect_update_target()  #检测是否update目标表
        self.detect_implicit_etl_tms()

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

    #统计insert与update语句中出现的表名。
    '''
        不够鲁棒 "insert into" 之间不能有多余一个空格。
    '''
    def extract_table_name(self, sql):
        insert_pattern = '(?<=insert into).*?(?=\()'          # 提取表名，前向界定、后向界定、懒惰匹配。
        update_pattern = '(?<=update ).*?(?=\()'

        result_insert = re.findall(insert_pattern, sql.lower(), re.DOTALL)
        result_update = re.findall(update_pattern, sql.lower(),re.DOTALL)

        if len(result_insert) > 0:
            return result_insert[0].strip()  # 返回表名
        elif len(result_update)>0:
            return result_update[0].strip()  # update 目标表
        else:
            return False

    #清除err_detector结果，扫描下一个文件。
    def clear(self):
        self.isRight = True
        self._statement = []
        self._field = []
        self.global_exception = global_exception.copy()   # 赋值副本，否则会更改原定义。
        self.local_table_name = {}                        # 记录目标表名与写入次数。
        self.local_exception = {}
        self.target_table_statement = []                  # 记录包含目标表的语句，后续处理。

    def setWrong(self):
        self.isRight = False

    #检测是否用update更新目标表。
    def detect_update_target(self):
        update_pattern = 'update'
        for i in self.target_table_statement:
            if len(re.findall(update_pattern, i, re.IGNORECASE)):
                self.global_exception['update target'] += 1

    '''
        检测是否显式更新etl_tms。
    '''
    def detect_implicit_etl_tms(self):
        etl_tms_pattern = 'etl_tms'
        sysdate_pattern = 'sysdate'
        for i in self.target_table_statement:
            if len(re.findall(sysdate_pattern, i ,re.IGNORECASE)):
                print('yes')
            if len(re.findall(etl_tms_pattern, i ,re.IGNORECASE)) and len(re.findall(sysdate_pattern, i ,re.IGNORECASE)):
                self.global_exception['etl_tms'] = 1
                print('yes, etl_tms')
            else:
                pass

    #输出异常检测结果
    def print_exception(self):
        #是否存在 select *
        if self.global_exception['select *'] > 0:
            self.err.select_error()
            self.setWrong()

        #是否创建多余2个临时表
        if self.global_exception['create multi-table'] > 2:
            self.err.multi_temp_table_error()
            self.setWrong()

        #是否销毁临时表
        if self.global_exception['create multi-table']>=2 and self.global_exception['drop table']==0:
            self.err.no_drop_error()
            self.setWrong()
        sort_table = sorted(self.local_table_name.items(), key=lambda x: x[1], reverse=True)

        #是否写入多目标表
        if len(self.local_table_name)>1:
            self.err.multi_target_error()
            self.setWrong()

        #是否多次写入目标表
        try :
            if sort_table[0][1]>1:
                self.err.multi_write_error()
                self.setWrong()
        except IndexError as i:
            print('No target table!')

        #是否存在一条语句多distinct情况
        if self.global_exception['flag_distinct']:
            self.err.over_distinct_error()
            self.setWrong()

        #是否update目标表
        if self.global_exception['update target'] > 0:
            self.err.update_target_table_error()
            self.setWrong()

        #是否显式赋值etl_tms
        if self.global_exception['etl_tms'] == 0:
            self.err.implicit_etl_tms_error()
            self.setWrong()

        if self.isRight:
            print('     扫描完毕，未发现错误！')

