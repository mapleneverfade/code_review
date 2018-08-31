#-*-utf-8-*-
import os
from utils.load_and_transform import load_sql
from options import Options
from err.err_detect import err_detector
from err.err_print import err_printer
from err.err_locate import err_locater
'''
    扫描parser.foldername目录下的所有文本，输出扫描结果。
    
    例如: python main.py --folderName 'c://test//'
'''
class code_review():
    def __init__(self):
        self.loader = load_sql()
        self.parser = Options().parse()
        self.detector = err_detector()
        self.printer = None

    def run(self):
        print("************ 检测开始 ************")
        filelist = list(filter(lambda x:x.endswith('sql'), os.listdir(self.parser.folderName)))    # 过滤非 .sql 文件
        if len(filelist)==0:
            raise(Exception('未检测到 .sql 文件 ！'))

        for file in filelist:
            print('********{} 检测中 ********\n'.format(file))
            filepath = os.path.join(self.parser.folderName, file)
            sql = self.loader.load_delete_note(filepath)                          # 导入去注释SQL文本


            statement = sql.split(';')
            #self.detector = err_detector(sql, statement)
            self.detector.sql, self.detector.statement = sql, statement         # detector接收去注释的sql文本与分割后的语句
            self.detector.detect()

            param_to_locater = (self.loader.load_sql_origin(filepath), self.detector.manipulate_target, self.detector.global_exception, self.detector.where_func, self.detector.implicit_field)
            locater = err_locater(*param_to_locater)    # locater接收原脚本文件
            locater.execute()                           # 每次循环都实例化一个新的locater



            self.printer = err_printer(self.parser.dstPath, self.detector.global_exception, file, locater.err_dic)
            self.printer.print_to_file()
            self.detector.clear()
        print('************ 检测结束 ************')

'''
    测试是否parser.isFolder 布尔类型bug
'''


if __name__=='__main__':
    main = code_review()
    main.run()



	print('test of git')
	print('new branch')