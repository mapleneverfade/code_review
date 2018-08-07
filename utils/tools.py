#-*-utf-8-*-
import os
import re


#导入sql文件。
def load_sql_file(filename):
    with open(filename, 'rb') as f:
        sql = ''
        for line in f:
            sql = '{}{}'.format(sql, line.decode('utf8').strip())  # 去除了特殊字符
    return sql

#提取表名。
def extract_table_name(sql):
    pattern = '(?<=insert into ).*?(?=\()'     #提取表名，前向界定、后向界定、懒惰匹配。
    result = re.findall(pattern, sql.lower(),re.DOTALL)
    return result
