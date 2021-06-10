#!/usr/bin/env python3
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


def run(sql):
    c = config.mssqlConnStr
    with pymssql.connect(c[0], c[1], c[2], c[3]) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()