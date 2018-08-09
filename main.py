#-*-utf-8-*-
import os
import re

from utils.load_and_cut import load_cut_statement
from err.err_detect import error_detect
import err.err_detect

if __name__=='__main__':

    filename = 'D:\\项目管理\\venv\\test\\tmp_1.sql'
    detector = load_cut_statement()

    detector.load_sql(filename)
    detector.split_to_statement()

    err = error_detect()
    err.get_statement(detector.statement)  #传入statement
    err.global_exception_detect()            #异常检测
    err.print_exception()                    #输出异常

    print(err.target_table_statement)  #脚本中的保存目标表语句。
	


