# -*- coding: utf-8 -*-

from dal import mssql


class Console:
    def __init__(self):
        sql = f"SELECT id,value FROM Console"
        self.data = {row['id']: row['value'] for row in mssql.queryAll(sql)}

        self.DELTA_TOLERANCE = float(self.data["DELTA_TOLERANCE"])


    def get_position_rate(self, account: str) -> float:
        return float(self.data[f"POSITION_RATE_{account}"])
    def set_position_rate(self, account: str, value: float):
        sql = [f"UPDATE Console SET value='{value}' WHERE id='POSITION_RATE_{account}'"]
        mssql.run(sql)
        self.data[f"POSITION_RATE_{account}"] = value


    def get_balance(self, account: str) -> float:
        return float(self.data[f"BALANCE_{account}"])
