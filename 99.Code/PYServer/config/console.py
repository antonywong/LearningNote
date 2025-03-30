# -*- coding: utf-8 -*-

from dal import mssql


class Console:
    def __init__(self):
        sql = f"SELECT id,value FROM Console"
        data = {row['id']: row['value'] for row in mssql.queryAll(sql)}

        self.POSITION_RATE = float(data["POSITION_RATE"])
        self.DELTA_TOLERANCE = float(data["DELTA_TOLERANCE"])
