#-*- coding:utf8 -*-
'''
    输出检测错误、写文件。
    类接收参数 ： 输出文件路径 、err_detector检测结果、 文件名
    err_printer.print_to_file   函数负责写结果到文件。
    err_printer.print_to_screen 函数负责显示结果。
'''
class err_printer():
    def __init__(self, dst_filename, global_exception, sql_file_name):
        self.flag = False
        self.dst_filename       =   dst_filename                      # 异常输出文件名
        self.global_exception   =   global_exception                  # 传入异常检测结果
        self.sql_file_name = sql_file_name
    #   输出异常结果至文件。
    def print_to_file(self):  # 输出异常检测结果到文件。
        with open(self.dst_filename, 'a') as f:
            f.write(f'脚本<{self.sql_file_name}>  <异常事项 ')
            if self.global_exception['select *']:
                self.flag = True
                f.write('1、')
            if self.global_exception['count *']:
                self.flag = True
                f.write('2、')
            if self.global_exception['flag_distinct']:
                self.flag = True
                f.write('3、')
            if self.global_exception['case_no_else']:
                self.flag = True
                f.write('4、')
            if self.global_exception['explicit_field']:  # 创建表脚本略过检测该项
                if not (self.global_exception['multi_target'] >= 0 and self.global_exception['create_multi_tmp_table']==0):
                    self.flag = True
                    f.write('5、')
            if self.global_exception['where_exist_function']:
                self.flag = True
                f.write('6、')
            if self.global_exception['update_target']:     #创建表脚本略过检测该项
                if not (self.global_exception['multi_target'] >= 0 and self.global_exception['create_multi_tmp_table']==0):
                    self.flag = True
                    f.write('7、')
            if self.global_exception['create_multi_tmp_table'] > 2 and not self.global_exception['drop_tmp_table']:
                f.write('8、')
                self.flag = True
            if self.global_exception['create_multi_tmp_table'] > 3:
                self.flag = True
                f.write('9、')
            if self.global_exception['no_on_commit_preserve_rows']:
                self.flag = True
                f.write('10、')
            if self.global_exception['etl_tms']:
                f.write('11、')
                self.flag = True
            if self.global_exception['multi_insert_target'] > 1:
                f.write('12、')
                self.flag = True
            if self.global_exception['multi_target'] > 1:
                f.write('13、')
                self.flag = True
            if self.global_exception['join_no_outer_inner']:
                f.write('14、')
                self.flag = True
            if self.global_exception['not_between']:
                f.write('15、')
                self.flag = True
            if not self.flag:
                f.write(' 无')
            f.write('>\n')

    # 输出检测结果到屏幕
    def print_to_screen(self):
        print(f'脚本<{self.sql_file_name}>  <异常事项 ')
        if self.global_exception['select *']:
            print('1、')
        if self.global_exception['count *']:
            print('2、')
        if self.global_exception['flag_distinct']:
            print('3、')
        if self.global_exception['case_no_else']:
            print('4、')
        if self.global_exception['explicit_field']:
            print('5、')
        if self.global_exception['where_exist_function']:
            print('6、')
        if self.global_exception['update_target']:
            print('7、')
        if self.global_exception['create_multi_tmp_table'] > 2 and not self.global_exception['drop_tmp_table']:
            print('8、')
        if self.global_exception['create_multi_tmp_table'] > 3:
            print('9、')
        if self.global_exception['no_on_commit_preserve_rows']:
            print('10、')
        if self.global_exception['etl_tms']:
            print('11、')
        if self.global_exception['multi_insert_target'] > 1:
            print('12、')
        if self.global_exception['multi_target'] > 1:
            print('13、')
        if self.global_exception['join_no_outer_inner']:
            print('14、')
        if self.global_exception['not_between']:
            print('15、')
        print('>\n')

    def __call__(self):
        self.output()