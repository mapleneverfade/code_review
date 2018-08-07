#-*- utf-8 -*-
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