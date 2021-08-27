#!/usr/bin/env python
# coding: utf-8

# In[2]:


import shapefile
import geopandas as gpd

# In[22]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import gc
from sqlalchemy import create_engine
import sqlite3
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from _datetime import time

# #  speed limit to sqlite3 database

# I use the postgreseql script to finish the speed limit match

# ```postgresql
# \copy (
# select pennshare_pa_south_ids_good.pennshids,min(rmsadmin_administrative_classifications_of_roadway.speed_limi) as speed_limi from pennshare_pa_south_ids_good
# left join rmsadmin_administrative_classifications_of_roadway
#  on pennshare_pa_south_ids_good.st_rt_no= rmsadmin_administrative_classifications_of_roadway.st_rt_no
#  and pennshare_pa_south_ids_good.cty_code= rmsadmin_administrative_classifications_of_roadway.cty_code
#  and pennshare_pa_south_ids_good.seg_no 
#  	between rmsadmin_administrative_classifications_of_roadway.seg_bgn
# 	and rmsadmin_administrative_classifications_of_roadway.seg_end
# 	group by
# 	pennshare_pa_south_ids_good.pennshids)
# 	to '/media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/pid_speed_limit.csv'
# 	CSV HEADER;
#  ```

# now I want to import the csv file to sqlite db

# In[28]:


output_loc_engine = create_engine(
    "sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_loc.db")

# In[29]:


pid_speed_limit = pd.read_csv("../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/pid_speed_limit.csv")

# In[30]:


pid_speed_limit.rename(columns={'speed_limi': 'speed_limit'}).to_sql(name='pid_speed_limit', con=output_loc_engine,
                                                                     index=False,
                                                                     dtype={'pennshids': Integer(),
                                                                            'speed_limit': Float()})

# # Workzone speed tmc location information table

# In[227]:


Penn2_MultiNet = pd.read_csv('../../PennShareRoad/MultiNet_join_PennShare0707ver2.csv')

Penn2_MultiNet['RDSTMC_new'] = [str(x)[1:] for x in Penn2_MultiNet['RDSTMC'].values]

# In[228]:


Penn2_MultiNet = Penn2_MultiNet.set_index('join_PennShIDs')

# In[238]:

PennXY_MultiID =  Penn2_MultiNet.reset_index().rename(columns = {'RDSTMC_new':'MultiID','join_PennShIDs':'PennShIDs'})[['MultiID','PennShIDs']]

# In[241]:


PennXY_MultiID.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/PennXY_MultiID_20190921.pkl')

# In[28]:


output_loc_engine = create_engine(
    "sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/PennMultiId.db")

# In[30]:


PennXY_MultiID.to_sql(name='PennXY_MultiID', con=output_loc_engine, index=False)
