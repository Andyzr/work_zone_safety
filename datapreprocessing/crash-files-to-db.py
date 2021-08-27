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


# # Create crash table

# In[20]:


def create_crash_table(year='15'):
    crash_add_gra_final = pd.read_pickle('/home/andy/Documents/sync/PITA_new/Data/crash_' + year + '_keypoint.pkl')
    crash_add_gra_final['keplist_0x'] = [i[0] if type(i) == list else -1 for i in
                                         crash_add_gra_final.PennShkeyplist_grav.values]
    crash_add_gra_final['keplist_0y'] = [i[1] if type(i) == list else -1 for i in
                                         crash_add_gra_final.PennShkeyplist_grav.values]
    crash_14 = pd.read_csv("../crashes/crash20" + year + "/CRASH.txt", low_memory=False)
    crash_14_clean = crash_14[pd.notna(crash_14.CRASH_DATE) & pd.notna(crash_14.TIME_OF_DAY)].copy()
    crash_14_clean['Time_qry'] = [str(int(i[0])) + str(int(i[1])).zfill(4) for i in
                                  crash_14_clean[['CRASH_DATE', 'TIME_OF_DAY']].values]
    crash_time_unique = crash_14_clean.drop_duplicates(['CRN', 'Time_qry'])
    crash_severity = pd.read_csv("../crashes/crash20" + year + "/FLAG.txt", low_memory=False)
    crash_severity_unique = crash_severity[['CRN', 'FATAL_OR_MAJ_INJ']].drop_duplicates(['CRN', 'FATAL_OR_MAJ_INJ'])
    crash_table = crash_add_gra_final.merge(right=crash_time_unique[['CRN', 'Time_qry']], left_on='CRN', right_on='CRN',
                                            how='left').merge(
        right=crash_severity_unique, left_on='CRN', right_on='CRN', how='left')

    crash_table.to_pickle(
        '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/crash_table_' + year + '.pkl')


# In[25]:


create_crash_table(year='15')
create_crash_table(year='16')
create_crash_table(year='17')

# In[22]:


create_crash_table(year='14')

# In[23]:


crash_table = pd.concat(
    [pd.read_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/crash_table_' + year + '.pkl') for
     year in ['14', '15', '16', '17']], axis=0)

# # Export to db

# In[25]:

from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine

crash_engine = create_engine(
    'sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/crash_db.db',
    echo=False)



# In[48]:


crash_db = crash_table[
    ['CRN', 'LANE_COUNT', 'RDWY_ORIENT', 'ROUTE', 'SPEED_LIMIT', 'PennShIDs_grav', 'Time_qry', 'keplist_0x',
     'keplist_0y', 'FATAL_OR_MAJ_INJ']]
crash_db = crash_db[~crash_db['Time_qry'].astype('str').str.contains('99')]
crash_db['Time_stamp'] = pd.to_datetime(crash_db['Time_qry'], format='%Y%m%d%H%M').astype('int') / 1e9

# In[ ]:


# In[52]:


crash_db.to_sql(name='crash_table1107', con=crash_engine,
                dtype={'CRN': Integer(), 'LANE_COUNT': Integer(), 'RDWY_ORIENT': String(), 'ROUTE': Integer(),
                       'SPEED_LIMIT': Float(), 'PennShIDs_grav': Integer(), 'Time_qry': Integer(),
                       'keplist_0x': Float(), 'keplist_0y': Float(),
                       'FATAL_OR_MAJ_INJ': Integer(), 'Time_stamp': Integer()})

# In[57]:


connection = crash_engine.connect()
connection.execute("CREATE INDEX crashindex1107 on crash_table1107 (PennShIDs_grav);")
connection.execute("CREATE INDEX crashindex1107_xy_time on crash_table1107 (keplist_0x,keplist_0y,Time_stamp);")

# In[225]:


connection = crash_engine.connect()
connection.execute("CREATE INDEX crashindex on crash_table (PennShIDs_grav);")
# print(np.nanmean(result.fetchall(),axis=0))
# for row in result:
#     print("username:", row)
# connection.commit()


# In[226]:


connection = crash_engine.connect()
connection.execute("CREATE INDEX crashindex2 on crash_table (PennShIDs_grav,Time_stamp);")
# print(np.nanmean(result.fetchall(),axis=0))
# for row in result:
#     print("username:", row)
connection.close()
