#-*-utf-8-*-
import os
import re
from utils.load_and_cut import load_cut_statement
from err.err_detect import error_detect
import err.err_detect
from options import Options

'''
    扫描parser.foldername目录下的所有文本，输出扫描结果。
    
    例如: python main.py --foldername 'c://test//'
'''
if __name__=='__main__':

    parser = Options().parse()
    if parser.folder :
        file_sql = os.listdir(parser.foldername)

    filename = 'D:\\项目管理\\venv\\test\\tmp_1.sql'
    '''
    detector = load_cut_statement()

    detector.load_sql(filename)
    detector.split_to_statement()

    err = error_detect()
    err.get_statement(detector.statement)  #传入statement
    err.global_exception_detect()            #异常检测
    err.print_exception()                    #输出异常
    '''


    detector = load_cut_statement()
    err = error_detect()
    for i in file_sql:
        print('检测文本 ：{}'.format(i))
        err.clear()
        detector.load_sql(os.path.join(parser.foldername,i))
        detector.split_to_statement()
        err.get_statement(detector.statement)
        err.global_exception_detect()
        err.print_exception()
        print('{}检测结束！'.format(i))



   # print(err.target_table_statement)  #脚本中的保存目标表语句。
	


