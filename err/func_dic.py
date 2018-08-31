# -*- utf-8 -*-
import re
import sys

'''
    程序以字典形式记录mysql、vertica、hive所有函数函数名。

'''
function = {
    'MySQL': [
        'ABS', 'CEIL', 'CEILING', 'FLOOR', 'RAND', 'SIGN', 'PI', 'TRUNCATE', 'ROUND', 'POW', 'POWER'
                                                                                             'SQRT', 'EXP', 'MOD',
        'LOG', 'LOG10', 'RADIANS', 'DEGREES', 'SIN', 'ASIN', 'COS', 'ACOS',
        'TAN', 'ATAN', 'ATAN2', 'COT',
        'CHAR_LENGTH', 'LENGTH', 'CONCAT', 'CONCAT_WS', 'INSERT', 'UPPER', 'LOWER', 'LCASE', 'LEFT',
        'RIGHT', 'LPAD', 'RPAD', 'LTRIM', 'RTRIM', 'TRIM', 'REPEAT', 'SPACE', 'REPLACE', 'STRCMP',
        'SUBSTRING', 'MID', 'LOCATE', 'POSITION', 'INSTR', 'REVERSE', 'ELT', 'EXPORT_SET', 'FIELD',
        'FIND_IN_SET', 'MAKE_SET', 'SUBSTRING_INDEX', 'LOAD_FILE',
        'CURDATE', 'CURRENT_DATE', 'CURTIME', 'CURRENT_TIME', 'NOW', 'CURRENT_TIMESTAMP', 'LOCALTIME',
         'LOCALTIMESTAMP', 'UNIX_TIMESTAMP', 'FROM_UNIXTIME', 'UTC_DATE', 'UTC_TIME',
        'MONTH', 'MONTHNAME', 'DAYNAME', 'DAYOFWEEK', 'WEEKDAY', 'WEEK', 'WEEKOFYEAR', 'DAYOFYEAR',
        'DAYOFMONTH', 'QUARTER', 'HOUR', 'MINUTE', 'SECOND', 'EXTRACT', 'TIME_TO_SEC', 'SEC_TO_TIME',
        'TO_DAYS', 'FROM_DAYS', 'DATEDIFF', 'ADDDATE', 'DATE_ADD', 'SUBDATE', 'ADDTIME', 'SUBTIME',
        'DATE_FORMAT', 'TIME_FORMAT', 'GET_FORMAT',
         'IFNULL', 'VERSION', 'CONNECTION_ID', 'DATABASE', 'SCHEMA', 'USER', 'SYSTEM_USER',
        'SESSION_USER', 'CURRENT_USER', 'CURRENT_USER', 'CHARSET', 'COLLATION', 'LAST_INSERT_ID',
        'PASSWORD', 'md5', 'ENCODE', 'DECODE', 'FORMAT', 'INET_ATON', 'INET_NTOA', 'GET_LOCK',
        'IS_FREE_LOCK', 'RELEASE_LOCK', 'BENCHMARK', 'CHARSET', 'CAST', 'CONVERT'
    ],

    'Vertica': [
        'truc', 'random', 'greatest', 'substr', 'to_char', 'day', 'month', 'year', 'week', 'quarter',
        'ln', 'least', 'isnull', 'ascii', 'chr', 'lpad', 'rpad','to_number','nullif'
    ],

    'Hive': [
        'log2', 'bin', 'hex', 'unhex', 'conv', 'abs', 'pmod', 'positive', 'negative', 'from_unixtime',
        'unix_timestamp', 'to_date', 'date_sub', 'COALESCE', 'ucase', 'regexp_replace', 'regexp_extract',
        'parse_url', 'get_json_object', 'split', 'count', 'sum', 'avg', 'min', 'max', 'var_pop', 'var_samp',
        'stddev_pop', 'stddev_samp', 'percentile', 'percentile_approx', 'histogram_numeric', 'map', 'struct',
        'array', 'size'
    ]
}
