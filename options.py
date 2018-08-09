#-*- coding:utf-8-*-
import argparse
import os
'''
    命令行控制options
'''
class Options():
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.initialized = False

    def initialize(self):
        self.parser.add_argument('--folder',default=False)
        self.parser.add_argument('--foldername', type=str, default='./test')
        self.parser.add_argument('--filename', type = str, default='./test/tmp_1.sql')

    def parse(self):
        if not self.initialized:
            self.initialize()
            self.opt = self.parser.parse_args()
            args = vars(self.opt)
        for k,v in sorted(args.items()):
            print('%s: %s'%(str(k), str(v)))
        return self.opt