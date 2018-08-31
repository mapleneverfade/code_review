#-*- utf-8 -*-
from copy import deepcopy
'''
    code review异常定义。
'''
#   异常定义类
'''
    本文件定义异常类，
    1、err_detect类中全局异常
    2、err_locate类中定位异常字典
'''

err_dic = {
            'select *'                       :set(),      # yes
            'count *'                        :set(),      # yes
            'flag_distinct'                 :set(),      # yes
            'case_no_else'                  :set(),      # yes
            'join_no_outer_inner'          :set(),      # yes
            'not_between'                   :set(),      # yes
            'multi_target'                  :set(),
            'multi_insert_target'          :set(),
            'etl_tms'                        :set(),
            'no_on_commit_preserve_rows'  :set(),      # yes
            'create_multi_tmp_table'       :set(),
            'drop_tmp_table'                :set(),
            'update_target'                 :set(),
            'explicit_field'                :set(),
            'where_exist_function'         :set()
        }

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


class error_define():
    def __init__(self):
        self.err_dic = deepcopy(err_dic)
        self.global_exception = global_exception
        self.exception = {
            'select':                      Exception("       SQL 程序中包含 'SELECT *'"),  # yes
            'multi-temp-table':           Exception('       SQL 脚本创建两个以上临时表'),  # yes
            'no-drop-table':               Exception('       SQL 脚本未显式销毁临时表'),     # yes
            'multi-target':                Exception('       SQL 脚本写入多个目标表 '),      # yes
            'multi-write':                 Exception('       SQL 脚本多次写入目标表 '),      # yes
            'over-distinct':               Exception('        SQL 语句包含多条 distinct '),  # yes
            'update-target':               Exception('        SQL UPDATE 目标表 ') ,          # yes
            'implicit-etl-tms':            Exception('        SQL 未显式赋值etl_tms') ,        # ing

            'case-no-else':                 Exception('        case语句缺失else分支'),         # ing
            'insert-select-lack-field':   Exception('        select|insert未显式提供字段名'),         # ing
            'join-no-outer-inner'      :   Exception('        JOIN未指定outer|inner'),         # ing
            'not-between'                :  Exception('        SQL脚本出现NOT-BETWEEN') ,        # ing
            'where-function'            :  Exception('        函数操作 where 条件字段'),        # ing
            'count *':                       Exception('        SQL脚本包含 count *'),         # ing
            'no-commit-preserve-rows'   : Exception('        未创建on-commit-preserve-rows'),         # ing
            'explicit-field':               Exception('        未显式指定insert|select字段')
        }
    # select * 错误
    def select_error(self):
        print(self.exception['select'])

    # 创建两个以上临时表错误
    def multi_temp_table_error(self):
        print(self.exception['multi-temp-table'])

    # 未显式销毁临时表
    def no_drop_error(self):
        print(self.exception['no-drop-table'])

    # 写入多目标表错误
    def multi_target_error(self):
        print(self.exception['multi-target'])

    # 多次写入目标表错误
    def multi_write_error(self):
        print(self.exception['multi-write'])

    # 一条语句包含超过3条distinct
    def over_distinct_error(self):
        print(self.exception['over-distinct'])

    def update_target_table_error(self):
        print(self.exception['update-target'])

    def implicit_etl_tms_error(self):
        print(self.exception['implicit-etl-tms'])

    def explicit_field(self):
        print(self.exception['explicit-field'])