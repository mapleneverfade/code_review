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

class code_review():
    def __init__(self):
        self.parser = Options().parse()
        self.detector = load_cut_statement()
        self.err = error_detect()

    def run(self):
        if self.parser.folder:
            file_sql = os.listdir(self.parser.foldername)   # 判断是否检测整个文件夹。
            for i in file_sql:
                self.execute(i)
        else:
            file_sql = self.parser.filename
            self.execute(file_sql)

    def execute(self, filename):
        print('********{} 检测开始********'.format(filename))
        self.err.clear()
        self.detector.load_sql(os.path.join(self.parser.foldername, filename))
        self.detector.split_to_statement()
        self.err.get_statement(self.detector.statement)
        self.err.global_exception_detect()
        self.err.print_exception()
        print('********{} 检测结束********'.format(filename))



if __name__=='__main__':

    main = code_review()
    main.run()
    '''
    parser = Options().parse()
    if parser.folder :
        file_sql = os.listdir(parser.foldername)
    else:
        file_sql = parser.filename

    print(file_sql)
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
	
    '''

