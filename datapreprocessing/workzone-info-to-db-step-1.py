#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import shapefile
# import finoa
# import shapely
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
# from pyproj import Proj, transform
# import stateplane
# from datetime import datetime
import pickle
# import multiprocessing as mp
import gc

# In[2]:


import shapefile
import geopandas as gpd

# # 1. Divide workzone projects to intervals for 0.5 hour

# In[7]:


wzs = pd.read_csv(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/workzone_lane_AADT_duration20190917_v2.csv')


# In[8]:


def divide_wzs(cleanid_M_1, interval=1800, wzs=wzs):
    if wzs.loc[cleanid_M_1]['duration'] > 0:
        times = pd.to_datetime(
            [wzs.loc[cleanid_M_1]['DATE_TIME_CLOSED_QRY'], wzs.loc[cleanid_M_1]['ACT_DATE_TIME_OPENED_QRY']],
            format='%Y%m%d%H%M')
        series = pd.DataFrame({'wzID': [cleanid_M_1, cleanid_M_1]}, index=times)
        divided = series.resample(str(interval) + 'S').pad().fillna(cleanid_M_1)
        return divided
    else:
        return pd.DataFrame({'wzID': cleanid_M_1},
                            index=[pd.to_datetime(wzs.loc[cleanid_M_1]['DATE_TIME_CLOSED_QRY'], format='%Y%m%d%H%M')])


# In[9]:


wzs_divided = pd.concat([divide_wzs(i) for i in range(len(wzs)) if wzs.loc[i]['duration'] < 7 * 24 * 3600])

# In[12]:


wzs_divided['wzTime_divided'] = wzs_divided.index.values
wzs_divided = wzs_divided.reset_index(drop=True)


# In[13]:


def creat_contorls(wzs_divided, times=[1, 2, 3]):
    return pd.concat([pd.DataFrame({'wzID': wzs_divided.wzID.values,
                                    'wzTime_divided': wzs_divided.wzTime_divided.values - pd.Timedelta(
                                        str(i * 7) + ' days'), 'Control': -i}) for i in times]).reset_index(drop=True)


# In[14]:


wzs_divided['Control'] = 0

# In[15]:


wzs_divided = pd.concat(
    [wzs_divided, creat_contorls(wzs_divided, times=[6, 5, 4, 3, 2, 1, -1, -2, -3, -4, -5, -6])]).reset_index(drop=True)

# In[19]:


print(str(len(wzs) - len(np.unique(
    wzs_divided.wzID.values))) + ' work zones are longer than one week, so we dropped them from the total ' + str(
    len(wzs)) + ' work zones')

# In[22]:


wzs_divided.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wzs_divided.pkl')

# # Add work zone information

# ## Add workzone characteristics

# In[2]:


import time

# In[3]:


from sqlalchemy import Column, Integer, String, ForeignKey, Float

# In[4]:


from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# In[9]:


wzs = pd.read_csv(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/workzone_lane_AADT_duration20190917_v2.csv')

# In[10]:


wzs['wzID'] = wzs['cleanID'] - 1

# In[16]:


engine = create_engine(
    'sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db',
    echo=False)

# In[18]:


connection = engine.connect()
wzs[['wzID', 'EVENTID', 'DATE_TIME_CLOSED_QRY', 'ACT_DATE_TIME_OPENED_QRY', 'ST_RT_NO', 'SR', 'DIRECTION',
     'DATETIME_REPORTED', 'LOCATION_LAT_BGN', 'LOCATION_LONG_BGN',
     'LOCATION_LAT_END', 'LOCATION_LONG_END', 'GCD', 'closure', 'x_bgn', 'y_bgn', 'x_end', 'y_end', 'LaneCounts',
     'AADT', 'NHS_IND',
     'PA_BYWAY_I', 'duration']].to_sql(name='wzsinfo', con=engine, dtype={'wzID': Integer(), 'EVENTID': Integer(),
                                                                          'DATE_TIME_CLOSED_QRY': Integer(),
                                                                          'ACT_DATE_TIME_OPENED_QRY': Integer(),
                                                                          'ST_RT_NO': Integer(), 'SR': String(),
                                                                          'DIRECTION': String(),
                                                                          'DATETIME_REPORTED': String(),
                                                                          'LOCATION_LAT_BGN': Float(),
                                                                          'LOCATION_LONG_BGN': Float(),
                                                                          'LOCATION_LAT_END': Float(),
                                                                          'LOCATION_LONG_END': Float(), 'GCD': Float(),
                                                                          'closure': Float(),
                                                                          'x_bgn': Float(), 'y_bgn': Float(),
                                                                          'x_end': Float(), 'y_end': Float(),
                                                                          'LaneCounts': Integer(), 'AADT': Float(),
                                                                          'NHS_IND': String(),
                                                                          'PA_BYWAY_I': String(), 'duration': Float()},
                                       chunksize=1000000, if_exists='replace')
connection.execute("CREATE INDEX IDwzinfo on wzsinfo (wzID);")
connection.close()

# In[2]:


import sqlite3

# In[3]:


sqlite3_conn = sqlite3.connect('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db')

# In[4]:


c = sqlite3_conn.cursor()
c.execute('ATTACH DATABASE "../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/speed_db.db" AS speed_db')
# c.execute('SELECT * FROM speed_db.Output_speed50 LIMIT 100')
# sqlite3_conn.commit()
# temp = c.fetchall()


# In[5]:


sqlite3_conn.commit()

# In[32]:


speed_db_conn = sqlite3.connect('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/speed_db.db')
speed_c = speed_db_conn.cursor()
speed_c.execute('CREATE INDEX IDwzoutputIDONLY on wzsoutput (wzID);')
speed_db_conn.commit()

# In[43]:


c.execute('DROP TABLE IF EXISTS wzoutput;')
sqlite3_conn.commit()
# c.execute('CREATE TABLE wzoutput AS SELECT * FROM  speed_db.wzsoutput LEFT JOIN wzsinfo ON speed_db.wzsoutput.wzID = wzsinfo.wzID; ')
c.execute('CREATE TABLE wzsoutput AS SELECT * FROM  wzsinfo;')
sqlite3_conn.commit()

# In[73]:


temp_reso = [0, 3, 6, 9, 12, 15]
week_reso = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
query_string = ' '
for i in range(len(temp_reso) - 1):
    query_string = query_string + "CASE WHEN "
    for j in week_reso:
        query_string = query_string + "(temp.datedelta BETWEEN " + str(temp_reso[i] + 7 * 24 * j) + " AND " + str(
            temp_reso[i + 1] + 7 * 24 * j) + ") OR "
    query_string = query_string[:-3]
    query_string = query_string + " THEN 1 ELSE 0 END sequence_" + str(i) + ',\n'
query_string = query_string[:-2]
# print(query_string)


# In[201]:


sqlite3_conn.close()

# In[74]:


# c.execute('CREATE TABLE wzoutput AS SELECT * FROM  speed_db.wzsoutput LEFT JOIN wzsinfo ON speed_db.wzsoutput.wzID = wzsinfo.wzID; ')
c.execute("""DROP TABLE IF EXISTS wzsoutput_add""")
sqlite3_conn.commit()
c.execute("""CREATE TABLE wzsoutput_add AS """ + """ select temp.*,
""" + query_string +
          """ FROM (SELECT wzID, location,wzTime_divided_stamp,cast(strftime('%w',cast(wzTime_divided_stamp as text),'unixepoch') as integer) BETWEEN 1 AND 5  as WeekdayofWeek,
          cast(strftime('%m',cast(wzTime_divided_stamp as text),'unixepoch') as integer) BETWEEN 1 AND 5  as Month,
          cast(strftime('%H',cast(wzTime_divided_stamp as text),'unixepoch') as integer) BETWEEN 6 AND 17 as DaytimeofDay,
          (strftime('%s',cast(wzTime_divided_stamp as text),'unixepoch')-
          strftime('%s',substr(cast(DATE_TIME_CLOSED_QRY as text),1,4)||'-'||substr(cast(DATE_TIME_CLOSED_QRY as text),5,2)||'-'||substr(cast(DATE_TIME_CLOSED_QRY as text),7,2)||' '||substr(cast(DATE_TIME_CLOSED_QRY as text),9,2)||':'||substr(cast(DATE_TIME_CLOSED_QRY as text),11,2)))/3600.0 as datedelta
          FROM wzsoutput ) temp ; """)
sqlite3_conn.commit()

# In[27]:


c.close()

# In[28]:


sqlite3_conn.close()

# ## Assign treatment

# Basic strategy: get PennShID--Time--treatment table; and workzone-pennShID--Alltime-AllControl table (wzoutput). then join and justify.

# In[2]:


wz_type_xy = pd.read_pickle(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_300m.pkl')

# In[4]:


wz_PennShID = wz_type_xy[['wzID', 'PennShID']].drop_duplicates()
wz_PennShID = wz_PennShID[wz_PennShID.PennShID != -1]

# In[5]:


wz_PennShID_m = wz_PennShID.sort_values(by='PennShID').merge(wz_PennShID.sort_values(by='PennShID'), left_on='PennShID',
                                                             right_on='PennShID', how='inner')

# In[6]:


wz_PennShID_m = wz_PennShID_m[['wzID_x', 'wzID_y']].drop_duplicates()

# In[9]:


wzs_divided = pd.read_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wzs_divided.pkl')

# In[10]:


wzs_divided['wzID'] = wzs_divided['wzID'].astype('int')

# In[11]:


wzs_divided['wzTime_divided_stamp'] = [i.astype('float') / 1e9 for i in wzs_divided['wzTime_divided'].values]

# In[2]:


import sqlite3

# In[6]:


sqlite3_conn = sqlite3.connect('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db')

# In[7]:


c = sqlite3_conn.cursor()

# In[16]:


wzs = pd.read_sql('SELECT wzID, DATE_TIME_CLOSED_QRY,ACT_DATE_TIME_OPENED_QRY FROM wzsinfo;', sqlite3_conn)

# In[17]:


wzs['DATE_TIME_CLOSED_QRY'] = pd.to_datetime(wzs['DATE_TIME_CLOSED_QRY'], format='%Y%m%d%H%M').astype(int) / 10 ** 9
wzs['ACT_DATE_TIME_OPENED_QRY'] = pd.to_datetime(wzs['ACT_DATE_TIME_OPENED_QRY'], format='%Y%m%d%H%M').astype(
    int) / 10 ** 9

# In[19]:


wz_PennShID_time = wz_PennShID_m.sort_values(by='wzID_y').merge(right=wzs, left_on='wzID_y',
                                                                right_on='wzID').sort_values(by='wzID_x')

# In[3]:


from sqlalchemy import Column, Integer, String, ForeignKey, Float

# In[8]:


from sqlalchemy import create_engine

# In[36]:


engine = create_engine(
    'sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db',
    echo=False)

# In[39]:


wzs_divided[wzs_divided.Control != 0][['wzID', 'wzTime_divided_stamp']].reset_index(drop=True).to_sql(
    name='temp_wztime', con=engine, dtype={'wzID': Integer(), 'wzTime_divided_stamp': Integer()}, if_exists='replace')
c.execute('CREATE INDEX IDtemp_wztime on temp_wztime (wzID);')
sqlite3_conn.commit()

# In[40]:


wz_PennShID_time[['wzID_x', 'DATE_TIME_CLOSED_QRY', 'ACT_DATE_TIME_OPENED_QRY']].reset_index(drop=True).to_sql(
    name='temp_wzPIDtime', con=engine,
    dtype={'wzID_x': Integer(), 'DATE_TIME_CLOSED_QRY': Integer(), 'ACT_DATE_TIME_OPENED_QRY': Integer()},
    if_exists='replace')
c.execute('CREATE INDEX IDtemp_wzPIDtime on temp_wzPIDtime (wzID_x);')
sqlite3_conn.commit()

# In[9]:


c.execute(
    "CREATE TABLE temp_treatment AS SELECT temp_wztime.wzID,temp_wztime.wzTime_divided_stamp,(temp_wztime.wzTime_divided_stamp BETWEEN temp_wzPIDtime.DATE_TIME_CLOSED_QRY AND temp_wzPIDtime.ACT_DATE_TIME_OPENED_QRY) AS treatment FROM temp_wztime INNER JOIN temp_wzPIDtime ON temp_wztime.wzID = temp_wzPIDtime.wzID_x;")
sqlite3_conn.commit()

# In[62]:


c.execute(
    "CREATE TABLE new_treatment AS select temp_treatment.wzID,temp_treatment.wzTime_divided_stamp,sum(temp_treatment.treatment)>0 as new_treatment from temp_treatment group by temp_treatment.wzID,temp_treatment.wzTime_divided_stamp;")
sqlite3_conn.commit()

# # create final output table

# In[4]:


import sqlite3

# In[5]:


sqlite3_conn = sqlite3.connect('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db')

# In[6]:


c = sqlite3_conn.cursor()

# In[72]:


# create index for wzsoutput
c.execute("CREATE INDEX wzsoutput_id_loc_time on  wzsoutput(wzID,location,wzTime_divided_stamp);")
sqlite3_conn.commit()
c.execute("CREATE INDEX wzsoutput_id on  wzsoutput(wzID);")
sqlite3_conn.commit()
c.execute("CREATE INDEX wzsoutput_id_time on  wzsoutput(wzID,wzTime_divided_stamp);")
sqlite3_conn.commit()

# In[77]:


c.execute("CREATE INDEX wzsoutput_add_id_loc_time on  wzsoutput_add(wzID, location,wzTime_divided_stamp);")
sqlite3_conn.commit()

# In[14]:


c.execute("pragma temp_store_directory = '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/'")
sqlite3_conn.commit()

# In[ ]:


c.execute("CREATE INDEX temp_treatment_id_time on  temp_treatment(wzID,wzTime_divided_stamp);")
sqlite3_conn.commit()

# In[68]:


c.execute("CREATE INDEX new_treatment_id_time on  new_treatment(wzID,wzTime_divided_stamp);")
sqlite3_conn.commit()

# In[52]:


c.execute("pragma temp_store_directory = '/tmp'")
sqlite3_conn.commit()

# In[15]:


c.execute(""" DROP TABLE IF EXISTS wzs_output_all;""")
sqlite3_conn.commit()
c.execute("""CREATE TABLE wzs_output_all AS select wzsoutput.wzID, wzsoutput.Control, wzsoutput.wzTime_divided_stamp, wzsoutput.location,
       wzsoutput.closure, wzsoutput.LaneCounts, wzsoutput.AADT, wzsoutput.NHS_IND,wzsoutput.PA_BYWAY_I, wzsoutput.duration,
       wzsoutput_add.WeekdayofWeek,wzsoutput_add.Month,wzsoutput_add.DaytimeofDay,wzsoutput_add.datedelta,wzsoutput_add.sequence_0,
            wzsoutput_add.sequence_1,wzsoutput_add.sequence_2,wzsoutput_add.sequence_3,wzsoutput_add.sequence_4,
            new_treatment.new_treatment as treatment
       from wzsoutput 
    LEFT JOIN wzsoutput_add
        ON wzsoutput.wzID = wzsoutput_add.wzID 
        AND wzsoutput.location = wzsoutput_add.location
        AND wzsoutput.wzTime_divided_stamp = wzsoutput_add.wzTime_divided_stamp 
    LEFT JOIN new_treatment
        ON wzsoutput.wzID = new_treatment.wzID 
        AND wzsoutput.wzTime_divided_stamp = new_treatment.wzTime_divided_stamp; """)
sqlite3_conn.commit()

# In[21]:


sqlite3_conn.close()

# In[22]:


sqlite3_conn = sqlite3.connect('/home/andy/Documents/dbs/WZ_output.db')

# In[23]:


c = sqlite3_conn.cursor()
c.execute('ATTACH DATABASE "../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db" AS olddb')
sqlite3_conn.commit()

# In[24]:


c.execute('CREATE TABLE wzs_output_all AS select * from olddb.wzs_output_all;')
sqlite3_conn.commit()

# In[25]:


sqlite3_conn.close()

# In[72]:


sqlite3_conn = sqlite3.connect('/home/andy/Documents/dbs/WZ_output.db')
c = sqlite3_conn.cursor()
c.execute(
    'CREATE TABLE wzs_output_all AS SELECT wzs_output_all.*,ifnull(wzs_output_all.treatment,1) FROM wzs_output_all')
sqlite3_conn.commit()

# # Correcting AADT numbers

# In[2]:


wz_type_xy = pd.read_pickle(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_300m.pkl')

# In[3]:


wz_PennShID = wz_type_xy[['wzID', 'PennShID', 'location']].drop_duplicates()
wz_PennShID = wz_PennShID[wz_PennShID.PennShID != -1]

# ## create PennShID ~ AADT 2013_2017 table

# In[2]:


import geopandas as gpd

# In[5]:


import os

# In[3]:


filenames = {'2013': '/home/andy/Documents/sync/PITA_new/Data/PasdaRoads/PaStateRoads_2013_02/PaStateRoads2013_02.shp',
             '2014': '/home/andy/Documents/sync/PITA_new/Data/PasdaRoads/PaStateRoads_2014_02/PaStateRoads2014_02.shp',
             '2015': '/home/andy/Documents/sync/PITA_new/Data/PasdaRoads/PaStateRoads_2015_01/PaStateRoads2015_01.shp',
             '2016': '/home/andy/Documents/sync/PITA_new/Data/PasdaRoads/PaStateRoads_2016_01/PaStateRoads2016_01.shp',
             '2017': '/home/andy/Documents/sync/PITA_new/Data/PasdaRoads/PaStateRoads_2017_01/PaStateRoads2017_01.shp'}

# In[4]:


PA_roads = {'road_' + str(i): gpd.read_file(filenames[str(i)]) for i in range(2013, 2018)}

# In[15]:


PA_roads['road_base'] = gpd.read_file(
    '../../PennShareRoad/RMSSEG_State_Roads/PennShare_PA_south_ids_good/PennShare_PA_south_ids_good.shp')

# In[17]:


PA_roads['speed_base'] = gpd.read_file(
    '../Maps/RMSADMIN_Administrative_Classifications_of_Roadway/RMSADMIN_Administrative_Classifications_of_Roadway.shp')

# In[18]:


PA_AADT = PA_roads['road_base']

# In[ ]:


PA_AADTs = PA_AADT[['PennShIDs', 'ST_RT_NO', 'CTY_CODE', 'SEG_NO', 'CUR_AADT']].rename(
    columns={'CUR_AADT': 'CUR_AADT_17'}).merge(
    right=PA_roads['road_2013'][['ST_RT_NO', 'CTY_CODE', 'SEG_NO', 'CUR_AADT']].rename(
        columns={'CUR_AADT': 'CUR_AADT_13'}), left_on=['ST_RT_NO', 'CTY_CODE', 'SEG_NO'],
    right_on=['ST_RT_NO', 'CTY_CODE', 'SEG_NO'], how='left')

# In[ ]:


PA_AADTs = PA_AADT[['PennShIDs', 'ST_RT_NO', 'CTY_CODE', 'SEG_NO', 'CUR_AADT']].rename(
    columns={'CUR_AADT': 'CUR_AADT_17'}).merge(
    right=PA_roads['road_2013'][['ST_RT_NO', 'CTY_CODE', 'SEG_NO', 'CUR_AADT']].rename(
        columns={'CUR_AADT': 'CUR_AADT_13'}), left_on=['ST_RT_NO', 'CTY_CODE', 'SEG_NO'],
    right_on=['ST_RT_NO', 'CTY_CODE', 'SEG_NO'], how='left')
for i in range(2014, 2017):
    PA_AADTs = PA_AADTs.merge(right=PA_roads['road_' + str(i)][['ST_RT_NO', 'CTY_CODE', 'SEG_NO', 'CUR_AADT']].rename(
        columns={'CUR_AADT': 'CUR_AADT_' + str(i)[-2:]}), left_on=['ST_RT_NO', 'CTY_CODE', 'SEG_NO'],
        right_on=['ST_RT_NO', 'CTY_CODE', 'SEG_NO'], how='left')

# In[ ]:


PA_AADTs['length'] = PA_roads['road_2017'].length

# In[ ]:


wz_PennShID = wz_PennShID[wz_PennShID.location == 'in'].reset_index(drop=True)

# In[ ]:


wz_PennShID_AADTs = wz_PennShID.merge(
    right=PA_AADTs[['PennShIDs', 'CUR_AADT_13', 'CUR_AADT_14', 'CUR_AADT_15', 'CUR_AADT_16', 'CUR_AADT_17', 'length']],
    left_on='PennShID', right_on='PennShIDs', how='left')

# In[ ]:


wz_PennShID_AADTs15_17 = wz_PennShID_AADTs.groupby('wzID').apply(lambda x: pd.Series(
    {'AADT_' + str(i): np.average(x['CUR_AADT_' + str(i)], weights=x['length']) for i in range(13, 18)})).reset_index()

# In[ ]:


wz_type_xy_14 = pd.read_pickle(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2014/important/wz_type_xy_20191014_300m.pkl')

# In[ ]:


wz_PennShID_14 = wz_type_xy_14[['wzID', 'PennShID', 'location']].drop_duplicates()
wz_PennShID_14 = wz_PennShID_14[wz_PennShID_14.PennShID != -1]
wz_PennShID_14 = wz_PennShID_14[wz_PennShID_14.location == 'in'].reset_index(drop=True)

# In[ ]:


wz_PennShID_14.PennShID = wz_PennShID_14.PennShID.astype('int')

# In[ ]:


wz_PennShID_AADTs_14 = wz_PennShID_14.merge(
    right=PA_AADTs[['PennShIDs', 'CUR_AADT_13', 'CUR_AADT_14', 'CUR_AADT_15', 'CUR_AADT_16', 'CUR_AADT_17', 'length']],
    left_on='PennShID', right_on='PennShIDs', how='left')

wz_PennShID_AADTs_14 = wz_PennShID_AADTs_14.groupby('wzID').apply(lambda x: pd.Series(
    {'AADT_' + str(i): np.average(x['CUR_AADT_' + str(i)], weights=x['length']) for i in range(13, 18)})).reset_index()

# In[ ]:


with open('../wzinnerIDs.pkl', 'rb') as f:
    wz_13_in = pickle.load(f)

wz_13_in = [r[5] for r in wz_13_in]

# In[ ]:


wz_PennShID_13 = pd.DataFrame([(i, m) for i, j in enumerate(wz_13_in) for m in j], columns=['wzID', 'PennShID'])

# In[ ]:


wz_PennShID_AADTs_13 = wz_PennShID_13.merge(
    right=PA_AADTs[['PennShIDs', 'CUR_AADT_13', 'CUR_AADT_14', 'CUR_AADT_15', 'CUR_AADT_16', 'CUR_AADT_17', 'length']],
    left_on='PennShID', right_on='PennShIDs', how='left')

wz_PennShID_AADTs_13 = wz_PennShID_AADTs_13.groupby('wzID').apply(lambda x: pd.Series(
    {'AADT_' + str(i): np.average(x['CUR_AADT_' + str(i)], weights=x['length']) for i in range(13, 18)})).reset_index()

# In[ ]:


wz_PennShID_AADTs_13['year'] = 13
wz_PennShID_AADTs_14['year'] = 14
wz_PennShID_AADTs15_17['year'] = 15

# In[ ]:


wz_AADTS = pd.concat([wz_PennShID_AADTs_13, wz_PennShID_AADTs_14, wz_PennShID_AADTs15_17])

# In[38]:


wzs_inters = pd.read_csv(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/workzone_lane_AADT_duration20191106v2.csv')

# In[40]:


wzs_inters['wzID'] = wzs_inters['cleanID'] - 1

# # Final out_put again

# In[4]:


import sqlite3

# In[8]:


from sqlalchemy import Column, Integer, String, ForeignKey, Float

# In[41]:


wzs_inters['NUM_ramps'] = wzs_inters['NUM_ramps'].astype('int')

# In[43]:


from sqlalchemy import create_engine, ForeignKey

# In[44]:


engine = create_engine(
    'sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db',
    echo=False)

# In[47]:


wzs_inters[['wzID', 'NUM_inters', 'NUM_ramps', 'NetLength']][wzs_inters.NetLength > 0].to_sql(name='wzInters',
                                                                                              con=engine,
                                                                                              dtype={"wzID": Integer(),
                                                                                                     'NUM_inters': Integer(),
                                                                                                     'NUM_ramps': Integer(),
                                                                                                     'NetLength': Float()},
                                                                                              index=False,
                                                                                              if_exists='replace')

# In[327]:


wz_AADTS[['year', 'wzID', 'AADT_13', 'AADT_14', 'AADT_15', 'AADT_16', 'AADT_17']].to_sql(name='wzAADT', con=engine,
                                                                                         dtype={"wzID": Integer(),
                                                                                                'AADT_13': Float(),
                                                                                                'year': Integer()},
                                                                                         index=False,
                                                                                         if_exists='replace')

# In[77]:


sqlite3_conn = sqlite3.connect('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/output/output_wz.db')

# In[78]:


c = sqlite3_conn.cursor()
c.execute('ATTACH DATABASE "/home/andy/Documents/dbs/WZ_output.db" AS wzoutput_db')

# In[79]:


c.execute('DROP TABLE IF EXISTS wzoutput_15_17')
c.execute("""CREATE TABLE wzoutput_15_17 AS SELECT 
temp.wzID,temp.Control,temp.wzTime_divided_stamp,temp.location,temp.closure,temp.LaneCounts,temp.AADT,temp.NHS_IND,temp.PA_BYWAY_I,temp.duration,temp.WeekdayofWeek,temp.Month,temp.DaytimeofDay,temp.sequence_0,temp.sequence_1,temp.sequence_2,temp.sequence_3,temp.sequence_4,temp.real_speed_50,temp.historical_speed_50,temp.free_speed_50,
temp.crash_50,temp.crash_severe_50,temp.real_speed_100,temp.historical_speed_100,temp.free_speed_100,temp.crash_100,temp.crash_severe_100,temp.real_speed_150,temp.historical_speed_150,
temp.free_speed_150,temp.crash_150,temp.crash_severe_150,temp.real_speed_200,temp.historical_speed_200,temp.free_speed_200,temp.crash_200,temp.crash_severe_200,temp.real_speed_250,
temp.historical_speed_250,temp.free_speed_250,temp.crash_250,temp.crash_severe_250,temp.real_speed_300,temp.historical_speed_300,temp.free_speed_300,temp.crash_300,temp.crash_severe_300,
temp.treatment_new, wzInters.NUM_inters,wzInters.NUM_ramps,wzInters.NetLength, cast(strftime('%Y',cast(wzTime_divided_stamp as text),'unixepoch') as integer) AS Year FROM (select * from wzoutput_db.wzs_output_all) temp INNER JOIN wzInters ON temp.wzID =wzInters.wzID ;""").fetchall()

# In[80]:


sqlite3_conn.commit()
