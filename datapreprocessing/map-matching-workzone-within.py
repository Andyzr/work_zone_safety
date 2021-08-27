# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import shapefile
import fiona
# import shapely
import numpy as np
import matplotlib.pyplot as plt

get_ipython().magic('matplotlib inline')
import pandas as pd
from pyproj import Proj, transform
import csv
# import stateplane


# %%
from linepointfunctions_ver0608 import min_wz_roadway_points, RoadwayProj, ProjWorkZone

# %% [markdown]
# # Transform the projection of Pasda Roadways

# %%
RoadwayProj("./Map/Pasda/PaStateRoads2014_02/PaStateRoads2014_02.shp",
            './Map/Pasda/PaStateRoads2014_02/PaStateRoads2014_02_state_south.shp', 'south')

# %%
workzone = pd.read_csv("./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/RCRS_2015_17_clean.csv")
workzone = workzone.apply(ProjWorkZone, axis=1)
workzone.to_csv("./RCRS_2013_allen0519_projed.csv", sep=',', index=False)

# %% [markdown]
# # Import the Roadway and Workzone Data

# %%
roads = shapefile.Reader(
    "../PennShareRoad/RMSSEG_State_Roads/PennShare_PA_south_ids_good/PaStateRoads2014_02_state_south.shp")
wz_start = workzone[["x_bgn", "y_bgn"]]
wz_end = workzone[["x_end", "y_end"]]
wz_route = workzone["ST_RT_NO"]
road_shaperecords = roads.shapeRecords()

# %% [markdown]
# Work zone data saved at wz_route, wz_start and wz_end. Roadway data saved at road_shaperecords
# %% [markdown]
# # Locate the work zone with the roadway

# %%

start_seg, end_seg, start_minDist_list, end_minDist_list, start_keyp_list, end_keyp_list = min_wz_roadway_points(
    workzone["ST_RT_NO"], workzone[["x_bgn", "y_bgn"]], workzone[["x_end", "y_end"]], workzone["DIRECTION"],
    road_shaperecords)

# %%
wz_dir_bi_dict = {'BOTH': 'BOTH', 'EAST': 'WEST', 'WEST': 'EAST', 'NORTH': "SOUTH", 'SOUTH': 'NORTH'}

# %%
wz_bi_dir = pd.Series([wz_dir_bi_dict[i] for i in workzone["DIRECTION"].values])

# %%

start_seg_bi, end_seg_bi, start_minDist_list_bi, end_minDist_list_bi, start_keyp_list_bi, end_keyp_list_bi = min_wz_roadway_points(
    workzone["ST_RT_NO"], workzone[["x_bgn", "y_bgn"]], workzone[["x_end", "y_end"]], wz_bi_dir, road_shaperecords)

# %%
import json

with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/start_seg_0610.txt', 'w') as out_file:
    json.dump(start_seg, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/end_seg_0610.txt', 'w') as out_file:
    json.dump(end_seg, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/start_minDist_list_0610.txt', 'w') as out_file:
    json.dump(start_minDist_list, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/end_minDist_list_0610.txt', 'w') as out_file:
    json.dump(end_minDist_list, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/start_keyp_list_0610.txt', 'w') as out_file:
    json.dump(start_keyp_list, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/end_keyp_list_0610.txt', 'w') as out_file:
    json.dump(end_keyp_list, out_file)

# %%
import json

with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/start_seg_0610_bi.txt', 'w') as out_file:
    json.dump(start_seg_bi, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/end_seg_0610_bi.txt', 'w') as out_file:
    json.dump(end_seg_bi, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/start_minDist_list_0610_bi.txt', 'w') as out_file:
    json.dump(start_minDist_list_bi, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/end_minDist_list_0610_bi.txt', 'w') as out_file:
    json.dump(end_minDist_list_bi, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/start_keyp_list_0610_bi.txt', 'w') as out_file:
    json.dump(start_keyp_list_bi, out_file)
with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/end_keyp_list_0610_bi.txt', 'w') as out_file:
    json.dump(end_keyp_list_bi, out_file)


# %%
# get the unique points of each start point
def uniquelist(start_keyp_list):
    start_new_key = []
    for i in range(len(start_keyp_list)):
        if len(start_keyp_list[i]) == 1:
            start_new_key.append(start_keyp_list[i])
        else:
            for j in range(len(start_keyp_list[i]) - 1):
                key = [start_keyp_list[i][0]]
                if start_keyp_list[i][j] == start_keyp_list[i][j + 1]:
                    continue
                else:
                    key.append(start_keyp_list[i][j + 1])
            start_new_key.append(key)
    return start_new_key

startkeyuni = uniquelist(start_keyp_list)
endkeyuni = uniquelist(end_keyp_list)

startkeyuni_bi = uniquelist(start_keyp_list_bi)
endkeyuni_bi = uniquelist(end_keyp_list_bi)

# %%
csvfile = "./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/startkeypoint.csv"
# Assuming res is a list of lists
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['lon', 'lat'])
    writer.writerows([[key[0][0], key[0][1]] for key in startkeyuni])
csvfile = "./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/endkeypoint.csv"
# Assuming res is a list of lists
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['lon', 'lat'])
    writer.writerows([[key[0][0], key[0][1]] for key in endkeyuni])

# %%
csvfile = "./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/startkeypoint_bi.csv"
# Assuming res is a list of lists
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['lon', 'lat'])
    writer.writerows([[key[0][0], key[0][1]] for key in startkeyuni_bi])
csvfile = "./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/endkeypoint_bi.csv"
# Assuming res is a list of lists
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['lon', 'lat'])
    writer.writerows([[key[0][0], key[0][1]] for key in endkeyuni_bi])

# %% [markdown]
# # Find Splitted Lines

# %%
from linepointfunctions_split_0610_20190920 import callinelength2019

# %%
startkeyuni = pd.read_csv('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/startkeypoint.csv', delimiter=',')
startkeyuni = startkeyuni.values
endkeyuni = pd.read_csv('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/endkeypoint.csv', delimiter=',')
endkeyuni = endkeyuni.values

startkeyuni = [[[i[0], i[1]]] for i in startkeyuni]
endkeyuni = [[[i[0], i[1]]] for i in endkeyuni]

# %%
startkeyuni_bi = pd.read_csv('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/startkeypoint_bi.csv',
                             delimiter=',')
startkeyuni_bi = startkeyuni_bi.values
endkeyuni_bi = pd.read_csv('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/endkeypoint_bi.csv', delimiter=',')
endkeyuni_bi = endkeyuni_bi.values

startkeyuni_bi = [[[i[0], i[1]]] for i in startkeyuni_bi]
endkeyuni_bi = [[[i[0], i[1]]] for i in endkeyuni_bi]

# %%
from linepointfunctions_split_0610_20190920 import FindSplittedLine7

# %%
import multiprocessing as mp


# %%
def helper_wzsplit(i):
    try:
        FindSplittedLine7(i, roads, road_shaperecords, endkeyuni, startkeyuni, wz_route, 10, 10, workzone["DIRECTION"],
                          fileloc="./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile")
    except:
        with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/badcases.csv', "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([str(i)])
        output.close()


# %%
def helper_wzsplit_bi(i):
    try:
        FindSplittedLine7(i, roads, road_shaperecords, endkeyuni_bi, startkeyuni_bi, wz_route, 10, 10, wz_bi_dir,
                          fileloc="./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile_bi/shapefile")
    except:
        with open('./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/badcases_bi.csv', "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([str(i)])
        output.close()


# %%

pool = mp.Pool(processes=3)
speeds_in = pool.map(helper_wzsplit, range(len(workzone)))
pool.close()

# %%

pool = mp.Pool(processes=3)
speeds_in = pool.map(helper_wzsplit_bi, range(len(workzone)))
pool.close()

# %%
netlength = []
for i in range(len(workzone)):
    try:
        netlength.append(
            callinelength2019(i, loc='./CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile'))
    except:
        print(i)
        netlength.append(-9999)

# %%
workzone['NetLength'] = netlength

# %%
wz_gcd = workzone["GCD"]

# %% [markdown]
# # Add lane counts, AADT, urban/rural

# %%
import geopandas as gpd


# %%
def FindLaneAADTUrban(wzi, Flocation="../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile"):
    try:
        wz_gpd = gpd.read_file(Flocation + str(wzi['cleanID'] - 1) + ".shp")
        wz_gpd['length'] = wz_gpd.length

        wzi['LaneCounts'] = np.min(wz_gpd['LANE_CNT'])
        wzi['AADT'] = np.sum(wz_gpd.CUR_AADT.values * wz_gpd.length.values) / np.sum(wz_gpd.length.values)
        wzi['NHS_IND'] = wz_gpd['NHS_IND'][np.argmax(wz_gpd.length)]
        wzi['PA_BYWAY_I'] = wz_gpd['PA_BYWAY_I'][np.argmax(wz_gpd.length)]
    except:
        wzi['LaneCounts'] = -1
        wzi['AADT'] = -1
        wzi['NHS_IND'] = -1
        wzi['PA_BYWAY_I'] = -1
    return wzi


# %%
workzone_lanes = workzone.apply(FindLaneAADTUrban, axis=1)

# %%
workzone_lanes.to_csv("../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/workzone_lane_AADT20190917.csv",
                      sep=',', index=False)

# %%
from datetime import datetime


# datetime.strptime('201301030901', '%Y%m%d%H%M').timestamp()
def wzduration(wz_i):
    wz_i['duration'] = datetime.strptime(str(wz_i['ACT_DATE_TIME_OPENED_QRY']),
                                         '%Y%m%d%H%M').timestamp() - datetime.strptime(
        str(wz_i['DATE_TIME_CLOSED_QRY']), '%Y%m%d%H%M').timestamp()
    return wz_i


# %%
workzone_lanes = workzone_lanes.apply(wzduration, axis=1)

# %%
workzone_lanes.to_csv(
    "../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/workzone_lane_AADT_duration20190917.csv", sep=',',
    index=False)

# %% [markdown]
# # Number of ramps, intersections

# %%
import geopandas as gpd

# %%
PennShare = gpd.read_file('../PennShareRoad/RMSSEG_State_Roads/PennShare_PA_south.shp')

# %%
PennNotNull = PennShare[(PennShare['geometry'].notnull().values)].reset_index()

# %%
PennNotNull_bounds = PennNotNull.bounds

# %%
from shapely.geometry import Point

# %%
import os
import csv


# %%
def IntersectionRamps(i, PennNotNull_bounds=PennNotNull_bounds, PennNotNull=PennNotNull, bufferx=1000, buffery=1000):
    if os.path.isfile(
            "../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile" + str(i) + ".shp"):
        try:
            wzi = gpd.read_file(
                "../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/shapefile/shapefile" + str(i) + ".shp")
        except:
            print('cannot read file! workzone' + str(i))
            with open('../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/inter_badcases2.csv', "a") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow([str(i), 'cannot read file'])
            output.close()
            return 0, 0, []
    else:
        print('file not existed! workzone' + str(i))
        with open('../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/inter_badcases2.csv', "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([str(i), 'file not existed'])
        output.close()
        return 0, 0, []
    try:
        xmin, ymin, xmax, ymax = wzi.total_bounds
        PennNotNull_sub0 = PennNotNull[
            (PennNotNull_bounds.minx > xmin - bufferx) & (PennNotNull_bounds.maxx < xmax + bufferx) & (
                    PennNotNull_bounds.miny > ymin - buffery) & (PennNotNull_bounds.maxy < ymax + buffery)]
        PennNotNull_sub = PennNotNull_sub0[((PennNotNull_sub0.ST_RT_NO != wzi.iloc[0].ST_RT_NO) | (
                PennNotNull_sub0.DIR_IND != wzi.iloc[0].DIR_IND))].reset_index(drop=True)

        sgeo = gpd.GeoSeries()
        egeo = gpd.GeoSeries()
        for jpennR in range(len(PennNotNull_sub)):
            if type(PennNotNull_sub.iloc[jpennR]['geometry']) == type(PennNotNull.iloc[0]['geometry']):
                startpoints = gpd.GeoSeries(Point(PennNotNull_sub.iloc[jpennR]['geometry'].coords[0]))
                endpoints = gpd.GeoSeries(Point(PennNotNull_sub.iloc[jpennR]['geometry'].coords[-1]))
            else:
                startpoints = gpd.GeoSeries(Point(PennNotNull_sub.iloc[jpennR]['geometry'][0].coords[0]))
                endpoints = gpd.GeoSeries(Point(PennNotNull_sub.iloc[jpennR]['geometry'][-1].coords[-1]))
            sgeo = sgeo.append(startpoints)
            egeo = egeo.append(endpoints)
        # print(sgeo)
        wz_dup = gpd.GeoDataFrame(geometry=pd.concat([wzi['geometry']] * (len(sgeo) + len(egeo)))).reset_index(
            drop=True)
        points_dup_temp = gpd.GeoSeries(pd.concat([sgeo] * len(wzi))).append(
            gpd.GeoSeries(pd.concat([egeo] * len(wzi))))
        # print(wz_dup)
        # print(points_dup_temp)

        points_dup = gpd.GeoDataFrame()
        points_dup['geometry'] = points_dup_temp
        points_dup = points_dup.reset_index(drop=True)
        # print(points_dup)

        # PennNotNullsub_dup = gpd.GeoDataFrame(pd.concat([PennNotNull_sub['geometry'] ]*len(wzi))).reset_index()
        inter_dist = wz_dup['geometry'].distance(points_dup['geometry']).reset_index(drop=True)
        # print(inter_dist)
        # print(np.sum(inter_dist<1))
        # print(inter_dist)
        # intersects = wz_dup.touches(PennNotNullsub_dup)

        # print(len(PennNotNull_sub))
        # print(intersects)
        intersectedName = [PennNotNull_sub.iloc[i % len(PennNotNull_sub)].STREET_NAM for i in
                           inter_dist[inter_dist < 3].index]
        rampsname = ['RAMP' in namei for namei in intersectedName if type(i) == str]

        # n%len(PennNotNull_sub)

        return np.sum(inter_dist < 1), np.sum(rampsname), intersectedName  # wz_dup,points_dup #
    except:
        print('ramp number calculated incorrect! workzone' + str(i))
        with open('../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/inter_badcases2.csv', "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([str(i), 'ramp number calculated incorrect'])
        output.close()
        return 0, 0, []


# %%
import multiprocessing as mp


# %%
def mp_get_inter_ramp_name(i):
    return IntersectionRamps(i, PennNotNull_bounds=PennNotNull_bounds, PennNotNull=PennNotNull, bufferx=1500,
                             buffery=1500)


# %%
with mp.Pool(3) as p:
    inter_ramp_name = p.map(mp_get_inter_ramp_name, range(len(workzone_lanes)))

# %%
wz_inters = pd.DataFrame([j for j in inter_ramp_name], columns=['NUMinters', 'NUMramps', 'NAMEinter'])

# %%
wz_inters.to_pickle('../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/wz_inters20190917')

# %%
workzone_lanes[['NUM_inters', 'NUM_ramps']] = wz_inters[['NUMinters', 'NUMramps']]

# %%
workzone_lanes['NetLength'] = netlength
workzone_lanes.to_csv(
    "../Data/CMU_rcrs_all_events_2010-2014-selected/RCRS_2015_17/important/workzone_lane_AADT_duration20191106v2.csv",
    sep=',', index=False)
