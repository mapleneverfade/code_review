#-*-utf-8-*-
import os
import utils.banVoc as ban
import utils.tools as tool
import re

class code_viewer():
    def __init__(self, sql):
        self.sql = sql

    def run(self):
        ban.test_select(self.sql)
        ban.count_temp_table(self.sql)
        ban.count_target_table(self.sql)
        ban.count_distinct(self.sql)


if __name__=='__main__':

    filename = 'D:\\项目管理\\venv\\test\\tmp_1.sql'
    sql = tool.load_sql_file(filename)

    checker = code_viewer(sql)
    checker.run()
    print('hello neo!')
	


