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
ws = pd.read_csv("../../weather/weatherStation.csv")

# #%%
postgre_engine = create_engine("postgresql://postgres:fakepassword@localhost:fakeport/gisdb")

# #%%
ws.to_sql(name='weatherstation', con=postgre_engine, index=False)

# #%%
pid_wid = pd.read_sql("SELECT * from pid_wstation;", postgre_engine)

# #%%
weather_engine = create_engine('sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/weather/weather.db',
                               echo=False)

# #%%
pid_wid[['pennshids', 'ID', 'distance']].to_sql(name='pid_wid',
                                                dtype={'pennshids': Integer(), 'ID': String(), 'distance': Float()},
                                                index=False, con=weather_engine)

# #%%
pid_wid = pd.read_sql("SELECT * from pid_wstation_all;", postgre_engine)
pid_wid[['pennshids', 'ID', 'distance']].to_sql(name='pid_wid_all',
                                                dtype={'pennshids': Integer(), 'ID': String(), 'distance': Float()},
                                                index=False, con=weather_engine)

# %%
# weather output
output_weather_conn = sqlite3.connect(
    '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_weather_1117.db')
output_weather_c = output_weather_conn.cursor()

# weather data source
output_weather_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/weather/weather.db" AS weather_db')
output_weather_conn.commit()

output_weather_c.execute("Create Index weather_db.i_pid_weaid on pid_wid(pennshids,ID)")
output_weather_conn.commit()

# wzs output source:
output_weather_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_crash_1117.db" AS wzs_output')
output_weather_conn.commit()

output_weather_c.execute(
    'create table if not exists wzsoutput as SELECT distinct wzID, wzTime_divided_stamp FROM wzs_output.wzsoutput;')
output_weather_conn.commit()

output_weather_c.execute('create index if not exists id_wzsoutput_id_time on wzsoutput(wzID,wzTime_divided_stamp);')
output_weather_conn.commit()

output_weather_c.execute('create index if not exists id_wzsoutput_id on wzsoutput(wzID);')
output_weather_conn.commit()

# wzs loc database:
output_weather_c.execute(
    'ATTACH DATABASE "/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_loc.db" AS wz_loc_db')
output_weather_conn.commit()

output_weather_c.execute("""create table if not exists wzid_pid as
select wzID, min(PennShID) as PennShID
from wz_loc_db.wz_loc_61
where PennShID >-1
group by
wzID
order by wzID""")
output_weather_conn.commit()

output_weather_c.execute("""create index if not exists
id_wzid on wzid_pid(wzID) """)
output_weather_conn.commit()

# %%
# %%time
# create table
output_weather_c.execute(""" 
--sql
create table output_weather as
select wzsoutput.wzID,wzsoutput.wzTime_divided_stamp,
AVG(AveT) as AveT, AVG(Precip) as AveP, AVG(AveWindSpeed) as AveW
from
wzsoutput
left join
 wzid_pid
on wzid_pid.wzID = wzsoutput.wzID

left join
weather_db.pid_wid
on wzid_pid.PennShID = weather_db.pid_wid.pennshids

left join
weather_db.weather
on weather_db.pid_wid.ID = weather_db.weather.ID
AND 
weather_db.weather.DateTime between datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-12600,'unixepoch') AND datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-1800,'unixepoch')
group by 
 wzsoutput.wzID,wzsoutput.wzTime_divided_stamp;
""")
output_weather_conn.commit()

# %%
# %%time
# #query
# pd.read_sql(""" 
# --sql
# explain query plan
# create table output_weather as
# select wzsoutput.wzID,wzsoutput.wzTime_divided_stamp,
# AVG(AveT) as AveT, AVG(Precip) as AveP, AVG(AveWindSpeed) as AveW
# from
# wzsoutput
# left join
#  wzid_pid
# on wzid_pid.wzID = wzsoutput.wzID

# left join
# weather_db.pid_wid
# on wzid_pid.PennShID = weather_db.pid_wid.pennshids

# left join
# weather_db.weather
# on weather_db.pid_wid.ID = weather_db.weather.ID
# AND 
# weather_db.weather.DateTime between datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-12600,'unixepoch') AND datetime(CAST(wzsoutput.wzTime_divided_stamp as INT)-1800,'unixepoch')
# group by 
#  wzsoutput.wzID,wzsoutput.wzTime_divided_stamp;
# """, output_weather_conn)

# %%
# %%time
# pd.read_sql("""
# --sql
# select wzID, min(PennShID) as PennShID
# from wz_loc_db.wz_loc_61
# where PennShID >-1
# group by
# wzID
# order by wzID
# """, output_weather_conn)

# %%
