# -*- coding: utf-8 -*-
# 隐含波动率统计

import json
from datetime import datetime, timedelta
import option
from dal import mssql


def get_new_data(codes):
    first_minute_str = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M")

    # 分钟线
    select_sql = "SELECT CONVERT(CHAR(16), day, 120) AS time,AVG(iv) AS iv FROM K LEFT JOIN OptionKGreek greek ON K.id=greek.id WHERE K.type=1 AND K.code IN ('%s') AND K.day>=CONVERT(DATETIME, '%s:00', 20) AND greek.iv IS NOT NULL AND DATEPART(HOUR,day)*100+DATEPART(MINUTE,day)<1457 GROUP BY CONVERT(CHAR(16), day, 120) ORDER BY CONVERT(CHAR(16), day, 120)"
    ivs = mssql.queryAll(select_sql % ("','".join(codes), first_minute_str))

    if ivs:
        first_minute_str = ivs[-1]["time"]
    # 最新买卖价
    select_sql = "SELECT CONVERT(CHAR(16), time, 120) AS time,AVG(iv) AS iv FROM OptionTick WHERE code IN ('%s') AND time>CONVERT(DATETIME, '%s:00', 20) AND DATEPART(HOUR,time)*100+DATEPART(MINUTE,time)<1457 GROUP BY CONVERT(CHAR(16), time, 120) ORDER BY CONVERT(CHAR(16), time, 120)"
    ivs.extend(mssql.queryAll(select_sql % ("','".join(codes), first_minute_str)))

    # 更新数据集
    new_x = [d["time"][5:].replace("-", "").replace(" ", "").replace(":", "") for d in ivs]
    new_y = [float(d["iv"]) for d in ivs]
    return new_x, new_y


def get_volume_increase(underlying: str) -> float:
    index = option.GET_UNDERLYING_INDEX(underlying)
    sql = f"""SELECT * FROM (
        SELECT CAST(day AS DATE) AS day, SUM(volume) AS volume FROM (
            SELECT day,volume,CAST(GETDATE() AS DATE) AS today, DATEADD(DAY, -7, CAST(GETDATE() AS DATE)) AS first,
            DATEPART(HOUR,GETDATE())*100 + DATEPART(MINUTE,GETDATE()) AS now
            FROM K WHERE type=1 AND code='{index}'
        ) AS t1 WHERE first<=CAST(day AS DATE) AND CAST(day AS DATE)<=today AND DATEPART(HOUR, day)*100 + DATEPART(MINUTE, day) <= now
        GROUP BY CAST(day AS DATE)
    ) t2 ORDER BY day DESC"""
    volumes = mssql.queryAll(sql)
    if len(volumes) < 2:
        return 0.0
    today = float(volumes[0]["volume"])
    before = [float(volumes[i]["volume"]) for i in range(1, len(volumes))]
    return today / sum(before) * len(before) - 1.0
