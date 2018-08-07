#-*-utf8-*-
import sys
content = ['..\\venv\\err',  '..\\venv\\utils']   #添加包路径。
sys.path.extend(content)
import error
import os
import re
import  utils.tools as tool

'''
    本文件包含正则扫描禁止的语法。
'''
#匹配 'select *' 字符
def test_select(sql):
    pattern = 'select\s*\\*'
    result = re.findall(pattern, sql, re.IGNORECASE)
    if len(result) > 0:
        error.select_error()
    else:
        pass

# 统计脚本创建临时表个数。
def count_temp_table(sql):
    pattern = 'create'
    drop_pattern = 'drop'
    result = re.findall(pattern, sql, re.IGNORECASE)             #匹配 'create'
    drop_result = re.findall(drop_pattern, sql, re.IGNORECASE)   #匹配 'drop'
    count = len(result)
    if count > 2:
        error.multi_temp_table_error()
    if count==2 and len(drop_result)==0:
        error.no_drop_error()

#统计目标表数.
def count_target_table(sql):
    tables = tool.extract_table_name(sql)
    table_dic = {}
    for i in filter(lambda x:not x.startswith('tmp'),tables): #过滤临时表名。
        if i not in table_dic :
            table_dic[i] = 1
        else:
            table_dic[i]+=1
    sort_table = sorted(table_dic.items(),key = lambda x:x[1], reverse=True)
    if len(sort_table)>1:                        #目标表数大于1.
        error.multi_target_error()
    if sort_table[0][1] > 1:                     #写入目标表次数超过1.
        error.multi_write_error()

#统计单句distinct数.
def count_distinct(sql):
    sql_vocabulary = sql.split(';')
    pattern = 'distinct'
    for i in sql_vocabulary:
        if len(re.findall(pattern, i )) > 3:
            error.over_distinct_error()
            break
