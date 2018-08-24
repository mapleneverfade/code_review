#-*-coding:utf8-*-
import re
'''
    本程序负责定位扫描脚本异常位置。
    1、记录每行对应的行数。
    2、发现异常提取行数。
    3、
'''
err_dic = {
            'select *'                       :[],      # yes
            'count *'                        :[],      # yes
            'flag_distinct'                 :[],      # yes
            'case_no_else'                  :[],      # yes
            'join_no_outer_inner'          :[],      # yes
            'not_between'                   :[],      # yes
            'multi_target'                  :[],
            'multi_insert_target'          :[],
            'etl_tms'                        :[],
            'no_on_commit_preserve_rows'  :[],      # yes
            'create_multi_tmp_table'       :[],
            'drop_tmp_table'                :[],
            'update_target'                 :[],
            'explicit_field'                :[],
            'where_exist_function'         :[]
        }

class err_locater():
    def __init__(self,sql=None):
        self.sql_dic = None     # 脚本字典，每一元素对应一行。
        self._sql = sql
        self.err_dic = err_dic.copy()

    @property
    def sql(self):
        return self._sql
    @sql.setter
    def sql(self, sql_):
        self._sql = sql_
    '''
        完成
    '''
    def select_locate(self):
        pattern = 'select[\s]+?\\*'
        blank_pattern = '\n'
        if re.search(pattern, self.sql, re.IGNORECASE):                 # 脚本存在此异常
            for i in re.finditer(pattern, self.sql, re.IGNORECASE):    # 统计匹配结果字符前所有换行符'\n',即为行数
                row_num = len(re.findall(blank_pattern, self.sql[:i.start()], re.IGNORECASE))+1
                self.err_dic['select *'].append(row_num)
                print(f'select 异常{row_num}')
    '''
        完成
    '''
    def count_locate(self):
        pattern = 'count[\\(|\s]+?\\*'
        blank_pattern = '\n'
        if re.search(pattern, self.sql, re.IGNORECASE):
            for i in re.finditer(pattern, self.sql, re.IGNORECASE):
                row_num = len(re.findall(blank_pattern, self.sql[:i.start()], re.IGNORECASE))+1
                self.err_dic['count *'].append(row_num)
                print(f'count 异常{row_num}')
    '''
        多distinct语句的检测，不能采用同其他异常相同的检测方式，
        distinct会在多行出现多次，只能通过限定正则检测范围来定位错误。
        解决方式：
                1、两步正则。先提取 'select...;' 之间的文本，再对检测文本进行distinct检测。
    '''
    '''
        ！完成
    '''
    def distinct_locate(self):
        select_pattern = 'select(.|\n)+?;'   # 注意惰性匹配
        distinct_pattern = 'distinct'
        blank_pattern = '\n'

        select_result = re.finditer(select_pattern, self.sql, re.IGNORECASE)

        for select_statement in select_result:
            if len(re.findall(distinct_pattern, select_statement.group(0), re.IGNORECASE)) > 3:                          # 若一段语句distinct超过3个
                row_num_select = len(re.findall(blank_pattern, self.sql[:select_statement.start()], re.IGNORECASE))+1    # 计算 select 行数

                distinct_result = re.search(distinct_pattern, select_statement.group(0), re.IGNORECASE)                                             # 检测异常语句中第一个 distinct 位置
                row_num_distinct = len(re.findall(blank_pattern, select_statement.group(0)[:distinct_result.start()], re.IGNORECASE))               # 计算 distinct 在段内偏移, 不用加 1

                row_num = row_num_select + row_num_distinct   # distinct 所处行数
                self.err_dic['flag_distinct'].append(row_num)

                print(f'distinct error 行数:{row_num}')
            else:
                pass
    '''
        处理方式同 distinct_locate 
    '''
    '''
        完成
    '''
    # 完成
    def case_else_locate(self):
        select_pattern = 'select(.|\n)+?;'   # 注意惰性匹配
        case_pattern = 'case\s+when'
        else_pattern = 'else'
        blank_pattern = '\n'
        select_result = re.finditer(select_pattern, self.sql, re.IGNORECASE)

        for select_statement in select_result:
            case_result = re.search(case_pattern, select_statement.group(0), re.IGNORECASE)
            else_result = re.search(else_pattern, select_statement.group(0), re.IGNORECASE)
            if case_result and not else_result:                          # 有 case 无 else
                row_num_select = len(re.findall(blank_pattern, self.sql[:select_statement.start()], re.IGNORECASE))+1    # 计算 select 行数

                case_result = re.search(case_pattern, select_statement.group(0), re.IGNORECASE)                                             # 检测异常语句中第一个 distinct 位置
                row_num_case = len(re.findall(blank_pattern, select_statement.group(0)[:case_result.start()], re.IGNORECASE))               # 计算 distinct 在段内偏移, 不用加 1

                row_num = row_num_select + row_num_case   # distinct 所处行数
                self.err_dic['case_no_else'].append(row_num)

                print(f'case no else error 行数:{row_num}')
            else:
                pass
    # 完成
    def not_between_locate(self):
        not_between_pattern = 'not\s+between'
        blank_pattern = '\n'
        if re.search(not_between_pattern, self.sql, re.IGNORECASE ):                 # 脚本存在此异常
            for i in re.finditer(not_between_pattern, self.sql, re.IGNORECASE):    # 统计匹配结果字符前所有换行符'\n',即为行数
                row_num = len(re.findall(blank_pattern, self.sql[:i.start()], re.IGNORECASE))+1
                self.err_dic['not_between'].append(row_num)
                print(f'not between 异常{row_num}')
    '''
        类似于distinct检测，先提取create...; 之间内容，再检测。
    '''
    '''
        完成
    '''
    def commit_preserve_rows_locate(self):
        create_pattern = 'create(.|\n)*?;'
        local_table_pattern = 'local(.|\n)+?temporary'
        commit_pattern = 'on(.|\n)+rows'
        blank_pattern = '\n'
        create_result = re.finditer(create_pattern, self.sql, re.IGNORECASE)          # 提取 create...; 部分语句

        for create_statement in create_result:
            #print(create_statement.group(0))
            local_table_result = re.search(local_table_pattern, create_statement.group(0), re.IGNORECASE)
            commit_result = re.search(commit_pattern, create_statement.group(0), re.IGNORECASE)

            if local_table_result and not commit_result:
                row_num_local = len(re.findall(blank_pattern, self.sql[:create_statement.start()], re.IGNORECASE)) + 1
                row_num_commit = len(re.findall(blank_pattern, create_statement.group(0)[:local_table_result.start()],
                                              re.IGNORECASE))
                row_num = row_num_local + row_num_commit
                self.err_dic['no_on_commit_preserve_rows'].append(row_num)
                print(f'no on commit error 行数:{row_num}')

            else:
                pass



    def join_locate(self):
        select_pattern = 'select(.|\n)+?;'   # 注意惰性匹配
        join_pattern = 'join'
        inner_pattern = 'inner'
        outer_pattern = 'outer'
        blank_pattern = '\n'
        select_result = re.finditer(select_pattern, self.sql, re.IGNORECASE)

        for select_statement in select_result:
            join_result = re.search(join_pattern, select_statement.group(0), re.IGNORECASE)
            inner_result = re.search(inner_pattern, select_statement.group(0), re.IGNORECASE)
            outer_result = re.search(outer_pattern, select_statement.group(0), re.IGNORECASE)

            if join_result and not (inner_result or outer_result):
                row_num_select = len(re.findall(blank_pattern, self.sql[:select_statement.start()],
                                                re.IGNORECASE)) + 1  # 计算 select 行数

                join_result = re.search(join_pattern, select_statement.group(0))  # 检测异常语句中第一个 distinct 位置
                row_num_join = len(re.findall(blank_pattern, select_statement.group(0)[
                                                             :join_result.start()]))  # 计算 distinct 在段内偏移, 不用加 1

                row_num = row_num_select + row_num_join  # distinct 所处行数
                self.err_dic['join_no_outer_inner'].append(row_num)

                print(f'join_no_outer_inner error 行数:{row_num}')
            else:
                pass
    def execute(self):
        self.select_locate()
        self.count_locate()
        self.distinct_locate()
        self.case_else_locate()
        self.join_locate()
        self.not_between_locate()
        self.commit_preserve_rows_locate()

    def clear(self):
        self.err_dic = err_dic.copy()

if __name__ == '__main__':
    load = err_locater('D:\\项目管理\\venv\\code-review\\test\\tmp_2.sql')
    load.loading()
    pattern = 'select[\s]+\\*'

    blank_pattern = '\n'
    result = re.finditer(pattern, load.sql,re.IGNORECASE)
    for i in result:
        print(load.sql[i.start():i.end()])
        print(len(re.findall(blank_pattern, load.sql[:i.start()], re.IGNORECASE)))

    #print(load.sql)