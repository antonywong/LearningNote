# -*- coding: utf-8 -*-
from dal import mssql

consts = mssql.queryAll(f"SELECT [key],[value] FROM Const")
DICT = {c["key"]: c["value"] for c in consts}