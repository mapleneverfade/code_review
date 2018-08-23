#-*- utf-8 -*-
import re
import sys

from .err_define import error_define
from .func_dic import function
'''
	重构err_detect代码。
'''
global_exception = {  # 统计全局错误
    'select *': False,  # 全局范围
    'count *': False,  # 全局范围
    'flag_distinct': False,  # 单条语句包含多余三条distinct             全局范围
    'case_no_else': False,  # case语句缺失else分支                     全局范围
    'join_no_outer_inner': 0,  # join未指定outer、inner                   全局范围
    'not_between': 0,  # 出现NOT BETWEEN                          全局范围

    'multi_target': 0,  # 操作多目标表                             目标表
    'multi_insert_target': 0,  # 多次插入目标表                           目标表
    'etl_tms': False,  # 未显式更新etl_tms                        目标表

    'no_on_commit_preserve_rows': 0,  # 创建临时表未使用on commit preserve rows  临时表
    'create_multi_tmp_table': 0,  # 创建多临时表                             临时表
    'drop_tmp_table': 0,  # 未显式销毁临时表                         临时表

    'update_target': False,  # 采用update更新目标表

    'explicit_field': False,
    'where_exist_function': False
}

'''
	ToDo:
		 创建临时表异常检测。
'''

# 异常检测器，负责检测异常，返回结果至error_detect.global_exception
class err_detector():
    def __init__(self, sql = None, statement = None):
        self.isRight = True                             # 全局flag，SQL脚本是否存在异常语句
        self._statement = statement                       # 分割后的SQL语句
        self._sql = sql

        self.tmp_create_statement = []
        self.tmp_field = {}
        self.target_field = {}                                  # 分割后的字段 {'table_name':field list}

        self.global_exception = global_exception.copy()  # 全局异常检测副本
        self.local_table_name = {}                       # 记录目标表名与写入次数
        self.local_exception = {}                        # 暂未使用 Todo
        self.target_table_statement = []                 # 记录包含目标表的语句，后续处理
        self.target_table_name = []
        self.err = error_define()                        # 异常定义

        self.create_set = set()                          #记录创建临时表字段数
        self.insert_set = set()                          #记录插入目标表字段数
        self.select_set = set()                          #记录select字段数

        self.split_to_field = statement_to_field()
    # 正则匹配select *,若存在，置global_exception为 True
    @property
    def statement(self):
        return self._statement
    @statement.setter
    def statement(self,statement):
        self._statement = statement
    @property
    def sql(self):
        return self._sql
    @sql.setter
    def sql(self,sql):
        self._sql = sql

    def select_err(self, sql):
        pattern = 'select\s*\\*'
        result = re.search(pattern, sql, re.IGNORECASE)
        if result:
            self.global_exception['select *'] = True
        else:
            pass

    def count_err(self, sql):
        #pattern = 'count\s*\\*'
        pattern = 'count[\\(|\s)]+?\\*'            # 懒惰匹配 count *
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
        else:
            pass

    # case...when...then...else...     情况可能较复杂，此处只检测一个case语句中是否存在else
    def case_no_else_err(self, sql):
        case_pattern = 'case'
        else_pattern = 'else'
        # sql语句中有case而无else异常置True
        if re.search(case_pattern, sql, re.IGNORECASE) and not re.search(else_pattern, sql, re.IGNORECASE):
            self.global_exception['case_no_else'] = True
        else:
            pass

    def join_no_outer_inner_err(self, sql):
        join_pattern  = 'join'
        outer_pattern = 'outer'
        inner_pattern = 'inner'
        # sql语句中有case而无else异常置True
        join_ = re.search(join_pattern, sql, re.IGNORECASE)
        outer_ = re.search(outer_pattern, sql, re.IGNORECASE)
        inner_ = re.search(inner_pattern, sql, re.IGNORECASE)
        if join_ and not (outer_ or inner_):                # join语句没有outer或inner
            self.global_exception['join_no_outer_inner'] = True
        else:
            pass

    def not_between_err(self, sql):
        pattern = 'not.*between'
        result = re.search(pattern, sql, re.IGNORECASE)
        if result:
            self.global_exception['not_between'] = True
        else:
            pass

    def drop_tmp_table_err(self, sql):     # 检测删除临时表操作
        pattern = 'drop'
        result = re.findall(pattern, sql, re.IGNORECASE)
        if  result:
            self.global_exception['drop_tmp_table'] += 1

    def explicit_etl_tms_err(self,sql):    # 检测目标表插入是否显式指定sysdate
        etl_tms_pattern = 'etl.*tms'
        sysdate_pattern = 'sysdate'
        etl_tms_ = re.search(etl_tms_pattern, sql, re.IGNORECASE)
        sysdate_ = re.search(sysdate_pattern, sql, re.IGNORECASE)
        if etl_tms_ and not sysdate_:
            self.global_exception['etl_tms'] = True

    def multi_tmp_table(self, sql):        # 检测创建临时表 与 是否 on commit preserve rows
        tmp_pattern = 'local.*temporary'
        order_pattern = 'on.*rows'
        tmp_result = re.search(tmp_pattern, sql, re.IGNORECASE)
        if tmp_result:                                              # 若语句为创建语句，则检测是否有on commit preserve rows
            self.global_exception['create_multi_tmp_table'] += 1
            self.tmp_create_statement.append(sql)                   # 存入创建临时表语句。

            order_result = re.search(order_pattern, sql, re.IGNORECASE)
            if not order_result:
                self.global_exception['no_on_commit_preserve_rows'] += 1

    def is_temp_table(self,table_name):
        if not table_name.startswith('tmp'):
            return False
        else:
            return True

    '''
        delete_target_detect
        update_target_detect
        insert_target_detect
        负责检测插入、删除、更新目标表操作
        ************目标表检测***************
    '''
    def delete_target_detect(self, sql):
        delete_pattern = '^delete.*from'
        delete_ = re.search(delete_pattern, sql.strip(), re.IGNORECASE)
        if delete_:
            table_name = sql.replace(delete_.group(0), '').strip().split(' ')[0].strip()
            if not self.is_temp_table(table_name) and table_name not in self.target_table_name:                # 表名为目标表
                self.target_table_name.append(table_name)
                self.global_exception['multi_target'] += 1

    def update_target_detect(self, sql):
        update_pattern = '^update'
        update_ = re.search(update_pattern, sql.strip(), re.IGNORECASE)
        if update_:
            table_name = sql.replace('update', '').strip().split(' ')[0].strip()
            if not self.is_temp_table(table_name) and table_name not in self.target_table_name:                # 表名为目标表
                self.target_table_name.append(table_name)
                self.global_exception['update_target'] = True   #是否update目标表
                self.global_exception['multi_target'] += 1
    '''
        两步正则。
        1、insert into {table} (field)
        2、insert into {table} select {field}
    '''

    def insert_target_detect(self, sql):  #两步正则，先检测insert into, 再通过前向后向界定检测目标表名。
        insert_pattern = '^insert.*into'
        insert_ = re.search(insert_pattern, sql.strip(), re.IGNORECASE)
        if insert_:
            try:
                table_name = re.search(f'(?<={insert_.group(0)}).*?(?=\()', sql, re.IGNORECASE).group(0).strip()
                if not self.is_temp_table(table_name) and table_name not in self.target_table_name:
                    self.target_table_name.append(table_name)
                    self.global_exception['multi_target'] += 1       # 多目标表

                #多次写入目标表。
                if not self.is_temp_table(table_name):
                    self.global_exception['multi_insert_target'] += 1
                    self.target_table_statement.append(sql)             # 记录目标表写入语句。
            except AttributeError as e:
                print('未显示指定insert 字段！')
                self.global_exception['explicit_field'] = True      # 直接置错

    def multi_target_err(self, sql):            #检测目标表,综合insert、update、delete
        self.delete_target_detect(sql)
        self.update_target_detect(sql)
        self.insert_target_detect(sql)
    '''
        ************目标表检测***************
    '''

    '''
        ToDo—insert、select字段须明确提供字段名。
        1、提取create tmp_table表名，表字段，存储。
        2、提取targer table 表字段，存储。
        对比target table 表字段与create table。
        
        错误！字段类型中包含Numeric(18,7) , select 中包含函数 tochar('','')
    '''
    '''
        提取表名
    '''
    '''
        添加检测规则，创建表时可能存在未指定字段名情况。
        1、以 ( 结尾提取表名。
        2、以 \n 换行结尾提取表名。
    '''
    def extract_table_name(self, sql, flag = 'temp'):
        if flag == 'temp':
            temp_pattern = '(?<=table).*?(?=\()'
            enter_pattern = '(?<=table).*?(?=on)'                   # 以 on 结尾提取临时表名
            result = re.search(temp_pattern, sql ,re.IGNORECASE)
            if result:
                pass
            else:
                result = re.search(enter_pattern, sql, re.IGNORECASE)   # 以 'on'为结尾提取临时表名，出现此种情况，说明没有指定字段。
                self.global_exception['explicit_field'] = True      # 直接置错
                #print(f'临时表 {result.group(0).strip()} 未显式指定任何字段！')

        elif flag=='target':
            target_pattern = '(?<=into).*?(?=\()'                    # 待插入目标表名
            result = re.search(target_pattern, sql, re.IGNORECASE)
        else:
            print('提取表名过程错误！')
        return result.group(0).strip()

    '''
        提取字段名
    '''
    # 考虑重构功能，将提取字段与对比功能抽象为新类。

    def explicit_field(self):
        #self.tmp_field — self.target_field
        #self.tmp_create_statement — self.target_table_statement
        #提取 tmp_table 名

        for i in self.tmp_create_statement:
            name_ = self.extract_table_name(i, 'temp')
            #self.tmp_field[name_] = self.split_to_field(i, 'temp')    # 提取字段加入self.tmp_field

            self.split_to_field.statement = i
            middle_param = self.split_to_field.to_field('temp')
            if middle_param:
                self.tmp_field[name_] = middle_param
                self.create_set.add(len(self.tmp_field[name_]))
            else:                                              # 创建临时表未显式提供字段。
                self.global_exception['explicit_field'] = True      # 直接置错

        for i in self.target_table_statement:
            name_ = self.extract_table_name(i, 'target')
            #self.target_field[name_+'_insert'], self.target_field[name_+'_select'] = self.split_to_field(i, 'target')
            self.split_to_field.statement = i
            self.target_field[name_ + '_insert'], self.target_field[name_ + '_select'] = self.split_to_field.to_field('target')

            self.insert_set.add(len(self.target_field[name_+'_insert']))
            self.select_set.add(len(self.target_field[name_+'_select']))
            print(self.target_field, self.tmp_field)
            print(self.insert_set,self.select_set,self.create_set)

    '''
        where 条件字段函数判断需要更改逻辑，适配不同脚本情况。
        干扰条件包括：
        1、select
        2、having
        3、join
        方案：删掉干扰部分。
    '''
    def where_func_err(self, sql):
        #pattern = '(?<=where).*?(?=;)'
        where_pattern = 'where.*?;'
        select_pattern = 'select.*?from'
        having_pattern = 'having.*'
        join_pattern = 'join.*where'
        result = re.findall(where_pattern, sql.lower(), re.DOTALL)
        func = []
        for i in function.values():
            func.extend(i)
        concat = ''
        if result:
            for i in result:                    # 连接所有where ...; 语句，方便检测
                concat = f'{concat} {i}'
            concat = re.sub(select_pattern, '', concat)
            concat = re.sub(having_pattern, '', concat)
            concat = re.sub(join_pattern, '', concat)

            for func_ in func:                  # 函数pattern
                func_pattern = f'{func_}\\(.*?\\)'
                func_detect_result = re.search(func_pattern, concat, re.IGNORECASE)
                if func_detect_result:
                    self.global_exception['where_exist_function'] = True

    # 检测是否grant语句。
    def is_grant(self, sql):
        pattern = 'grant.*on'
        if re.search(pattern, sql, re.IGNORECASE):
            return True
        else:
            return False

    def detect(self):  # 返回检测
        for sql in self.statement:
            if self.is_grant(sql):                       # 去除grant语句干扰。
                continue
            if not self.global_exception['select *']:  # 若已监测到'select *'，则跳过。
                self.select_err(sql)

            if not self.global_exception['count *']:  # 若已监测到'count *'，则跳过。
                self.count_err(sql)

            if not self.global_exception['flag_distinct']:  # 若已监测到'distinct error'，则跳过。
                self.distinct_err(sql)

            if not self.global_exception['case_no_else']:  # 若已监测到'case no else'，则跳过。
                self.case_no_else_err(sql)

            if not self.global_exception['join_no_outer_inner']:  # 若已监测到'join no outer|inner'，则跳过。
                self.join_no_outer_inner_err(sql)

            if not self.global_exception['not_between']:
                self.not_between_err(sql)

            self.multi_tmp_table(sql)               #检测临时表数量
            self.drop_tmp_table_err(sql)            #检测是否drop临时表
            self.multi_target_err(sql)              #检测目标表

        self.where_func_err(self.sql)
        # 在目标表语句中检测是否显式插入sysdate
        for sql in self.target_table_statement:
            if not self.global_exception['etl_tms']:
                self.explicit_etl_tms_err(sql)

        self.explicit_field()

        if not (self.insert_set == self.select_set and self.create_set&self.insert_set):  #若create与select或insert字段数不一致，则置error
            self.global_exception['explicit_field'] = True

        return self.global_exception

    # 重置变量。
    def clear(self):
        self.isRight = True                             # 全局flag，SQL脚本是否存在异常语句
        self.statement = []                       # 分割后的SQL语句
        self.sql = ''
        self.tmp_create_statement = []
        self.tmp_field = {}
        self.target_field = {}                           # 分割后的字段 {'table_name':field list}
        self.global_exception = global_exception.copy()  # 全局异常检测副本
        self.local_table_name = {}                       # 记录目标表名与写入次数
        self.local_exception = {}                        # 暂未使用 Todo
        self.target_table_statement = []                 # 记录包含目标表的语句，后续处理
        self.target_table_name = []
        self.err = error_define()                        # 异常定义
        self.create_set = set()                          #记录创建临时表字段数
        self.insert_set = set()                          #记录插入目标表字段数
        self.select_set = set()                          #记录select字段数
        self.split_to_field = statement_to_field()
    '''
        去掉所有注释，排除检测干扰。
    '''
    @staticmethod
    def delete_note(sql):
        pattern = '--.*?\n'
        result = re.search(pattern, sql, re.IGNORECASE)
        if result:
            print('Yes')
            return re.sub('\n', '',  re.sub(pattern, '', sql))  #剔除注释和换行符
        else:
            print('No')
            return sql

'''
    重构代码提出新类
    负责分割出create、insert、select语句中的所有字段
    同时检测出现异常
'''

class statement_to_field():
    def __init__(self):
        self.flag = True  # 指示是否存在分割字段。
        self._statement = None
        self._field = None
    @property
    def statement(self):
        return self._statement
    @statement.setter
    def statement(self,new_statement):
        self._statement = new_statement
    @property
    def field(self):
        return self._field
    @field.setter
    def field(self, new_field):
        self._field = new_field

    # 考虑重构功能，将提取字段与对比功能抽象为新类。
    def to_field(self, flag='temp'):
            if flag == 'temp':
                tmp_field_name = []  # 存储提取字段名
                create_pattern = '(?<=\().*?(?=on commit)'         # 提取临时表字段
                result = re.search(create_pattern, self.statement, re.IGNORECASE) # 若为空，则说明创建临时表时未显式指定字段。
                if result:
                    result = re.sub('(?<=\().*?(?=\))', '', result.group(0).strip(')'))  # 去掉类型中的内容','
                    for frame_statement in result.split(','):
                        tmp_field_name.append(frame_statement)
                    #self.create_set.add(len(tmp_field_name))
                else:
                    return None
                return tmp_field_name

            elif flag == 'target':
                insert_field_name = []  # insert字段记录
                select_field_name = []  # select字段记录
                insert_pattern = '(?<=\().*?(?=select)'
                select_pattern = '(?<=select).*?(?=from)'
                insert_result = re.search(insert_pattern, self.statement, re.IGNORECASE)
                select_result = re.search(select_pattern, self.statement, re.IGNORECASE)

                if insert_result and select_result:
                    for frame_statement in insert_result.group(0).split(','):
                        insert_field_name.append(frame_statement)

                    select_result = re.sub('(?<=\().*?(?=\))', '', select_result.group(0))  # 去掉select函数中的内容','
                    for frame_statement in select_result.split(','):
                        select_field_name.append(frame_statement)
                #self.insert_set.add(len(insert_field_name))
                #self.select_set.add(len(select_field_name))
                return insert_field_name, select_field_name
            else:
                print('提取字段过程错误！')


if __name__ == '__main__':

    path_to_sql = 'D:\\项目管理\\venv\\code-review\\test\\tmp_3.sql'
    dst_path = 'C:\\Users\\chenchangyu\\Desktop\\测试屋\\test.txt'

    sql = ''
    with open(path_to_sql, 'rb') as f:
        for i in f:
            pattern = '--.*?\n'                         # 匹配注释段
            i =  re.sub(pattern, '', i.decode('utf8'))  # 剔除注释
            sql = f"{sql} {i.strip()}"

    statement = sql.split(';')
    detect = detector(sql, statement)
    detect.detect()

    p = err_printer(dst_path, detect.global_exception)
    p.print_to_file()
    #detect = detector('D:\\项目管理\\venv\\code-review\\test\\tmp_3.sql')
