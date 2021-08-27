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


# # Using road network, get upstream/downstream/bi/biupstream/bidownstream road network 

# In[23]:
import networkx as nx

def shp_2_nx_MultiDiGraph(Map_position):
    """Input: Map position, shapefile;
    Output: Multi_DiGraph"""
    Map = shapefile.Reader(Map_position)
    road_shaperecords = Map.shapeRecords()
    N = nx.MultiDiGraph()
    for segment in road_shaperecords:
        seg_records = dict({'PennShIDs': segment.record[-1]})
        if segment.record[10] == 'N' or segment.record[10] == 'E':
            seg_points = list(zip(list(segment.shape.points[:-1]), list(segment.shape.points[1:], ),
                                  [seg_records] * (len(segment.shape.points) - 1)))
            N.add_edges_from(seg_points)
        elif segment.record[10] == 'S' or segment.record[10] == 'W':
            seg_points = list(zip(list(segment.shape.points[1:]), list(segment.shape.points[:-1], ),
                                  [seg_records] * (len(segment.shape.points) - 1)))
            N.add_edges_from(seg_points)
        else:
            seg_points = list(zip(list(segment.shape.points[1:]), list(segment.shape.points[:-1], ),
                                  [seg_records] * (len(segment.shape.points) - 1)))
            N.add_edges_from(seg_points)
            seg_points = list(zip(list(segment.shape.points[:-1]), list(segment.shape.points[1:], ),
                                  [seg_records] * (len(segment.shape.points) - 1)))
            N.add_edges_from(seg_points)
    return N


# In[30]:


import time

start = time.time()

Net = shp_2_nx_MultiDiGraph(
    Map_position='../../PennShareRoad/RMSSEG_State_Roads/PennShare_PA_south_ids_good/PennShare_PA_south_ids_good.shp')

end = time.time()

print(end - start)

# In[25]:


nx.write_gpickle(Net, "../PANetWork.pkl")

# In[35]:


Net = nx.read_gpickle("../PANetWork.pkl")

# In[36]:


workzone = pd.read_csv("../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/RCRS_2015_17_clean.csv")

# In[37]:


Map = shapefile.Reader(
    '../../PennShareRoad/RMSSEG_State_Roads/PennShare_PA_south_ids_good/PennShare_PA_south_ids_good.shp')
road_shaperecords = Map.shapeRecords()

# In[13]:


PennRoads = gpd.read_file(
    '../../PennShareRoad/RMSSEG_State_Roads/PennShare_PA_south_ids_good/PennShare_PA_south_ids_good.shp')

# In[39]:


PennRoads = PennRoads.set_index('PennShIDs')


# In[40]:


def distPP(P1, P2):
    distP = np.sqrt((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2)
    return distP


# In[41]:


def check_route_direction(j, PennRoads_i, nx_Net, start_point_i, end_point_i, direction):
    """To do: identify the bi-way work zones, do not return the ST_NO for inner way work zones"""
    try:
        data = PennRoads_i.loc[nx_Net.get_edge_data(j, start_point_i)[0]['PennShIDs']]  # .ST_RT_NO
        data_xy = data['geometry'].coords[0]
        if ((data.DIR_IND == direction) | (data.DIR_IND == 'B')) & (
                distPP(end_point_i, data_xy) > distPP(start_point_i, end_point_i)):
            return data.ST_RT_NO
        else:
            return '9999'
    except:
        return '9999'


# In[42]:


def prede_successors(start_point, end_point, predecessor_list, successor_list,
                     direction, wz_routenumber, nx_Net, distance_threshold, wzshploc, PennRoads):
    dist_i = 0
    start_point_i = start_point
    end_point_i = end_point
    while dist_i < distance_threshold:
        precessor_i = list(nx_Net.predecessors(start_point_i))
        if len(precessor_i) <= 1:
            precessor_i = precessor_i[0]
        elif len(precessor_i) > 1:
            RouteNumbers = [check_route_direction(j, PennRoads, nx_Net, start_point_i, end_point_i, direction) for j in
                            precessor_i]
            try:
                precessor_i = precessor_i[RouteNumbers.index(wz_routenumber)]
            except:
                """Need to make sure this step won't be a self-loop"""
                precessor_i = precessor_i[0]
        dist_i = dist_i + distPP(tuple(precessor_i), start_point_i)
        """2019-09-20 update: add PennShID output"""
        predecessor_list.append(
            list([precessor_i, dist_i, direction, nx_Net[precessor_i][start_point_i][0]['PennShIDs']]))
        start_point_i = precessor_i
    dist_i = 0
    while dist_i < distance_threshold:
        successor_i = list(nx_Net.successors(end_point_i))
        if len(successor_i) <= 1:
            successor_i = successor_i[0]
        elif len(successor_i) > 1:
            RouteNumbers = [check_route_direction(j, PennRoads, nx_Net, end_point_i, start_point_i, direction) for j in
                            successor_i]
            try:
                successor_i = successor_i[RouteNumbers.index(wz_routenumber)]
            except:
                successor_i = successor_i[0]
        dist_i = dist_i + distPP(tuple(successor_i), end_point_i)
        """2019-09-20 update: add PennShID output"""
        successor_list.append(list([successor_i, dist_i, direction, nx_Net[end_point_i][successor_i][0]['PennShIDs']]))
        end_point_i = successor_i
    return predecessor_list, successor_list


# In[43]:


def workzone_dir_bi(start_point, end_point):
    workzone_dir = str('')
    if start_point[0] - end_point[0] < 0:
        workzone_dir = workzone_dir + 'E'
    else:
        workzone_dir = workzone_dir + 'W'
    if start_point[1] - end_point[1] < 0:
        workzone_dir = workzone_dir + 'N'
    else:
        workzone_dir = workzone_dir + 'S'
    return workzone_dir


# In[44]:


def prede_successors_bi(start_point, end_point, predecessor_list, successor_list,
                        wz_routenumber, nx_Net, distance_threshold, wzshploc, PennRoads):
    dist_i = 0
    start_point_i = start_point
    end_point_i = end_point
    workzone_dir = workzone_dir_bi(start_point, end_point)
    while dist_i < distance_threshold:
        precessor_i = list(nx_Net.predecessors(start_point_i))
        if len(precessor_i) <= 1:
            precessor_i = precessor_i[0]
        elif len(precessor_i) > 1:
            RouteNumbers = [check_route_direction(j, PennRoads, nx_Net, start_point_i, end_point_i, workzone_dir) for j
                            in precessor_i]
            try:
                precessor_i = precessor_i[RouteNumbers.index(wz_routenumber)]
            except:
                """Need to make sure this step won't be a self-loop"""
                precessor_i = precessor_i[0]
        dist_i = dist_i + distPP(tuple(precessor_i), start_point_i)
        """2019-09-20 update: add PennShID output"""
        predecessor_list.append(
            list([precessor_i, dist_i, workzone_dir, nx_Net[precessor_i][start_point_i][0]['PennShIDs']]))
        #         predecessor_list.append(list([precessor_i,dist_i,workzone_dir]))
        start_point_i = precessor_i
    dist_i = 0
    while dist_i < distance_threshold:
        successor_i = list(nx_Net.successors(end_point_i))
        if len(successor_i) <= 1:
            successor_i = successor_i[0]
        elif len(successor_i) > 1:
            RouteNumbers = [check_route_direction(j, PennRoads, nx_Net, end_point_i, start_point_i, workzone_dir) for j
                            in successor_i]
            try:
                successor_i = successor_i[RouteNumbers.index(wz_routenumber)]
            except:
                successor_i = successor_i[0]
        dist_i = dist_i + distPP(tuple(successor_i), end_point_i)
        """2019-09-20 update: add PennShID output"""
        successor_list.append(
            list([successor_i, dist_i, workzone_dir, nx_Net[end_point_i][successor_i][0]['PennShIDs']]))

        #         successor_list.append(list([successor_i,dist_i,workzone_dir]))
        end_point_i = successor_i
    return predecessor_list, successor_list


# In[45]:


def wzshp_predecessor_successor(wzshploc, nx_Net, distance_threshold, wz_direction, PennRoads):
    wzi = shapefile.Reader(wzshploc).shapeRecords()
    segs = [int(i.record[4]) for i in wzi]
    s_i_min = segs.index(np.min(segs))
    s_i_max = segs.index(np.max(segs))
    if wzi[0].record[10] == 'N' or wzi[0].record[10] == 'E':
        predecessor_list, successor_list = prede_successors(wzi[s_i_min].shape.points[1], wzi[s_i_max].shape.points[-2],
                                                            [], [], wzi[0].record[10], str(wzi[0].record[0]).zfill(4),
                                                            nx_Net, distance_threshold, wzshploc, PennRoads)
    elif wzi[0].record[10] == 'S' or wzi[0].record[10] == 'W':
        predecessor_list, successor_list = prede_successors(wzi[s_i_max].shape.points[-2], wzi[s_i_min].shape.points[1],
                                                            [], [], wzi[0].record[10], str(wzi[0].record[0]).zfill(4),
                                                            nx_Net, distance_threshold, wzshploc, PennRoads)
    else:
        # print(wzi[s_i_min].shape.points[1])
        # print(wzi[s_i_max].shape.points[-2])
        predecessor_list, successor_list = prede_successors_bi(wzi[s_i_min].shape.points[1],
                                                               wzi[s_i_max].shape.points[-2],
                                                               [], [], str(wzi[0].record[0]).zfill(4), nx_Net,
                                                               distance_threshold, wzshploc, PennRoads)
        predecessor_list, successor_list = prede_successors_bi(wzi[s_i_max].shape.points[-2],
                                                               wzi[s_i_min].shape.points[1],
                                                               predecessor_list, successor_list,
                                                               str(wzi[0].record[0]).zfill(4), nx_Net,
                                                               distance_threshold, wzshploc, PennRoads)
    return successor_list, predecessor_list


# In[35]:


successor, predecessor = wzshp_predecessor_successor(
    wzshploc='../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile0.shp',
    nx_Net=Net, distance_threshold=400, wz_direction=str(workzone.DIRECTION.values[0])[0], PennRoads=PennRoads)


# In[48]:


def Get_upstream_downstream(distance_threshold=350):
    downs = []
    ups = []
    for i in range(len(workzone)):
        try:
            downstream, upstream = wzshp_predecessor_successor(
                wzshploc='../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile' + str(i) + '.shp',
                nx_Net=Net, distance_threshold=distance_threshold, wz_direction=str(workzone.DIRECTION.values[i])[0],
                PennRoads=PennRoads)
            [j.append(i) for j in downstream]
            [j.append(i) for j in upstream]
        except:
            downstream = [[(-1, -1), -1, 'A', -1, i]]
            upstream = [[(-1, -1), -1, 'A', -1, i]]
        downs.append(downstream)
        ups.append(upstream)
    return downs, ups


# In[ ]:


downstream_Nodes, upstream_Nodes = Get_upstream_downstream()


# In[49]:


def Get_bi_upstream_downstream(distance_threshold=350):
    downs = []
    ups = []
    for i in range(len(workzone)):
        try:
            downstream, upstream = wzshp_predecessor_successor(
                wzshploc='../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile_bi/shapefile' + str(
                    i) + '.shp',
                nx_Net=Net, distance_threshold=distance_threshold, wz_direction=str(workzone.DIRECTION.values[i])[0],
                PennRoads=PennRoads)
            [j.append(i) for j in downstream]
            [j.append(i) for j in upstream]
        except:
            downstream = [[(-1, -1), -1, 'A', -1, i]]
            upstream = [[(-1, -1), -1, 'A', -1, i]]
        downs.append(downstream)
        ups.append(upstream)
    return downs, ups


# In[ ]:


bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream()


# In[50]:


def get_shape_points_in(i):
    try:
        wztest = shapefile.Reader('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile' + str(
            i) + '.shp').shapeRecords()

        """something need to be correct here"""
        # dire = str(wztest.rec)
        # dire = str(workzone.DIRECTION.values[i])[0]
        #         PennShID = workzone
        return [[j[0], j[1], m.record[10], m.record[-1], i] for m in wztest for j in m.shape.points]
    except:
        return [[-1, -1, 'A', -1, -1]]


# In[51]:


def get_shape_points_bi_in(i):
    try:
        wztest = shapefile.Reader('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile_bi/shapefile' + str(
            i) + '.shp').shapeRecords()
        #         dire = str(workzone.DIRECTION.values[i])[0]
        return [[j[0], j[1], m.record[10], m.record[-1], i] for m in wztest for j in m.shape.points]
    except:
        return [[-1, -1, 'A', -1, -1]]


# In[52]:


def creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone):
    wzup = pd.DataFrame.from_records([[i[0][0], i[0][1], i[2], i[3], i[4]] for m in upstream_Nodes for i in m],
                                     columns=['x', 'y', 'direct', 'PennShID', 'wzID'])
    wzdown = pd.DataFrame.from_records([[i[0][0], i[0][1], i[2], i[3], i[4]] for m in downstream_Nodes for i in m],
                                       columns=['x', 'y', 'direct', 'PennShID', 'wzID'])
    wzup_bi = pd.DataFrame.from_records([[i[0][0], i[0][1], i[2], i[3], i[4]] for m in bi_upstream_Nodes for i in m],
                                        columns=['x', 'y', 'direct', 'PennShID', 'wzID'])
    wzdown_bi = pd.DataFrame.from_records(
        [[i[0][0], i[0][1], i[2], i[3], i[4]] for m in bi_downstream_Nodes for i in m],
        columns=['x', 'y', 'direct', 'PennShID', 'wzID'])
    wz_in = [n for m in [get_shape_points_in(i) for i in range(len(workzone))] for n in m]
    wz_in = pd.DataFrame.from_records(wz_in, columns=['x', 'y', 'direct', 'PennShID', 'wzID'])
    wz_bi_in = [n for m in [get_shape_points_bi_in(i) for i in range(len(workzone))] for n in m]
    wz_bi_in = pd.DataFrame.from_records(wz_bi_in, columns=['x', 'y', 'direct', 'PennShID', 'wzID'])

    wzup['location'] = 'up'
    wzdown['location'] = 'down'
    wzup_bi['location'] = 'bi_up'
    wzdown_bi['location'] = 'bi_down'
    wz_in['location'] = 'in'
    wz_bi_in['location'] = 'bi_in'

    wz_type_xy = pd.concat([wz_in, wz_bi_in, wzup, wzdown, wzup_bi, wzdown_bi], axis=0)
    return wz_type_xy


# In[53]:


downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=518)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=518)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_518m.pkl')

# In[54]:


downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=61)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=61)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_61m.pkl')

# In[ ]:


downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=300)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=300)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_300m.pkl')

downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=250)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=250)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_250m.pkl')

downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=200)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=200)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_200m.pkl')

downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=150)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=150)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_150m.pkl')

downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=100)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=100)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_100m.pkl')

downstream_Nodes, upstream_Nodes = Get_upstream_downstream(distance_threshold=50)
bi_downstream_Nodes, bi_upstream_Nodes = Get_bi_upstream_downstream(distance_threshold=50)
wz_type_xy = creat_WZ_type_XYs(upstream_Nodes, downstream_Nodes, bi_upstream_Nodes, bi_downstream_Nodes, workzone)
wz_type_xy.to_pickle('../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_50m.pkl')


# In[ ]:


def correct_wz_type_xy(wz_type_xy):
    return pd.concat([wz_type_xy[wz_type_xy.location == 'in'], wz_type_xy[wz_type_xy.location == 'bi_in'],
                      wz_type_xy[wz_type_xy.location == 'up'].rename(
                          columns={'wzID': 'PennShID_2', 'PennShID': 'wzID'}).rename(
                          columns={'PennShID_2': 'PennShID'}),
                      wz_type_xy[wz_type_xy.location == 'down'].rename(
                          columns={'wzID': 'PennShID_2', 'PennShID': 'wzID'}).rename(
                          columns={'PennShID_2': 'PennShID'}),
                      wz_type_xy[wz_type_xy.location == 'bi_up'].rename(
                          columns={'wzID': 'PennShID_2', 'PennShID': 'wzID'}).rename(
                          columns={'PennShID_2': 'PennShID'}),
                      wz_type_xy[wz_type_xy.location == 'bi_down'].rename(
                          columns={'wzID': 'PennShID_2', 'PennShID': 'wzID'}).rename(
                          columns={'PennShID_2': 'PennShID'})], axis=0, sort=True)


# In[ ]:


for i in [50, 100, 150, 200, 250, 300]:
    wz_type_xy = pd.read_pickle(
        '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_' + str(i) + 'm.pkl')
    correct_wz_type_xy(wz_type_xy).to_pickle(
        '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_' + str(i) + 'm1107.pkl')

# In[3]:


from sqlalchemy import create_engine
import sqlite3
from sqlalchemy import Column, Integer, String, ForeignKey, Float

# In[4]:


wz_loc_engine = create_engine(
    'sqlite:////media/andy/b4a51c70-19cd-420f-91e4-c7adf2274c39/WorkZone/Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_loc.db',
    echo=False)

# In[11]:


wz_type_xy = pd.read_pickle(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_518m.pkl')

# In[7]:


wz_type_xy.to_sql(name='wz_loc_518', con=wz_loc_engine,
                  dtype={'x': Float(), 'y': Float(), 'direct': String(), 'PennShID': Integer(), 'wzID': Integer(),
                         'location': String()},
                  index=False, chunksize=1000, if_exists='replace')

# In[8]:


wz_loc_engine.execute("CREATE INDEX wz_loc_518_id_loc on wz_loc_518(wzID,location);")

# In[19]:


wz_loc_engine.execute("CREATE INDEX wz_loc_518_id_loc_Pid on wz_loc_518(wzID,location,PennShID);")

# In[ ]:


wz_loc_engine.execute("CREATE INDEX wz_loc_61_id_loc_Pid on wz_loc_61(wzID,location,PennShID);")

# In[9]:


wz_type_xy = pd.read_pickle(
    '../CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/wz_type_xy_20191014_61m.pkl')

wz_type_xy.to_sql(name='wz_loc_61', con=wz_loc_engine,
                  dtype={'x': Float(), 'y': Float(), 'direct': String(), 'PennShID': Integer(), 'wzID': Integer(),
                         'location': String()},
                  index=False, chunksize=1000, if_exists='replace')

wz_loc_engine.execute("CREATE INDEX wz_loc_61_id_loc on wz_loc_61(wzID,location);")

# In[18]:


wz_loc_engine.execute("CREATE INDEX wz_loc_61_id_loc_Pid on wz_loc_61(wzID,location,PennShID);")
