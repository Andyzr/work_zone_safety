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

speed_engine = create_engine(
    'sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/speed_db.db',
    echo=False)

# speed_engine_old = create_engine('sqlite:////media/andy/zhangzr/speed_db.db', echo=False)

Pid_Mid_engine = create_engine(
    'sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/PennMultiId.db',
    echo=False)

# output location
output_speed_conn = sqlite3.connect(
    '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_speed_1117.db')
output_speed_c = output_speed_conn.cursor()

# source of speed
output_speed_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/INRIX_2012_17/speed_2012_17.db" AS speed_db')
output_speed_conn.commit()

output_speed_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/PennMultiId.db" AS PMinfo')
output_speed_conn.commit()

output_speed_c.execute('CREATE INDEX if not exists PMinfo.PMinfo_Pid on PennXY_MultiID(PennShIDs) ')
output_speed_conn.commit()

output_speed_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_loc.db" AS wz_loc_db')
output_speed_conn.commit()

output_speed_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_crash_1117.db" AS wzs_output')
output_speed_conn.commit()

output_speed_c.execute('create table if not exists wzsoutput as select * from wzs_output.wzsoutput;')
output_speed_conn.commit()

output_speed_c.execute(
    'create index if not exists id_wzsoutput_id_time_loc on wzsoutput(wzID,wzTime_divided_stamp,location);')
output_speed_conn.commit()

# %%
# %%time
output_speed_c.execute("create index wz_loc_db.wz_loc_61_id_loc_pid on wz_loc_61(wzID,location,PennShID)")
output_speed_conn.commit()

# %%
# %%time
# speed db creation
output_speed_c.execute("""
--sql
create table if not exists speed_xy_61 AS
SELECT temp_61.wzID,
temp_61.wzTime_divided_stamp,
temp_61.location,
AVG(speed_db.speed.speed) AS real_speed_61,
AVG(speed_db.speed.average_speed) AS historical_speed_61,
AVG(speed_db.speed.reference_speed) AS free_speed_61
 FROM 
 (select wzsoutput.wzID,wzsoutput.wzTime_divided_stamp,wzsoutput.location,
    temp.MultiID,
    datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-12600,'unixepoch') as wztimeint,
    datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-1800,'unixepoch') as wztimeintend 

FROM wzsoutput 
inner JOIN 

(SELECT wz_loc_db.wz_loc_61.wzID,wz_loc_db.wz_loc_61.location,
PMinfo.PennXY_MultiID.MultiID
 from wz_loc_db.wz_loc_61 
inner join PMinfo.PennXY_MultiID
on wz_loc_db.wz_loc_61.PennShID =PMinfo.PennXY_MultiID.PennShIDs ) temp

ON wzsoutput.wzID == temp.wzID AND
wzsoutput.location == temp.location) temp_61

    inner JOIN speed_db.speed 
    ON 
    temp_61.MultiID = speed_db.speed.tmc_code 
    AND 
    speed_db.speed.measurement_tstamp BETWEEN temp_61.wztimeint AND temp_61.wztimeintend 
    
    GROUP BY temp_61.wzID,
    	temp_61.wzTime_divided_stamp,
        temp_61.location ; """)

output_speed_conn.commit()

# %%
# %%time
output_speed_c.execute("create index wz_loc_db.wz_loc_518_id_loc_pid on wz_loc_518(wzID,location,PennShID)")
output_speed_conn.commit()

# %%
# %%time
# speed db creation
output_speed_c.execute("""
--sql
create table if not exists speed_xy_518 AS
SELECT temp_518.wzID,
temp_518.wzTime_divided_stamp,
temp_518.location,
AVG(speed_db.speed.speed) AS real_speed_518,
AVG(speed_db.speed.average_speed) AS historical_speed_518,
AVG(speed_db.speed.reference_speed) AS free_speed_518
 FROM 
 (select wzsoutput.wzID,wzsoutput.wzTime_divided_stamp,wzsoutput.location,
    temp.MultiID,
    datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-12600,'unixepoch') as wztimeint,
    datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-1800,'unixepoch') as wztimeintend 

FROM wzsoutput 
inner JOIN 

(SELECT wz_loc_db.wz_loc_518.wzID,wz_loc_db.wz_loc_518.location,
PMinfo.PennXY_MultiID.MultiID
 from wz_loc_db.wz_loc_518 
inner join PMinfo.PennXY_MultiID
on wz_loc_db.wz_loc_518.PennShID =PMinfo.PennXY_MultiID.PennShIDs ) temp

ON wzsoutput.wzID == temp.wzID AND
wzsoutput.location == temp.location) temp_518

    inner JOIN speed_db.speed 
    ON 
    temp_518.MultiID = speed_db.speed.tmc_code 
    AND 
    speed_db.speed.measurement_tstamp BETWEEN temp_518.wztimeint AND temp_518.wztimeintend 
    
    GROUP BY temp_518.wzID,
    	temp_518.wzTime_divided_stamp,
        temp_518.location ; """)

output_speed_conn.commit()

# %%
# %%time
# pd.read_sql("""
# --sql
# EXPLAIN QUERY PLAN
# create table if not exists speed_xy_518 AS
# SELECT temp_61.wzID,
# temp_61.wzTime_divided_stamp,
# temp_61.location,
# AVG(speed_db.speed.speed) AS real_speed_61,
# AVG(speed_db.speed.average_speed) AS historical_speed_61,
# AVG(speed_db.speed.reference_speed) AS free_speed_61
#  FROM 
#  (select wzsoutput.wzID,wzsoutput.wzTime_divided_stamp,wzsoutput.location,
#     temp.MultiID,
#     datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-12600,'unixepoch') as wztimeint,
#     datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-1800,'unixepoch') as wztimeintend 

# FROM wzsoutput 
# inner JOIN 

# (SELECT wz_loc_db.wz_loc_61.wzID,wz_loc_db.wz_loc_61.location,
# PMinfo.PennXY_MultiID.MultiID
#  from wz_loc_db.wz_loc_61 
# inner join PMinfo.PennXY_MultiID
# on wz_loc_db.wz_loc_61.PennShID =PMinfo.PennXY_MultiID.PennShIDs ) temp

# ON wzsoutput.wzID == temp.wzID AND
# wzsoutput.location == temp.location) temp_61

#     inner JOIN speed_db.speed 
#     ON 
#     temp_61.MultiID = speed_db.speed.tmc_code 
#     AND 
#     speed_db.speed.measurement_tstamp BETWEEN temp_61.wztimeint AND temp_61.wztimeintend 

#     GROUP BY temp_61.wzID,
#     	temp_61.wzTime_divided_stamp,
#         temp_61.location; """,output_speed_conn).values

# %%
