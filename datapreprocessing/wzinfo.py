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
output_info_conn = sqlite3.connect(
    '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_info_1117.db')
output_info_c = output_info_conn.cursor()

# %%
# wz info source 1: wz_loc_db.pid_speed_limit
output_info_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_loc.db" AS wz_loc_db')
output_info_conn.commit()

# wz info source 2: wz_output_old.wzoutput_15_17 -- everything except for speed-limit and aadt_new;
# wz_output_old.wzAADT -- aadt_new;

output_info_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db" AS wz_output_old')
output_info_conn.commit()

output_info_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_weather_1117.db" AS output_weather')
output_info_conn.commit()

# %%
# create index for wz_loc_db.pid_speed_limit
output_info_c.execute("""
--sql
create index if not exists wz_loc_db.pid_speed_limit_pid 
on pid_speed_limit(pennshids);
""")
output_info_conn.commit()

# %%
# %%time
# query output
query_string = """
--sql
select wz_output_old.wzoutput_15_17.wzID,wz_output_old.wzoutput_15_17.Control,
CAST( wz_output_old.wzoutput_15_17.wzTime_divided_stamp as INT) as wzTime_divided_stamp,
wz_output_old.wzoutput_15_17.location ,wz_output_old.wzoutput_15_17.closure ,  wz_output_old.wzoutput_15_17.LaneCounts ,  wz_output_old.wzoutput_15_17.AADT ,  wz_output_old.wzoutput_15_17.NHS_IND ,  wz_output_old.wzoutput_15_17.PA_BYWAY_I ,  wz_output_old.wzoutput_15_17.duration ,  wz_output_old.wzoutput_15_17.WeekdayofWeek,  wz_output_old.wzoutput_15_17.Month,  wz_output_old.wzoutput_15_17.DaytimeofDay,  wz_output_old.wzoutput_15_17.sequence_0,  wz_output_old.wzoutput_15_17.sequence_1,  wz_output_old.wzoutput_15_17.sequence_2,  wz_output_old.wzoutput_15_17.sequence_3,  wz_output_old.wzoutput_15_17.sequence_4, wz_output_old.wzoutput_15_17.treatment_new,  wz_output_old.wzoutput_15_17.NUM_inters ,  wz_output_old.wzoutput_15_17.NUM_ramps ,  wz_output_old.wzoutput_15_17.NetLength ,  wz_output_old.wzoutput_15_17.Year,
wzid_speedlimit.speed_limit,
CASE
    WHEN wzoutput_15_17.Year=2014 THEN wzAADT.AADT_14
    WHEN wzoutput_15_17.Year=2015 THEN wzAADT.AADT_15
    WHEN wzoutput_15_17.Year=2016 THEN wzAADT.AADT_16
    WHEN wzoutput_15_17.Year=2017 THEN wzAADT.AADT_17
    END AADT_new
from wz_output_old.wzoutput_15_17 
left join 
(select output_weather.wzid_pid.wzID, wz_loc_db.pid_speed_limit.speed_limit
from output_weather.wzid_pid 
left join wz_loc_db.pid_speed_limit
on output_weather.wzid_pid.PennShID =  wz_loc_db.pid_speed_limit.pennshids
) wzid_speedlimit

on wz_output_old.wzoutput_15_17.wzID = wzid_speedlimit.wzID
 LEFT JOIN 

wz_output_old.wzAADT ON wz_output_old.wzoutput_15_17.wzID = wz_output_old.wzAADT.wzID WHERE wz_output_old.wzAADT.year=15
;
"""
temp = pd.read_sql("" + query_string[:-2] + " limit 10000", output_info_conn)
temp = pd.read_sql("explain query plan " + query_string[:-2] + " limit 10000", output_info_conn)
# %%
# %%time
# create table for wzs_info
output_info_c.execute("create table wzs_info AS " + query_string)
output_info_conn.commit()

# %%
