#-*-utf-8-*-
import os
import re
from utils.load_and_cut import load_cut_statement
from err.err_detect import error_detect
import err.err_detect
from options import Options
from err.test_reconstruct import error_detection, err_printer, detector

import types

'''
    扫描parser.foldername目录下的所有文本，输出扫描结果。
    
    例如: python main.py --foldername 'c://test//'
'''

class Run():
    def __init__(self):
        pass
    def run(self):
        pass
    def __call__(self):
        self.run()

class code_review():
    def __init__(self):
        self.parser = Options().parse()
        self.detector = load_cut_statement()
        self.err = error_detect()

    def run(self):
        if self.parser.isFolder:

            file_sql = os.listdir(self.parser.foldername)   # 判断是否检测整个文件夹。
            for i in file_sql:
                self.execute(os.path.join(self.parser.foldername,i))
        else:
            file_sql = self.parser.filename
            self.execute(file_sql)

    def execute(self, filename):
        print('********{} 检测开始********'.format(filename))
        self.err.clear()                                         # 清空err_detect类变量。
        self.detector.load_sql(filename)                         # 导入SQL脚本
        self.detector.split_to_statement()                       # 分割SQL语句
        self.err.get_statement(self.detector.statement)
        self.err.global_exception_detect()                       # 检测异常语法。
        self.err.print_exception()                               # 输出检测结果。
        print('********{} 检测结束********\n'.format(filename))


'''
    测试是否parser.isFolder 布尔类型bug
'''
import os
if __name__=='__main__':
    parser = Options().parse()
    folderpath = parser.foldername
    dst_path = 'C:\\Users\\chenchangyu\\Desktop\\测试屋\\test.txt'
    filelist = os.listdir(folderpath)
    try:
        for file in filelist:
            sql = ''
            with open(os.path.join(folderpath, file), 'rb') as f:
                for line in f:
                    pattern = '--.*?\n'                             # 匹配注释段
                    i = re.sub(pattern, '', line.decode('utf8'))    # 剔除注释
                    sql = f"{sql} {i.strip()}"
            statement = sql.split(';')
            detect = detector(sql, statement)
            detect.detect()

            p = err_printer(dst_path, detect.global_exception, file)
            p.print_to_file()
    except :
            print('Error accur!')



