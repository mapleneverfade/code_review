#-*- utf-8 -*-
import re

'''
    本文件包含code review所有异常定义。
'''
exception ={
    'select':                   Exception("SQL 程序中包含 'SELECT *'"),  #yes
    'multi-temp-table':       Exception('SQL 脚本创建两个以上临时表'),  #yes
    'no-drop-table':           Exception('SQL 脚本未显式销毁临时表'),    #yes
    'multi-target':            Exception('SQL 脚本写入多个目标表 '),     #yes
    'multi-write':             Exception('SQL 脚本多次写入目标表 '),     #yes
    'over-distinct':           Exception('SQL 语句包含多条 distinct '), #yes
    'update-target':           Exception('SQL UPDATE 目标表 ')
}
#select * 错误
def select_error():
    print(exception['select'])

#创建两个以上临时表错误
def multi_temp_table_error():
    print(exception['multi-temp-table'])

#未显式销毁临时表
def no_drop_error():
    print(exception['no-drop-table'])

#写入多目标表错误
def multi_target_error():
    print(exception['multi-target'])

#多次写入目标表错误
def multi_write_error():
    print(exception['multi-write'])

#一条语句包含超过3条distinct
def over_distinct_error():
    print(exception['over-distinct'])

def update_target_table_error():
    print(exception['update-target'])

def detect_keyword(sql):
    select_pattern = 'select\s*\\*'
    create_pattern = 'create'
    drop_pattern   = 'drop'
    result_select  = re.findall(select_pattern, sql, re.IGNORECASE)      #匹配 'select'
    result_create  = re.findall(create_pattern, sql, re.IGNORECASE)      #匹配 'create'
    result_drop    = re.findall(drop_pattern, sql, re.IGNORECASE)          #匹配 'drop'
    tmp_table      = extract_table_name(sql)
    return len(result_select), len(result_create), len(result_drop), tmp_table

def extract_table_name(sql):
    pattern = '(?<=insert into ).*?(?=\()'     #提取表名，前向界定、后向界定、懒惰匹配。
    result = re.findall(pattern, sql.lower(),re.DOTALL)
    if len(result) > 0:
        return result[0]  #返回表名
    else:
        return False

class exception_detect():
    def __init__(self):
        self._statement = []
        self._field = []
        self.global_exception ={            #统计全局错误
                'select *':0,
                'create multi-table': 0,
                'drop table':0,
                'insert target':0
        }
        self.local_table_name = {}           #记录目标表名与写入次数。
        self.local_exception = {}

    def get_statement(self, statement):
        self._statement = statement

    def get_field(self, field):
        self._field = field

    def global_exception_detect(self):   #检测全局异常
        for i in self._statement:
            select, create, drop, table_name = detect_keyword(i)
            self.global_exception['select *']                += select
            self.global_exception['create multi-table']    += create
            self.global_exception['drop table']             += drop

            if table_name and not table_name.startswith('tmp'):    #统计目标表数与写入次数。
                if table_name not in self.local_table_name:
                    self.local_table_name[table_name] = 1
                else:
                    self.local_table_name[table_name] += 1

    #输出异常检测结果
    def print_exception(self):
        if self.global_exception['select *'] > 0:
            select_error()
        if self.global_exception['create multi-table'] > 2:
            multi_temp_table_error()
        if self.global_exception['create multi-table']>=2 and self.global_exception['drop table']==0:
            no_drop_error()

        sort_table = sorted(self.local_table_name.items(), key=lambda x: x[1], reverse=True)

        if len(self.local_table_name)>1:
            multi_target_error()
        if sort_table[0][1]>1:
            multi_write_error()





