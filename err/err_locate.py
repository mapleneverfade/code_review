#-*-coding:utf8-*-
import re
from copy import deepcopy
from .err_define import error_define

'''
    本程序负责定位扫描脚本异常位置。
    1、记录每行对应的行数。
    2、发现异常提取行数。

'''
'''
    Todo:
        修正定位，去除注释内容影响
'''

class err_locater():
    def __init__(self,sql=None, target_table_name=None, global_exception=None, where_func = None,implicit_field = None):
        self.err_define = error_define()
        self._sql = sql
        self.err_dic = deepcopy(self.err_define.err_dic)   #　须采用深拷贝

        self.target_table_name = target_table_name
        self.global_exception = global_exception
        self.where_function = where_func
        self.implicit_field = implicit_field

    @property
    def sql(self):
        return self._sql
    @sql.setter
    def sql(self, sql_):
        self._sql = sql_

    '''
        移除注释
        1、 --类型注释
        2、/*...*/ 类型注释
    '''
    def remove_annotation(self):
        anno1_pattern = '--.*?\n'
        anno2_pattern = '/\*(.|\n)*?\*/'
        blank_pattern = '\n'
        self.sql = re.sub(anno1_pattern, '\n', self.sql)             # 移除 --注释部分

        for i in re.finditer(anno2_pattern, self.sql, re.IGNORECASE): # 移除 /*...*/ 注释部分
            if not re.search(blank_pattern, i.group(0), re.IGNORECASE):        # 若/*...*/ 之间无换行符
                self.sql = re.sub(self.to_regular(i.group(0)), '', self.sql)
            else:
                line_row =len(re.findall(blank_pattern, i.group(0), re.IGNORECASE))
                line_pattern = '\n'* line_row                                      # 补充删掉的换行符
                self.sql = re.sub(self.to_regular(i.group(0)), line_pattern, self.sql)

    '''
        完成
    '''
    def select_locate(self):
        pattern = 'select[\s]+?\\*'
        blank_pattern = '\n'
        if re.search(pattern, self.sql, re.IGNORECASE):                 # 若待检脚本存在此异常
            for i in re.finditer(pattern, self.sql, re.IGNORECASE):    # 统计匹配结果字符前所有换行符'\n',即为行数
                row_num = len(re.findall(blank_pattern, self.sql[:i.start()], re.IGNORECASE))+1
                self.err_dic['select *'].add(row_num)
        #print(f'select * 异常行数 : {self.err_dic["select *"]}')
    '''
        完成
    '''
    def count_locate(self):
        pattern = 'count[\\(|\s]+?\\*'
        blank_pattern = '\n'
        if re.search(pattern, self.sql, re.IGNORECASE):
            for i in re.finditer(pattern, self.sql, re.IGNORECASE):
                row_num = len(re.findall(blank_pattern, self.sql[:i.start()], re.IGNORECASE))+1
                self.err_dic['count *'].add(row_num)
        #print(f'count * 异常行数 : {self.err_dic["count *"]}')
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

        select_result = re.finditer(select_pattern, self.sql, re.IGNORECASE)           # 提取脚本中所有 select...; 之间的内容

        for select_statement in select_result:
            if len(re.findall(distinct_pattern, select_statement.group(0), re.IGNORECASE)) > 3:                          # 若一段语句distinct超过3个
                row_num_select = len(re.findall(blank_pattern, self.sql[:select_statement.start()], re.IGNORECASE))+1    # 计算 select 行数

                distinct_result = re.search(distinct_pattern, select_statement.group(0), re.IGNORECASE)                                             # 检测异常语句中第一个 distinct 位置
                row_num_distinct = len(re.findall(blank_pattern, select_statement.group(0)[:distinct_result.start()], re.IGNORECASE))               # 计算 distinct 在段内偏移, 不用加 1

                row_num = row_num_select + row_num_distinct   # distinct 所处行数
                self.err_dic['flag_distinct'].add(row_num)
            else:
                pass
        #print(f'multi-distinct error 异常行数 : {self.err_dic["flag_distinct"]}')
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
                self.err_dic['case_no_else'].add(row_num)
            else:
                pass
        #print(f'case no else error 异常行数 : {self.err_dic["case_no_else"]}')

    # 完成 检测方式同select * | count *
    def not_between_locate(self):
        not_between_pattern = 'not\s+between'
        blank_pattern = '\n'
        if re.search(not_between_pattern, self.sql, re.IGNORECASE ):                 # 脚本存在此异常
            for i in re.finditer(not_between_pattern, self.sql, re.IGNORECASE):    # 统计匹配结果字符前所有换行符'\n',即为行数
                row_num = len(re.findall(blank_pattern, self.sql[:i.start()], re.IGNORECASE))+1
                self.err_dic['not_between'].add(row_num)
        #print(f'not between 异常行数 : {self.err_dic["not_between"]}')

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
            local_table_result = re.search(local_table_pattern, create_statement.group(0), re.IGNORECASE)     # 判断是否是临时表，即是否存在关键字 local temporary...
            commit_result = re.search(commit_pattern, create_statement.group(0), re.IGNORECASE)               # 判断是否存在关键字 on commit rows

            if local_table_result and not commit_result:
                row_num_local = len(re.findall(blank_pattern, self.sql[:create_statement.start()], re.IGNORECASE)) + 1    # 统计 create 段所处行数
                row_num_commit = len(re.findall(blank_pattern, create_statement.group(0)[:local_table_result.start()],
                                              re.IGNORECASE))
                row_num = row_num_local + row_num_commit
                self.err_dic['no_on_commit_preserve_rows'].add(row_num)
            else:
                pass
        #print(f'no on commit error 异常行数 : {self.err_dic["no_on_commit_preserve_rows"]}')

    def join_locate(self):
        select_pattern = 'select(.|\n)+?;'   # 匹配 select...; 之间的内容，注意惰性匹配
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
                                                re.IGNORECASE)) + 1                                # 统计 select 行数

                join_result = re.search(join_pattern, select_statement.group(0))
                row_num_join = len(re.findall(blank_pattern,
                                              select_statement.group(0)[:join_result.start()]))  # 计算 join 在段内偏移, 不用加 1

                row_num = row_num_select + row_num_join  # distinct 所处行数
                self.err_dic['join_no_outer_inner'].add(row_num)
            else:
                pass
        #print(f'join_no_outer_inner error 异常行数 : {self.err_dic["join_no_outer_inner"]}')

    '''
        创建多临时表异常。
    '''
    '''
        完成
    '''
    def multi_tmp_table_locate(self):
        create_tmp_pattern = 'create.+?local.+?temporary'
        blank_pattern = '\n'
        create_tmp_result = re.finditer(create_tmp_pattern, self.sql, re.IGNORECASE)
        for create_tmp_statement in create_tmp_result:
            row_num = len(re.findall(blank_pattern, self.sql[:create_tmp_statement.start()], re.IGNORECASE)) + 1  #　统计创建临时表行数
            self.err_dic['create_multi_tmp_table'].add(row_num)      # 需要统计列表内容是否大于2

            # 若大于2，则输出所有临时表行数
        #print(f'多临时表 异常行数 : {self.err_dic["create_multi_tmp_table"]}')

    '''
        操作多目标表,
        返回所有操作目标表的行数
    '''
    def manipulate_multi_target_table_locate(self):
        blank_pattern = '\n'
        mani_target_table = set()
        if len(self.target_table_name['delete']) > 0:
            for delete_target_table_name in self.target_table_name['delete']:
                delete_pattern = f'delete(.|\n)+{delete_target_table_name}(.|\n)+?;'
                delete_result = re.search(delete_pattern, self.sql, re.IGNORECASE)
                row_num = len(re.findall(blank_pattern, self.sql[:delete_result.start()], re.IGNORECASE)) + 1
                mani_target_table.add(row_num)
                #print(f'delete target table error 异常行数 : {row_num}')

        if len(self.target_table_name['update']) > 0:
            for update_target_table_name in self.target_table_name['update']:
                update_pattern = f'update(.|\n)+{update_target_table_name}(.|\n)+?;'
                update_result = re.finditer(update_pattern, self.sql, re.IGNORECASE)
                for update_ in update_result:
                    row_num = len(re.findall(blank_pattern, self.sql[:update_.start()], re.IGNORECASE)) + 1
                    mani_target_table.add(row_num)
                    #print(f'update target table error 异常行数 : {row_num}')

        if len(self.target_table_name['insert']) > 0:
            for insert_target_table_name in self.target_table_name['insert']:
                insert_pattern = f'insert\s+?into\s+{insert_target_table_name}'
                insert_result = re.finditer(insert_pattern, self.sql, re.IGNORECASE)
                for insert_ in insert_result:
                    row_num = len(re.findall(blank_pattern, self.sql[:insert_.start()], re.IGNORECASE)) + 1
                    mani_target_table.add(row_num)
                    #print(f'insert target table error 异常行数 : {row_num}')
        #print(f'manipulate multi-target table error 异常行数 : {mani_target_table}')
        #self.err_dic['multi_target'].extend(list(mani_target_table))
        self.err_dic['multi_target'] |= set(list(mani_target_table))

    '''
        多次写入目标表
    '''
    '''
        完成
    '''
    def multi_insert_target(self):
        blank_pattern = '\n'
        multi_insert_target_row = set()
        for multi_insert_target in self.target_table_name['insert']:
            insert_pattern = f'insert\s+?into\s+{multi_insert_target}'
            multi_insert_result = re.finditer(insert_pattern, self.sql, re.IGNORECASE)
            if len(re.findall(insert_pattern, self.sql, re.IGNORECASE)) > 1:
                for insert_ in multi_insert_result:
                    row_num = len(re.findall(blank_pattern, self.sql[:insert_.start()], re.IGNORECASE)) + 1
                    multi_insert_target_row.add(row_num)
            else:
                pass
        #self.err_dic['multi_insert_target'].extend(list(multi_insert_target_row))
        self.err_dic['multi_insert_target'] |= set(list(multi_insert_target_row))
        #print(f'multi-insert target table error 异常行数 : {multi_insert_target_row}')

    '''
        update 目标表
        接收err_detect传递的update与目标表名信息，检测update段。
    '''
    '''
        完成
        修正1：update同一目标表多次。改用finditer
        修正2：惰性匹配update语句。
    '''
    def update_target_locate(self):
        blank_pattern = '\n'
        for target_table_name in self.target_table_name['update']:
            update_pattern = f'update(.|\n)+?{target_table_name}(.|\n)+?;'  # 提取update目标表达的语句。
            update_result = re.finditer(update_pattern, self.sql, re.IGNORECASE)
            for update_ in update_result:
                row_num = len(re.findall(blank_pattern, self.sql[:update_.start()], re.IGNORECASE)) + 1
                if row_num not in self.err_dic['update_target']:
                    self.err_dic['update_target'].add(row_num)
    '''
        未显式赋值 etl_tms
        1、定位 insert target—table 语句
        2、检测 insert 语句是否包含 etl_tms 而不包含 sysdate
    '''
    '''
        完成
    '''
    def explicit_etl_tms_locate(self):
        etl_tms_pattern = 'etl.*tms'
        sysdate_pattern = 'sysdate'
        blank_pattern = '\n'
        for insert_target_table in self.target_table_name['insert']:
            insert_pattern = f'insert\s+?into\s+{insert_target_table}(.|\n)*?;'
            for insert_statement in re.finditer(insert_pattern, self.sql, re.IGNORECASE):
                etl_tms_ = re.search(etl_tms_pattern, insert_statement.group(0), re.IGNORECASE)
                sysdate_ = re.search(sysdate_pattern, insert_statement.group(0), re.IGNORECASE)
                if etl_tms_ and not sysdate_:
                    row_num = len(re.findall(blank_pattern, self.sql[:insert_statement.start()], re.IGNORECASE)) + 1
                    self.err_dic['etl_tms'].add(row_num)
        #print(f'etl-tms no sysdate error 异常行数 : {self.err_dic["etl_tms"]}')

    '''
        替换正则表达式中的特殊字符
    '''
    def to_regular(self, pattern):
        return pattern.replace('*','\*').replace('+','\+').replace('$','\$').replace('.', '\.')

    '''
        insert|select|create未显式提供字段名。
        定位方式：
                err_detector传递检测结果，更具结果在原文定位。
                {
                    'create':( bool(是否异常), 'tmp_table_name'),
                    'insert':( bool(是否异常), 'target_table_name')
                }
                
    '''

    '''
        修改，存在表名为其他表名子集情况。
        解决方式：findall
    '''
    def explicit_field_locate(self):
        blank_pattern = '\n'
        if len(self.implicit_field['create']) > 0:
            for create_tmp_statement in self.implicit_field['create']:
                create_tmp_pattern = f'create\s+local.*?{self.to_regular(create_tmp_statement)}'
                create_result = re.finditer(create_tmp_pattern, self.sql, re.IGNORECASE)            # 找出所有满足的创建语句
                for create_ in create_result:
                    row_num_create = len(re.findall(blank_pattern, self.sql[:create_.start()], re.IGNORECASE)) + 1            #　创建临时表未显示指定字段
                    if row_num_create not in self.err_dic['explicit_field']:
                        self.err_dic['explicit_field'].add(row_num_create)

        if len(self.implicit_field['insert']) > 0:
            for insert_statement in self.implicit_field['insert']:
                insert_target_pattern = f'insert\s+?into\s+?{self.to_regular(insert_statement)}'
                insert_result = re.search(insert_target_pattern, self.sql, re.IGNORECASE)
                row_num_insert = len(re.findall(blank_pattern, self.sql[:insert_result.start()], re.IGNORECASE)) + 1
                self.err_dic['explicit_field'].add(row_num_insert)
        #print(f'implicit field 异常行数 : {self.err_dic["explicit_field"]}')
        '''
        if self.implicit_field['create']:
            create_tmp_pattern = f'create\s+local.*?{self.implicit_field["create"][1]}'

            create_result = re.search(create_tmp_pattern, self.sql, re.IGNORECASE)

            row_num_create = len(re.findall(blank_pattern, self.sql[:create_result.start()], re.IGNORECASE)) + 1            #　创建临时表未显示指定字段
            self.err_dic['explicit_field'].append(row_num_create)
        if self.implicit_field['insert']:
            insert_target_pattern = f'insert\s+?into\s+?{self.implicit_field["insert"][1]}'
            insert_result = re.search(insert_target_pattern, self.sql, re.IGNORECASE)
            row_num_insert = len(re.findall(blank_pattern, self.sql[:insert_result.start()], re.IGNORECASE)) + 1
            self.err_dic['explicit_field'].append(row_num_insert)
        #print(f'implicit field 异常行数 : {self.err_dic["explicit_field"]}')
        '''
    '''
        where字段存在函数
        接收err_detector传递的函数检测结果，重回原文定位函数位置。PS：可能存在误检(注释部分、select部分等)
        
        定位检测结果依赖于检测，待修正。
    '''
    def where_exist_func_locate(self):
        blank_pattern = '\n'
        for func_ in self.where_function['function']:
            function_pattern = f'{func_}'.replace('(', '\\(').replace(')','\\)')

            func_result = re.finditer(function_pattern, self.sql, re.IGNORECASE)
            #print(re.findall(tmp, self.sql, re.IGNORECASE))

            for func_result_ in func_result:

                row_num = len(re.findall(blank_pattern, self.sql[:func_result_.start()], re.IGNORECASE)) + 1
               # multi_insert_target_row.add(row_num)
                self.err_dic['where_exist_function'].add((func_, row_num))
        #print(f'where字段带函数 异常行数 : {self.err_dic["where_exist_function"]}')


    def execute(self):
        self.remove_annotation()

        self.select_locate()
        self.count_locate()
        self.distinct_locate()
        self.case_else_locate()
        self.join_locate()
        self.not_between_locate()
        self.commit_preserve_rows_locate()

        if len(self.target_table_name['update']) > 0:
            self.update_target_locate()
        target_name = self.target_table_name['delete'] | self.target_table_name['insert'] | self.target_table_name['update']
        if len(target_name) > 1:
            self.manipulate_multi_target_table_locate()   #　操作目标表数大于1

        self.multi_tmp_table_locate()
        self.multi_insert_target()

        self.explicit_etl_tms_locate()
        if self.where_function['isExist']:
            self.where_exist_func_locate()

        self.explicit_field_locate()
        #print(self.err_dic)


    def clear(self):
        self.err_dic = self.err_define.err_dic.copy()

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