# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import gc
from sqlalchemy import create_engine
import sqlite3
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from _datetime import time

# %%
output_all_conn = sqlite3.connect(
    '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_all_1117.db')
output_all_c = output_all_conn.cursor()

output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_weather_1117.db" AS output_weather')
output_all_conn.commit()

output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_speed_1117.db" AS output_speed')
output_all_conn.commit()

output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_crash_1117.db" AS output_crash')
output_all_conn.commit()

output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/output/output_info_1117.db" AS output_info')
output_all_conn.commit()

# %%
# The above is 2014 data, now I try to combine them with 2015_17 data
output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_weather_1117.db" AS output_15weather')
output_all_conn.commit()

output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_speed_1117.db" AS output_15speed')
output_all_conn.commit()

output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_crash_1117.db" AS output_15crash')
output_all_conn.commit()

output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_info_1117.db" AS output_15info')
output_all_conn.commit()

# %%
# %%time

# create index for matching year 15-17
output_all_c.execute("""
--sql
create index if not exists output_15weather.id_output_weather_id_time 
on output_weather(wzID,wzTime_divided_stamp);
""")
output_all_conn.commit()

output_all_c.execute("""
--sql
create index if not exists output_15speed.id_speed_xy_61_id_time_loc 
on speed_xy_61(wzID,wzTime_divided_stamp,location);
""")
output_all_conn.commit()

output_all_c.execute("""
--sql
create index if not exists output_15speed.id_speed_xy_518_id_time_loc 
on speed_xy_518(wzID,wzTime_divided_stamp,location);
""")
output_all_conn.commit()

output_all_c.execute("""
--sql
create index if not exists output_15crash.id_crash_xy_61_id_time_loc 
on crash_xy_61(wzID,wzTime_divided_stamp,location);
""")
output_all_conn.commit()

output_all_c.execute("""
--sql
create index if not exists output_15crash.id_crash_xy_518_id_time_loc 
on crash_xy_518(wzID,wzTime_divided_stamp,location);
""")
output_all_conn.commit()

output_all_c.execute("""
--sql
create index if not exists output_15info.id_wzs_info_id_time_loc 
on wzs_info(wzID,wzTime_divided_stamp,location);
""")
output_all_conn.commit()

# %%
# %%time
# try joining with index
# CPU times: user 8 ms, sys: 4 ms, total: 12 ms
# Wall time: 210 ms
temp = pd.read_sql("""
--sql
SELECT wzs_info.*,
wzs_info.wzID as wzID_new,
output_15weather.output_weather.AveT,
output_15weather.output_weather.AveP,
 output_15weather.output_weather.AveW,
output_15speed.speed_xy_61.real_speed_61,
output_15speed.speed_xy_61.historical_speed_61, 
output_15speed.speed_xy_61.free_speed_61,
output_15speed.speed_xy_518.real_speed_518,
output_15speed.speed_xy_518.historical_speed_518, 
output_15speed.speed_xy_518.free_speed_518,
output_15crash.crash_xy_61.crash_61,
output_15crash.crash_xy_61.crash_severe_61,
output_15crash.crash_xy_518.crash_518,
output_15crash.crash_xy_518.crash_severe_518
FROM output_15info.wzs_info 

LEFT JOIN
output_15weather.output_weather
ON
output_15info.wzs_info.wzID = output_15weather.output_weather.wzID
AND
output_15info.wzs_info.wzTime_divided_stamp = output_15weather.output_weather.wzTime_divided_stamp

LEFT JOIN
output_15speed.speed_xy_61
ON
output_15info.wzs_info.wzID = output_15speed.speed_xy_61.wzID
AND
output_15info.wzs_info.wzTime_divided_stamp = output_15speed.speed_xy_61.wzTime_divided_stamp
AND
output_15info.wzs_info.location = output_15speed.speed_xy_61.location


LEFT JOIN
output_15speed.speed_xy_518
ON
output_15info.wzs_info.wzID = output_15speed.speed_xy_518.wzID
AND
output_15info.wzs_info.wzTime_divided_stamp = output_15speed.speed_xy_518.wzTime_divided_stamp
AND
output_15info.wzs_info.location = output_15speed.speed_xy_518.location

LEFT JOIN
output_15crash.crash_xy_61
ON
output_15info.wzs_info.wzID = output_15crash.crash_xy_61.wzID
AND
output_15info.wzs_info.wzTime_divided_stamp = output_15crash.crash_xy_61.wzTime_divided_stamp
AND
output_15info.wzs_info.location = output_15crash.crash_xy_61.location

LEFT JOIN
output_15crash.crash_xy_518
ON
output_15info.wzs_info.wzID = output_15crash.crash_xy_518.wzID
AND
output_15info.wzs_info.wzTime_divided_stamp = output_15crash.crash_xy_518.wzTime_divided_stamp
AND
output_15info.wzs_info.location = output_15crash.crash_xy_518.location
limit 100;""", output_all_conn)
