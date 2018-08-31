# SQL代码扫描说明
### 1、主程序main.py检测SQL代码禁止语法。
### 2、err目录中err_define、err_detect、err_print、err_locate
### 分别禁止语法的定义、检测、输出、定位文件
### 3、options定义传递给main.py的参数
    --folderName指定待检测SQL脚本目录路径，默认为 './test'
    --dstPath 指定输出文件路径，默认为 './result/检测结果.txt'
#### 例如，待检测SQL脚本存放于目录C://sql,指定检测结果存放于 C://result
    python main.py --folderName c://sql --dstPath c://result