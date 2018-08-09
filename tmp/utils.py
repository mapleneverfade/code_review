#-*- coding:utf-8-*-
import re

'''
    options:保留测试功能。
'''

def detect_keyword(sql):               #针对单语句正则匹配相应关键字。
    select_pattern = 'select\s*\\*'  #正则匹配模式
    create_pattern = 'create'
    drop_pattern   = 'drop'
    distinct_pattern = 'distinct'
    flag_distinct = False

    result_select  = re.findall(select_pattern, sql, re.IGNORECASE)      #匹配 'select'
    result_create  = re.findall(create_pattern, sql, re.IGNORECASE)      #匹配 'create'
    result_drop    = re.findall(drop_pattern, sql, re.IGNORECASE)        #匹配 'drop'

    if len(re.findall(distinct_pattern, sql, re.IGNORECASE)) > 3:  #对于distinct关键字的检测，以flag_distinct为标志。
        flag_distinct = True
    tmp_table = extract_table_name(sql)
    return len(result_select), len(result_create), len(result_drop), tmp_table, flag_distinct

def extract_table_name(sql):
    pattern = '(?<=insert into ).*?(?=\()'                          #提取表名，前向界定、后向界定、懒惰匹配。
    result = re.findall(pattern, sql.lower(),re.DOTALL)
    if len(result) > 0:
        return result[0]  #返回表名
    else:
        return False