# -*- coding: utf-8 -*-
import pymssql
import config


def query(sql):
    return


def queryAll(sql):
    result = []
    c = config.mssqlConnStr
    with pymssql.connect(c[0], c[1], c[2], c[3]) as conn:
        with conn.cursor(as_dict=True) as cursor:   # 数据存放到字典中
            cursor.execute(sql)
            for row in cursor:
                result.append(row)
    return result


def run(*sqls):
    # 如果参数只有一个，且是字符串类型，则将其转换为列表
    if len(sqls) == 1 and isinstance(sqls[0], str):
        sqls = [sqls[0]]

    c = config.mssqlConnStr
    with pymssql.connect(c[0], c[1], c[2], c[3]) as conn:
        with conn.cursor() as cursor:
            for sql in sqls[0]:
                #print(sql)
                cursor.execute(sql)
            conn.commit()