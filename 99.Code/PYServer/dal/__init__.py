#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import config


def query(sql, dbFile = config.sqliteFile):
    conn = sqlite3.connect(dbFile)
    cu = conn.cursor()
    cu.execute(sql)
    conn.close()
    return cu


def queryAll(sql, dbFile = config.sqliteFile):
    conn = sqlite3.connect(dbFile)
    cu = conn.cursor()
    cu.execute(sql)
    result = cu.fetchall()
    cu.close()
    conn.close()
    return result


def run(sql, dbFile = config.sqliteFile):
    conn = sqlite3.connect(dbFile)
    cu = conn.cursor()
    cu.execute(sql)
    conn.commit()
    result = cu.rowcount
    cu.close()
    conn.close()
    return result