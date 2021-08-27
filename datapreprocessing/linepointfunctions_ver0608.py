import shapefile
# import finoa
import shapely
# import matplotlib
import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
from pyproj import Proj, transform

# import stateplane


__author__ = 'Zhuoran Zhang'


def distPL(Point, lineseg):
    # input:Point(x,y);lineseg[(x,y),(x,y),(x,y)...]
    # output:distance
    xp, yp = Point[0], Point[1]  # lat lon
    distlist = []
    for i in range(len(lineseg) - 1):
        x1, y1 = lineseg[i][0], lineseg[i][1]
        x2, y2 = lineseg[i + 1][0], lineseg[i + 1][1]
        point = [x1, y1, x2, y2]
        dist12 = [np.sqrt((xp - x1) ** 2 + (yp - y1) ** 2), np.sqrt((xp - x2) ** 2 + (yp - y2) ** 2)]
        dist3 = (abs((y2 - y1) * xp - (x2 - x1) * yp + x2 * y1 - y2 * x1)) / (np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        if x1 == x2:
            if yp > min(y1, y2) and yp < max(y1, y2):
                dist = dist3
            else:
                dist = np.min(dist12)
        elif y1 == y2:
            if xp > min(x1, x2) and xp < max(x1, x2):
                dist = dist3
            else:
                dist = np.min(dist12)
        else:
            k = (y2 - y1) / (x2 - x1)
            x0 = (k ** 2 * x1 + k * (yp - y1) + xp) / (k ** 2 + 1)
            y0 = k * (x0 - x1) + y1
            if x0 > min(x1, x2) and x0 < max(x1, x2) and y0 > min(y1, y2) and y0 < max(y1, y2):
                dist = dist3
            else:
                dist = np.min(dist12)
        distlist.append(dist)
    return np.min(distlist)


def distPP(P1, P2):
    distP = np.sqrt((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2)
    return distP


def PointinBox1(LON, LAT, bufferlat, bufferlon, road):
    if road.shape.bbox[0] - bufferlon < LON and road.shape.bbox[2] + bufferlon > LON \
            and road.shape.bbox[1] - bufferlat < LAT and road.shape.bbox[3] + bufferlat > LAT:
        return True
    else:
        return False


def caldist_pl(x0, y0, points):
    # input: a point, and a list of line points pairs
    # return the dictionary of points and dist, with format{index:points} \
    # and {index:dist}
    # inProj = Proj(init='epsg:4269')#NAD83
    # outProj = Proj(init='epsg:32618')# WGS84 UTM18N
    results = []
    for i in range(len(points) - 1):
        x1, y1 = points[i][0], points[i][1]
        x2, y2 = points[i + 1][0], points[i + 1][1]
        point = [x1, y1, x2, y2]
        dist12 = [np.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2), np.sqrt((x0 - x2) ** 2 + (y0 - y2) ** 2)]
        dist3 = (abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)) / (np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        if x1 == x2:
            if y0 > min(y1, y2) and y0 < max(y1, y2):
                dist = dist3
                keypoint = [x1, y0]
            else:
                dist = np.min(dist12)
                keypoint = [x1, points[i + dist12.index(dist)][1]]
        elif y1 == y2:
            if x0 > min(x1, x2) and x0 < max(x1, x2):
                dist = dist3
                keypoint = [x0, y1]
            else:
                dist = np.min(dist12)
                keypoint = [points[i + dist12.index(dist)][0], y1]
        else:
            k = (y2 - y1) / (x2 - x1)
            xk = (k ** 2 * x1 + k * (y0 - y1) + x0) / (k ** 2 + 1)
            yk = k * (xk - x1) + y1
            if xk > min(x1, x2) and xk < max(x1, x2) and yk > min(y1, y2) and yk < max(y1, y2):
                dist = dist3
                keypoint = [xk, yk]
            else:
                dist = np.min(dist12)
                keypoint = [points[i + dist12.index(dist)][0], points[i + dist12.index(dist)][1]]
        # return the position of work zone!
        detail_1 = {'points': [points[i][0], points[i][1], points[i + 1][0], points[i + 1][1]], 'dist': dist,
                    'keyp': keypoint}
        results = np.append(results, detail_1)
    return {'detail': results}
    # return {detail':[{'points':[33,78,34,76],'dist':44},{'points':[23,68,44,86],'dist':46,'keyp':keypoint(lon,lat)
    # the new work zone position after mapping with roadway}]}


def cross_prod(p, q):
    assert len(p) == 2 and len(q) == 2
    return p[0] * q[1] - p[1] * q[0]


def rect_overlap(r1, r2):
    return not (((r1[1][0] < r2[0][0]) | (r1[0][1] > r2[1][1])) \
                | ((r2[1][0] < r1[0][0]) | (r2[0][1] > r1[1][1])))


def line_intersection(p1, p2, q1, q2):
    return False if not rect_overlap([p1, p2], [q1, q2]) else \
        (True if cross_prod(p1 - q1, q2 - q1) * cross_prod(q2 - q1, p2 - q1) >= 0 else False)


def get_minP_list(wz_lon, wz_lat, start_list):
    # input: the dictionary list, get the minimum dist,
    # and extract the corresponding points pairs
    # output: the posints list
    # indexs = [i['index'] for i in start_list]
    details = [i['detail'] for i in start_list]
    dists = [m['dist'] for j in details for m in j]
    points = [m['points'] for j in details for m in j]
    keypoints = [m['keyp'] for j in details for m in j]

    if dists == []:
        return [0, 0], -9999, [[0, 0]]
    else:
        minimum = np.min(dists)
        indices = [i for i, v in enumerate(dists) if v == minimum]

    return [points[i] for i in indices], minimum, [keypoints[i] for i in indices]


def direction_match(wzdiri, roaddiri):
    if str(wzdiri)[0:1] == roaddiri:
        return True
    elif (str(wzdiri)[0:1] == 'B') and (roaddiri == 'O'):
        return True
    elif roaddiri == 'B':
        return True
    else:
        return False


def min_wz_roadway_points(wz_route, wz_start, wz_end, workzone_DIRECTION, road_shaperecords):
    # input: the wz information and road information,
    # output: the shortest-distance points pair for each wz
    end_minP_list = []
    start_minP_list = []
    start_minDist_list = []
    end_minDist_list = []
    start_keyp_list = []
    end_keyp_list = []
    for i in range(len(wz_route)):
        start_list = []
        end_list = []
        for road in road_shaperecords:
            if str(wz_route[i]).zfill(4) == road.record[0]:
                if direction_match(workzone_DIRECTION[i], road.record[10]):
                    # print(0)
                    if PointinBox1(wz_start["x_bgn"][i], wz_start["y_bgn"][i], 5000, 5000, road):
                        # print(1)
                        start_list = \
                            np.append(start_list, caldist_pl(wz_start["x_bgn"][i], \
                                                             wz_start["y_bgn"][i], \
                                                             road.shape.points))
                    if PointinBox1(wz_end["x_end"][i], wz_end["y_end"][i], 5000, 5000, road):
                        end_list = \
                            np.append(end_list, caldist_pl(wz_end["x_end"][i], \
                                                           wz_end["y_end"][i], \
                                                           road.shape.points))
            else:
                continue
        start_minPs, start_minDists, start_keyp = get_minP_list(wz_start["x_bgn"][i], \
                                                                wz_start["y_bgn"][i], start_list)
        end_minPs, end_minDists, end_keyp = get_minP_list(wz_end["x_end"][i], \
                                                          wz_end["y_end"][i], end_list)

        start_minP_list.append(start_minPs)
        end_minP_list.append(end_minPs)
        start_minDist_list.append(start_minDists)
        end_minDist_list.append(end_minDists)
        start_keyp_list.append(start_keyp)
        end_keyp_list.append(end_keyp)

    return start_minP_list, end_minP_list, start_minDist_list, end_minDist_list, start_keyp_list, end_keyp_list


def RoadwayProj(inposition, outposition, sproj='north'):
    roads = shapefile.Reader(inposition)
    road_shaperecords = roads.shapeRecords()
    w = shapefile.Writer()
    w.fields = roads.fields[1:]
    records = []
    points = []
    inProj = Proj(init='epsg:4269')  # NAD83
    if sproj == 'north':
        outProj = Proj(init='epsg:32128')  # NAD83 / Pennsylvania North
    else:
        outProj = Proj(init='epsg:32129')  # NAD83 / Pennsylvania South
    for road in road_shaperecords:
        records.append([road.record])
        pointspart = []
        for jm in range(len(road.shape.points)):
            x, y = transform(inProj, outProj, road.shape.points[jm][0], road.shape.points[jm][1])
            # x,y = stateplane.from_lonlat(road.shape.points[jm][0],road.shape.points[jm][1],statefp=statefpi)
            # print(x,y)
            pointspart.append((x, y))
        points.append([pointspart])

    # print(points)

    for idx in range(len(records)):
        w.line(parts=points[idx])
        w.record(*records[idx][0])
        # print(records[idx][0])
    w.save(outposition)


def ProjWorkZone(workzone):
    inProj = Proj(init='epsg:4269')
    outProj = Proj(init='epsg:32129')  # NAD83 / Pennsylvania South
    workzone['x_bgn'] = transform(inProj, outProj, workzone["LOCATION_LONG_BGN"], workzone["LOCATION_LAT_BGN"])[0]
    workzone['y_bgn'] = transform(inProj, outProj, workzone["LOCATION_LONG_BGN"], workzone["LOCATION_LAT_BGN"])[1]
    workzone['x_end'] = transform(inProj, outProj, workzone["LOCATION_LONG_END"], workzone["LOCATION_LAT_END"])[0]
    workzone['y_end'] = transform(inProj, outProj, workzone["LOCATION_LONG_END"], workzone["LOCATION_LAT_END"])[1]
    return workzone

# want to write a function to calculate dist(point,line_segment),
# it would be easier with calculate_dist function

# with this, I can write a function to justify whether point is in buffer distance of a line segment

# then I could be more efficiency for match points

# I also could be possible to find the inner line, yeah!
