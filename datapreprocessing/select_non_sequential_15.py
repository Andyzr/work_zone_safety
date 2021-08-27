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

queryString1 = """ SELECT wzs_info.*,
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
    output_15info.wzs_info.location = output_15crash.crash_xy_518.location"""

# %%
# %%time
# select non sequential wzs
pd.read_sql("""
select * from
(""" + queryString1 + """) wz_all_old
left join
(select distinct(wzID)
from
output_15info.wzs_info
where 
output_15info.wzs_info.treatment_new>0 AND output_15info.wzs_info.Control!=0) no_sequential
on wz_all_old.wzID = no_sequential.wzID
where no_sequential.wzID is null
limit 100;

""", output_all_conn).values

# %%
# add already finished wz output
output_all_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz1117.db" AS output_wz_old')
output_all_conn.commit()

# %%
# %%time
# create needed index
output_all_c.execute("CREATE INDEX if not exists output_wz_old.id_output_14_wid on output_14(wzID);")
output_all_conn.commit()

output_all_c.execute("CREATE INDEX if not exists  output_wz_old.id_output_15_17_wid on output_15_17(wzID);")
output_all_conn.commit()

# %%
output_all_c.execute(""" create table output_15info.sequential_wzID
as  select distinct (wzID) from
output_15info.wzs_info
where 
output_15info.wzs_info.treatment_new>0 AND output_15info.wzs_info.Control!=0;""")
output_all_conn.commit()

output_all_c.execute("create index if not exists output_15info.id_sequential_wzID_wid on sequential_wzID(wzID);")
output_all_conn.commit()

# %%
# %%time
output_all_c.execute(""" create table output_info.sequential_wzID
as  select distinct (wzID) from
output_info.wzs_info
where 
output_info.wzs_info.treatment_new>0 AND output_info.wzs_info.Control!=0;""")
output_all_conn.commit()

output_all_c.execute("create index if not exists output_info.id_sequential_wzID_wid on sequential_wzID(wzID);")
output_all_conn.commit()

# %%
# %%time
# select non sequential wzs
pd.read_sql("""
select output_15_17.*
from
output_wz_old.output_15_17
left join 
output_15info.sequential_wzID
on output_wz_old.output_15_17.wzID == output_15info.sequential_wzID.wzID
where output_15info.sequential_wzID.wzID is null
limit 10000;

""", output_all_conn).wzID.value_counts()

# %%
# %%time
# select non sequential wzs
pd.read_sql("""
select wzs_info.*
from
output_15info.wzs_info
where 
output_15info.wzs_info.treatment_new>0 AND output_15info.wzs_info.Control!=0
limit 10;

""", output_all_conn)
# %%
# select * from
# output_wz_old.output_15_17
# left join
# (
#     ) no_sequential
# on output_wz_old.output_15_17.wzID == no_sequential.wzID
# where no_sequential.wzID is null
