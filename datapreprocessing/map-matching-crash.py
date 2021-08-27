#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time

# In[2]:


import shapefile
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


# # 0. Match Multiple years crash data

# In[35]:


def map_matching_crash(year='14'):
    crash = pd.read_csv('../Data/crash_data/crash20' + year + '/CRASH.csv', low_memory=False)

    crash = crash[[((i[0][0] != ' ') & (i[1][0] != ' ')) for i in crash[['LATITUDE', 'LONGITUDE']].values]]

    crash = crash.drop(['DEC_LAT', 'DEC_LONG'], axis=1)

    def divide_latlong(string):
        num_list = string.split(':')
        pos = float(num_list[0][0:2])
        pos = pos + float(num_list[0][3:]) / 60
        pos = pos + float(num_list[1]) / 60 / 60
        return pos

    crash['DEC_LAT'] = [divide_latlong(i) for i in crash['LATITUDE'].values]
    crash['DEC_LONG'] = [-(divide_latlong(i)) for i in crash['LONGITUDE'].values]

    crash_route = pd.read_csv('../Data/crash_data/crash20' + year + '/ROADWAY.csv', low_memory=False)

    crash_gravity = crash.groupby('CRN').agg({'DEC_LAT': np.mean, 'DEC_LONG': np.mean}).reset_index()

    roads = shapefile.Reader("../../WorkZone/Data/PennShareRoad/RMSSEG_State_Roads/PennShare_PA_south.shp")
    road_shaperecords = roads.shapeRecords()

    from linepointfunctions_crashver10012018 import Projcrash_roadway, min_wz_Crash_roadway_points2

    import multiprocessing as mp

    def project_crash(crash, crash_route):  # ,road_shaperecords,name='crash_14'):
        crash_gravity = crash.groupby('CRN').agg({'DEC_LAT': np.mean, 'DEC_LONG': np.mean}).reset_index()
        crash_gravity = crash_gravity.merge(right=crash_route[pd.notna(crash_route['ROUTE'])], left_on='CRN',
                                            right_on='CRN', how='inner')
        crash_add_gra_need = Projcrash_roadway(crash_gravity, 'DEC_LONG', 'DEC_LAT', 'x_grav', 'y_grav')
        return crash_add_gra_need

    crash_add_gra_need = project_crash(crash, crash_route)

    def min_crash_PennShare_pool(idx, crash_route=crash_add_gra_need['ROUTE'].values,
                                 crash_xcrash=crash_add_gra_need['x_grav'].values,
                                 crash_ycrash=crash_add_gra_need['y_grav'].values,
                                 crash_RDWY_ORIE=crash_add_gra_need['RDWY_ORIENT'].values,
                                 road_shaperecords=road_shaperecords):
        return min_wz_Crash_roadway_points2(crash_route[idx], crash_xcrash[idx], crash_ycrash[idx],
                                            crash_RDWY_ORIE[idx], road_shaperecords)

    def run_crash_match(crash_add_gra_need, name='crash_' + year):
        pool = mp.Pool(processes=4)
        results_pool = pool.map(min_crash_PennShare_pool, range(len(crash_add_gra_need)))
        pool.close()

        crash_add_gra_need['PennShkeyplist_grav'] = [r[0][0][0] for r in results_pool]
        crash_add_gra_need['PennShIDs_grav'] = [r[3][0][0] for r in results_pool]
        crash_add_gra_need['PennShdist_grav'] = [r[1][0] for r in results_pool]
        crash_add_gra_need['PennShkeyp_grav'] = [r[2][0][0] for r in results_pool]
        crash_add_gra_need['PennShDistInd_grav'] = [int(i) for i in crash_add_gra_need['PennShdist_grav'] <= 100]
        crash_add_gra_need.to_pickle('../Data/' + name + '_keypoint.pkl')
        return crash_add_gra_need

    crash_add_gra = run_crash_match(crash_add_gra_need, name='crash_' + year)


# In[ ]:


map_matching_crash(year='14')
map_matching_crash(year='15')
map_matching_crash(year='16')
map_matching_crash(year='17')
