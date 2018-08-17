#-*- utf-8 -*-
import re
import sys
from err_define import error_define

'''
	重构err_detect代码。
'''
global_exception = {  # 统计全局错误
    'select *': False,  # 全局范围
    'count *': False,  # 全局范围
    'flag_distinct': False,  # 单条语句包含多余三条distinct             全局范围
    'case_no_else': 0,  # case语句缺失else分支                     全局范围
    'insert_or_select_no_field': 0,  # insert、select未显式指定字段名           全局范围
    'join_no_outer_inner': 0,  # join未指定outer、inner                   全局范围
    'not_between': 0,  # 出现NOT BETWEEN                          全局范围
    'func_where_field': 0,  # 函数操作where字段                        全局范围

    'multi_target': 0,  # 操作多目标表                             目标表
    'multi_insert_target': 0,  # 多次插入目标表                           目标表
    'etl_tms': False,  # 未显式更新etl_tms                        目标表

    'no_on_commit_preserve_rows': 0,  # 创建临时表未使用on commit preserve rows  临时表
    'create_multi_tmp_table': 0,  # 创建多临时表                             临时表
    'drop_tmp_table': 0,  # 未显式销毁临时表                         临时表

    'update_target': False,  # 采用update更新目标表
}

'''
	ToDo:
		 创建临时表异常检测。
'''

'''
	error_detect异常检测，负责调度 detector 与 error_print
'''

class error_detection():
    def __init__(self, statement):
        self.detector = detector()  # 初始化检测器
        self.err_print = printer()  # 初始化输出类
        self.global_exception = None  # 记录检测结果
        self.statement = statement  # 存储分割后的SQL语句

        # 检测异常过程。

    def run(self):
        self.global_exception = detector(self.statement)
        self.err_print(self.global_exception)

    def __call__(self):
        self.run()

# 异常检测器，负责检测异常，返回结果至error_detect.global_exception
class detector():
    def __init__(self, statement):
        self.isRight = True  # 全局flag，SQL脚本是否存在异常语句
        self.statement = statement  # 分割后的SQL语句
        self.field = []  # 分割后的字段
        self.global_exception = global_exception.copy()  # 全局异常检测副本
        self.local_table_name = {}  # 记录目标表名与写入次数
        self.local_exception = {}  # 暂未使用 Todo
        self.target_table_statement = []  # 记录包含目标表的语句，后续处理
        self.target_table_name = []
        self.err = error_define()  # 异常定义

    # 正则匹配select *,若存在，置global_exception为 True
    def select_err(self, sql):
        pattern = 'select\s*\\*'
        result = re.search(pattern, sql, re.IGNORECASE)
        if result:
            self.global_exception['select *'] = True
        else:
            pass

    def count_err(self, sql):
        #pattern = 'count\s*\\*'
        pattern = 'count(.|\s)*\\*'
        result = re.search(pattern, sql, re.IGNORECASE)
        if result:
            self.global_exception['count *'] = True
        else:
            pass

    def distinct_err(self, sql):
        pattern = 'distinct'
        result = re.findall(pattern, sql, re.IGNORECASE)
        if len(result) > 3:
            self.global_exception['flag_distinct'] = True

    # case...when...then...else...     情况可能较复杂，此处只检测一个case语句中是否存在else
    def case_no_else_err(self, sql):
        case_pattern = 'case'
        else_pattern = 'else'
        # sql语句中有case而无else异常置True
        if re.search(case_pattern, sql, re.IGNORECASE) and not re.search(else_pattern, sql, re.IGNORECASE):
            self.global_exception['case_no_else'] = True

    def join_no_outer_inner_err(self, sql):
        join_pattern  = 'join'
        outer_pattern = 'outer'
        inner_pattern = 'inner'
        # sql语句中有case而无else异常置True
        join_ = re.search(join_pattern, sql, re.IGNORECASE)
        outer_ = re.search(outer_pattern, sql, re.IGNORECASE)
        inner_ = re.search(inner_pattern, sql, re.IGNORECASE)
        if join_ and not (outer_ or inner_):  # join语句没有outer或inner
            self.global_exception['join_no_outer_inner'] = True

    def not_between_err(self, sql):
        pattern = 'not.*between'
        result = re.search(pattern, sql, re.IGNORECASE)
        if result:
            self.global_exception['not_between'] = True

    def multi_tmp_table(self, sql):        # 检测创建临时表 与 是否 on commit preserve rows
        tmp_pattern = 'local.*temporary'
        order_pattern = 'on.*rows'
        tmp_result = re.search(tmp_pattern, sql, re.IGNORECASE)
        if tmp_result:                                        #若语句为创建语句，则检测是否有on commit preserve rows
            self.global_exception['create_multi_tmp_table'] += 1
            order_result = re.search(order_pattern, sql, re.IGNORECASE)
            if not order_result:
                self.global_exception['no_on_commit_preserve_rows'] += 1

    def drop_tmp_table_err(self, sql):     # 检测删除临时表操作
        pattern = 'drop'
        result = re.findall(pattern, sql, re.IGNORECASE)
        if  result:
            self.global_exception['drop_tmp_table'] += 1



    def explicit_etl_tms_err(self,sql):   #检测目标表插入是否显式指定sysdate
        etl_tms_pattern = 'etl.*tms'
        sysdate_pattern = 'sysdate'
        etl_tms_ = re.search(etl_tms_pattern, sql, re.IGNORECASE)
        sysdate_ = re.search(sysdate_pattern, sql, re.IGNORECASE)
        if etl_tms_ and not sysdate_:
            self.global_exception['etl_tms'] = True

    def is_temp_table(self,table_name):
        if not table_name.startswith('tmp'):
            return False
        else:
            return True

    def delete_target_detect(self, sql):
        delete_pattern = 'delete.*from'
        delete_ = re.search(delete_pattern, sql, re.IGNORECASE)
        if delete_:
            table_name = sql.replace(delete_.group(0), '').strip().split(' ')[0].strip()
            if not self.is_temp_table(table_name) and table_name not in self.target_table_name:                # 表名为目标表
                self.target_table_name.append(table_name)
                self.global_exception['multi_target'] += 1

    def update_target_detect(self, sql):
        update_pattern = 'update'
        update_ = re.search(update_pattern, sql, re.IGNORECASE)
        if update_:
            table_name = sql.replace('update', '').strip().split(' ')[0].strip()
            if not self.is_temp_table(table_name) and table_name not in self.target_table_name:                # 表名为目标表
                self.target_table_name.append(table_name)
                self.global_exception['update_target'] = True   #是否update目标表
                self.global_exception['multi_target'] += 1
    '''
        两步正则。
    '''
    def insert_target_detect(self, sql):  #两步正则，先检测insert into, 再通过前向后向界定检测目标表名。
        insert_pattern = 'insert.*into'
        insert_ = re.search(insert_pattern, sql, re.IGNORECASE)
        if insert_:
            table_name = re.search(f'(?<={insert_.group(0)}).*?(?=\()', sql, re.IGNORECASE).group(0).strip()
            if not self.is_temp_table(table_name) and table_name not in self.target_table_name:
                self.target_table_name.append(table_name)
                self.global_exception['multi_target'] += 1

            #多次写入目标表。
            if not self.is_temp_table(table_name):
                self.global_exception['multi_insert_target'] += 1
                self.target_table_statement.append(sql)             #记录目标表写入语句。

    def multi_target_err(self, sql):            #检测目标表,综合insert、update、delete
        self.delete_target_detect(sql)
        self.update_target_detect(sql)
        self.insert_target_detect(sql)


    def detect(self):  # 返回检测
        for sql in self.statement:
            if not self.global_exception['select *']:  # 若已监测到'select *'，则跳过。
                self.select_err(sql)

            if not self.global_exception['count *']:  # 若已监测到'count *'，则跳过。
                self.count_err(sql)

            if not self.global_exception['flag_distinct']:  # 若已监测到'distinct error'，则跳过。
                self.distinct_err(sql)

            if not self.global_exception['case_no_else']:  # 若已监测到'case no else'，则跳过。
                self.case_no_else_err(sql)

            if not self.global_exception['join_no_outer_inner']:  # 若已监测到'case no else'，则跳过。
                self.join_no_outer_inner_err(sql)

            if not self.global_exception['not_between']:
                self.not_between_err(sql)


            self.multi_tmp_table(sql)               #检测临时表数量
            self.drop_tmp_table_err(sql)            #检测是否drop临时表
            self.multi_target_err(sql)              #检测目标表

        # 在目标表语句中检测是否显式插入sysdate
        for sql in self.target_table_statement:
            if not self.global_exception['etl_tms']:
                self.explicit_etl_tms_err(sql)

        print(self.global_exception)


        return global_exception


# 输出检测错误、写文件。
class printer():
    def __init__(self, dst_filename):
        self.dst_filename = dst_filename

    def print_to_file(self):  # 输出异常检测结果到文件。
        pass

    def print_to_screen(self):
        print(self.detector)

    def __call__(self):
        self.output()

path_to_sql = 'D:\\项目管理\\venv\\code-review\\test\\tmp_3.sql'
sql = ''
with open(path_to_sql, 'rb') as f:
    for i in f:
        sql = f"{sql} {i.decode('utf8').strip()}"
statement = sql.split(';')
detect = detector(statement)
detect.detect()
#detect = detector('D:\\项目管理\\venv\\code-review\\test\\tmp_3.sql')