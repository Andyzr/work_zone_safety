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
# speed_engine = create_engine('sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/speed_db.db', echo=False)

# speed_engine_old = create_engine('sqlite:////media/andy/zhangzr/speed_db.db', echo=False)

# crash_engine = create_engine('sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_crash.db', echo=False)

# output location
output_crash_conn = sqlite3.connect(
    '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_crash_1117.db')
output_crash_c = output_crash_conn.cursor()

# source of wzs_output (wzID-loc-time): speed_db.wzsoutput
output_crash_c.execute('ATTACH DATABASE "/media/andy/zhangzr/speed_db.db" AS speed_db')
output_crash_conn.commit()

output_crash_c.execute('create table wzsoutput as select * from speed_db.wzsoutput;')
output_crash_conn.commit()

output_crash_c.execute('create index id_wzsoutput_id_time_loc on wzsoutput(wzID,wzTime_divided_stamp,location);')
output_crash_conn.commit()

# output_crash_c.execute('ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wzs_output_db.db" AS wzs_output_db')
# output_crash_conn.commit()

# source of crash database crash_db.crash_table1107
output_crash_c.execute(
    'ATTACH DATABASE "../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/crash_db.db" AS crash_db')

# source of wzloc wz_loc_db.wz_loc_518 or wz_loc_db.wz_loc_61
output_crash_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_loc.db" AS wz_loc_db')
output_crash_conn.commit()

# create crash table

# %%
# %%time
output_crash_c.execute("""
create table if not exists crash_xy_61 AS
SELECT temp_61.wzID,
temp_61.wzTime_divided_stamp,
temp_61.location,
COUNT(crash_db.crash_table1107.FATAL_OR_MAJ_INJ)>0 AS crash_61,
SUM(crash_db.crash_table1107.FATAL_OR_MAJ_INJ)>0 AS crash_severe_61

 FROM 
 (select wzsoutput.wzID,wzsoutput.wzTime_divided_stamp,wzsoutput.location,
wz_loc_db.wz_loc_61.x as x,wz_loc_db.wz_loc_61.y as y ,

CAST(wzsoutput.wzTime_divided_stamp as INT) as wztimeint,CAST(wzsoutput.wzTime_divided_stamp as INT)+1800 as wztimeintend 

FROM wzsoutput 
LEFT JOIN wz_loc_db.wz_loc_61 
ON wzsoutput.wzID == wz_loc_db.wz_loc_61.wzID AND
wzsoutput.location == wz_loc_db.wz_loc_61.location)temp_61

    LEFT JOIN crash_db.crash_table1107 
    ON 
    temp_61.x = crash_db.crash_table1107.keplist_0x 
    AND
    temp_61.y = crash_db.crash_table1107.keplist_0y 
    AND 
    crash_db.crash_table1107.Time_stamp BETWEEN temp_61.wztimeint AND temp_61.wztimeintend 
    
    GROUP BY temp_61.wzID,
    	temp_61.wzTime_divided_stamp,
        temp_61.location """)
output_crash_conn.commit()

# %%
# %%time
output_crash_c.execute("""
create table if not exists crash_xy_518 AS
SELECT temp_518.wzID,
temp_518.wzTime_divided_stamp,
temp_518.location,
COUNT(crash_db.crash_table1107.FATAL_OR_MAJ_INJ)>0 AS crash_518,
SUM(crash_db.crash_table1107.FATAL_OR_MAJ_INJ)>0 AS crash_severe_518

 FROM 
 (select wzsoutput.wzID,wzsoutput.wzTime_divided_stamp,wzsoutput.location,
wz_loc_db.wz_loc_518.x as x,wz_loc_db.wz_loc_518.y as y ,

CAST(wzsoutput.wzTime_divided_stamp as INT) as wztimeint,CAST(wzsoutput.wzTime_divided_stamp as INT)+1800 as wztimeintend 

FROM wzsoutput 
LEFT JOIN wz_loc_db.wz_loc_518 
ON wzsoutput.wzID == wz_loc_db.wz_loc_518.wzID AND
wzsoutput.location == wz_loc_db.wz_loc_518.location)temp_518

    LEFT JOIN crash_db.crash_table1107 
    ON 
    temp_518.x = crash_db.crash_table1107.keplist_0x 
    AND
    temp_518.y = crash_db.crash_table1107.keplist_0y 
    AND 
    crash_db.crash_table1107.Time_stamp BETWEEN temp_518.wztimeint AND temp_518.wztimeintend 
    
    GROUP BY temp_518.wzID,
    	temp_518.wzTime_divided_stamp,
        temp_518.location """)
output_crash_conn.commit()
