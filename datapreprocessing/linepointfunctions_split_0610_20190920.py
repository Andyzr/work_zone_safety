import shapefile
# import finoa
import shapely
# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
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


def LineInPointBox(i, startkeyuni, endkeyuni, bufferlat, bufferlon, road):
    if min(endkeyuni[i][0][0], startkeyuni[i][0][0]) - bufferlon < road.shape.bbox[0] and \
            max(endkeyuni[i][0][0], startkeyuni[i][0][0]) + bufferlon > road.shape.bbox[0] and \
            min(endkeyuni[i][0][1], startkeyuni[i][0][1]) - bufferlat < road.shape.bbox[1] and \
            max(endkeyuni[i][0][1], startkeyuni[i][0][1]) + bufferlat > road.shape.bbox[1]:
        return True
    elif min(endkeyuni[i][0][0], startkeyuni[i][0][0]) - bufferlon < road.shape.bbox[2] and \
            max(endkeyuni[i][0][0], startkeyuni[i][0][0]) + bufferlon > road.shape.bbox[2] and \
            min(endkeyuni[i][0][1], startkeyuni[i][0][1]) - bufferlat < road.shape.bbox[3] and \
            max(endkeyuni[i][0][1], startkeyuni[i][0][1]) + bufferlat > road.shape.bbox[3]:
        return True

    else:
        return False


def PointBox(i, startkeyuni, endkeyuni, bufferlat, bufferlon, road):
    if road.shape.bbox[0] - bufferlon < startkeyuni[i][0][0] and road.shape.bbox[2] + bufferlon > startkeyuni[i][0][0] \
            and road.shape.bbox[1] - bufferlat < startkeyuni[i][0][1] and road.shape.bbox[3] + bufferlat > \
            startkeyuni[i][0][1]:
        return True
    elif road.shape.bbox[0] - bufferlon < endkeyuni[i][0][0] and road.shape.bbox[2] + bufferlon > endkeyuni[i][0][0] \
            and road.shape.bbox[1] - bufferlat < endkeyuni[i][0][1] and road.shape.bbox[3] + bufferlat > \
            endkeyuni[i][0][1]:
        return True
    elif min(endkeyuni[i][0][0], startkeyuni[i][0][0]) - bufferlon < road.shape.bbox[0] and \
            max(endkeyuni[i][0][0], startkeyuni[i][0][0]) + bufferlon > road.shape.bbox[0] and \
            min(endkeyuni[i][0][1], startkeyuni[i][0][1]) - bufferlat < road.shape.bbox[1] and \
            max(endkeyuni[i][0][1], startkeyuni[i][0][1]) + bufferlat > road.shape.bbox[1]:
        return True
    elif min(endkeyuni[i][0][0], startkeyuni[i][0][0]) - bufferlon < road.shape.bbox[2] and \
            max(endkeyuni[i][0][0], startkeyuni[i][0][0]) + bufferlon > road.shape.bbox[2] and \
            min(endkeyuni[i][0][1], startkeyuni[i][0][1]) - bufferlat < road.shape.bbox[3] and \
            max(endkeyuni[i][0][1], startkeyuni[i][0][1]) + bufferlat > road.shape.bbox[3]:
        return True

    else:
        return False


def PointInLineBox(i, startkeyuni, bufferlat, bufferlon, roadshapebbox):
    if roadshapebbox[0] - bufferlon < startkeyuni[i][0][0] and roadshapebbox[2] + bufferlon > startkeyuni[i][0][0] \
            and roadshapebbox[1] - bufferlat < startkeyuni[i][0][1] and roadshapebbox[3] + bufferlat > \
            startkeyuni[i][0][1]:
        return True
    else:
        return False


def DrawKeyPoint(i, road_shaperecords, endkeyuni, startkeyuni, wz_start, wz_end, wz_route, bufferlat, bufferlon):
    plt.figure(1)
    # plt.subplot(211)
    for road in road_shaperecords:
        if road.record[0] == str(wz_route[i]).zfill(4):
            shape3 = road
            shape_ex = shape3.shape
            x_lon = []
            y_lat = []
            for ip in range(len(shape_ex.points)):
                lat1 = shape_ex.points[ip][1]
                lon1 = shape_ex.points[ip][0]
                x_lon.append(lon1)
                y_lat.append(lat1)
            # print(x_lon,y_lat)
        # plt.plot(x_lon,y_lat)

    ori_wz_end_lat = wz_end["y_end"][i]
    ori_wz_end_lon = wz_end["x_end"][i]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.plot(ori_wz_end_lon,ori_wz_end_lat,'og',label ='Original End')

    ori_wz_start_lat = wz_start["y_bgn"][i]
    ori_wz_start_lon = wz_start["x_bgn"][i]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.plot(ori_wz_start_lon,ori_wz_start_lat,'ok',label ='Original Start')

    case_wz_end_lat = endkeyuni[i][0][1]
    case_wz_end_lon = endkeyuni[i][0][0]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.plot(case_wz_end_lon,case_wz_end_lat,'*b',label ='Matched End')

    case_wz_start_lat = startkeyuni[i][0][1]
    case_wz_start_lon = startkeyuni[i][0][0]
    # print(case_wz_start_lat, case_wz_start_lon)
    # plt.plot(case_wz_start_lon,case_wz_start_lat,'*r',label ='Matched Start')
    plt.legend(loc='upper right')
    plt.title('Big Map of Work Zone-' + str(i) + " on State Plane")
    plt.savefig("./CMU_rcrs_all_events_08-2015_04-2017/Figures/BigMapStatePlane_" + str(i) + ".png")

    plt.figure(2)
    # plt.subplot(212)

    for road in road_shaperecords:
        if road.record[0] == str(wz_route[i]).zfill(4) and \
                (LineInPointBox(i, startkeyuni, endkeyuni, 1e-2, 1e-2, road) or \
                 PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox) or \
                 PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox)):
            shape3 = road
            shape_ex = shape3.shape
            x_lon = []
            y_lat = []
            for ip in range(len(shape_ex.points)):
                lat1 = shape_ex.points[ip][1]
                lon1 = shape_ex.points[ip][0]
                x_lon.append(lon1)
                y_lat.append(lat1)
            # print(x_lon,y_lat)
        # plt.plot(x_lon,y_lat)
    ori_wz_end_lat = wz_end["y_end"][i]
    ori_wz_end_lon = wz_end["x_end"][i]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.plot(ori_wz_end_lon,ori_wz_end_lat,'og',label ='Original End')

    ori_wz_start_lat = wz_start["y_bgn"][i]
    ori_wz_start_lon = wz_start["x_bgn"][i]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.plot(ori_wz_start_lon,ori_wz_start_lat,'ok',label ='Original Start')

    case_wz_end_lat = endkeyuni[i][0][1]
    case_wz_end_lon = endkeyuni[i][0][0]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.plot(case_wz_end_lon,case_wz_end_lat,'*b',label ='Matched End')

    case_wz_start_lat = startkeyuni[i][0][1]
    case_wz_start_lon = startkeyuni[i][0][0]
    # print(case_wz_start_lat, case_wz_start_lon)
    # plt.plot(case_wz_start_lon,case_wz_start_lat,'*r',label ='Matched Start')
    plt.legend(loc='upper right')
    plt.title('Detailed Map of Work Zone-' + str(i) + " on State Plane")
    plt.savefig("./CMU_rcrs_all_events_08-2015_04-2017/Figures/DetailedMapStatePlane_" + str(i) + ".png")

    plt.show()


def road_direction(wz_direction, startkeyuni_i, road_point_j1):
    wzx, wzy = startkeyuni_i[0][0], startkeyuni_i[0][1]
    roadx, roady = road_point_j1[0], road_point_j1[1]

    if wz_direction == "NORTH":
        if roadx > wzx:
            return True
        else:
            return False
    elif wz_direction == "SOUTH":
        if roadx < wzx:
            return True
        else:
            return False
    elif wz_direction == "EAST":
        if roady < wzy:
            return True
        else:
            return False
    elif wz_direction == "WEST":
        if roady > wzy:
            return True
        else:
            return False


# significant error!!!!!!!!!!!!!!!!!!!!!!!!!!!


def drawline(i):
    shapetest = shapefile.Reader("./CMU_rcrs_all_events_08-2015_04-2017/shapefile/SplittedLine_WZ" + str(i) + ".shp")
    shapetest_sr = shapetest.shapeRecords()
    # print(len(shapetest_sr))
    plt.figure(1)
    for road in shapetest_sr:
        x_lon = []
        y_lat = []
        for ip in range(len(road.shape.points)):
            # lat1, lon1 =transform(inProj,outProj,shape_ex.points[ip][0],shape_ex.points[ip][1])
            x_lon.append(road.shape.points[ip][0])
            y_lat.append(road.shape.points[ip][1])
        # print(x_lon)
    # plt.plot(x_lon,y_lat)

    case_wz_end_lon, case_wz_end_lat = endkeyuni[i][0][0], endkeyuni[i][0][1]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.plot(case_wz_end_lon,case_wz_end_lat,'*b',label ='Matched End')
    case_wz_start_lon, case_wz_start_lat = startkeyuni[i][0][0], startkeyuni[i][0][1]
    # print(case_wz_start_lat, case_wz_start_lon)
    # plt.plot(case_wz_start_lon,case_wz_start_lat,'*r',label ='Matched Start')
    plt.legend(loc='upper right')
    plt.title('Splitted  of Work Zone-' + str(i) + " on State South")
    plt.savefig("./CMU_rcrs_all_events_08-2015_04-2017/Figures/lineMapStateSouth_" + str(i) + ".png")


def callinelength5(i):
    shapetest = shapefile.Reader("./CMU_rcrs_all_events_08-2015_04-2017/shapefile5/SplittedLine_WZ" + str(i) + ".shp")
    shapetest_sr = shapetest.shapeRecords()
    length = 0
    for road in shapetest_sr:
        for ip in range(len(road.shape.points) - 1):
            lon1, lat1 = road.shape.points[ip][0], road.shape.points[ip][1]
            lon2, lat2 = road.shape.points[ip + 1][0], road.shape.points[ip + 1][1]
            length = length + np.sqrt((lon1 - lon2) ** 2 + (lat1 - lat2) ** 2)
    return length


def callinelength2019(i, loc="./CMU_rcrs_all_events_08-2015_04-2017/shapefile5/SplittedLine_WZ"):
    shapetest = shapefile.Reader(loc + str(i) + ".shp")
    shapetest_sr = shapetest.shapeRecords()
    length = 0
    for road in shapetest_sr:
        for ip in range(len(road.shape.points) - 1):
            lon1, lat1 = road.shape.points[ip][0], road.shape.points[ip][1]
            lon2, lat2 = road.shape.points[ip + 1][0], road.shape.points[ip + 1][1]
            length = length + np.sqrt((lon1 - lon2) ** 2 + (lat1 - lat2) ** 2)
    return length


def direction_match(wzdiri, roaddiri):
    if str(wzdiri)[0:1] == roaddiri:
        return True
    elif (str(wzdiri)[0:1] == 'B') and (roaddiri == 'O'):
        return True
    elif roaddiri == 'B':
        return True
    else:
        return False


def FindSplittedLine5_bi(i, roads, road_shaperecords, endkeyuni, startkeyuni, wz_route, bufferlat, bufferlon,
                         workzone_DIRECTION):
    w = shapefile.Writer()
    w.fields = roads.fields[1:]
    records = []
    pointsparts = []
    k1 = []
    k2 = []
    collection = set()
    smark = 0
    emark = 0
    scountlist = 0
    ecountlist = 0

    for road in road_shaperecords:
        if (road.record[0] == str(wz_route[i]).zfill(4)) and (direction_match(workzone_DIRECTION[i], road.record[10])):
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    scount = distPL(startkeyuni[i][0], vetice) < 10 and distPL(endkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    scountlist = scountlist + scount
            if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    ecount = distPL(endkeyuni[i][0], vetice) < 10 and distPL(startkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    ecountlist = ecountlist + ecount

    for road in road_shaperecords:
        if (road.record[0] == str(wz_route[i]).zfill(4)) and (direction_match(workzone_DIRECTION[i], road.record[10])):
            collection.add(road)
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(startkeyuni[i][0], vetice) < 10 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        smark = smark + 1
                        cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                         road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            spoints.append(k1)
                                            break
                                # print("k1 ori = "+str(k1))

                                collection.remove(road)
                            else:
                                if scountlist < 3:
                                    if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                road.shape.points[len(road.shape.points) - 1][
                                                                    1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        # print("scountlist ==1,k1="+str(k1))
                                        collection.remove(road)
                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j + 1]):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        # print(scountlist,smark)
                                        # print("road_direction,k1="+str(k1))
                                        # print(road.record)
                                        collection.remove(road)

                        else:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                for jm in range(j + 1):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                k1 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            spoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            spoints.insert(0, k1)
                                            break

                                collection.remove(road)

                            else:
                                if scountlist == 1:
                                    if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                road.shape.points[0][1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j + 1):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                        srecord = [road.record]
                                        spoints = []
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                    else:
                        continue


            elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                # print('a')
                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(endkeyuni[i][0], vetice) < 10 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        emark = emark + 1
                        cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                           road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            # print('d')
                            if emark <= 1:
                                erecord = [road.record]
                                epoints = []
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            epoints.append(k2)
                                            break
                                # print("cosup>0emark<=1")
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass
                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - 1][
                                                                      1]]) < distPP(startkeyuni[i][0], k2):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))

                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j + 1]):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass


                        else:
                            # print("e")
                            # print(cosup)
                            # print(j)
                            if emark <= 1:
                                # print(emark)
                                # print("emark<=1")
                                erecord = [road.record]
                                epoints = []
                                for jm in range(j + 1):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                k2 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            epoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            epoints.insert(0, k2)
                                            break
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass

                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                  road.shape.points[0][1]]) < distPP(startkeyuni[i][0],
                                                                                                     k2):
                                        erecord = [road.record]
                                        epoints = []
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break

                                        # print("ecountlist=2")
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                        # print("f")
                                        erecord = [road.record]
                                        epoints = []
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                    else:
                        continue
                        # handle collection, delete the odd/even segnumber that is different from
    # print('k2='+str(k2))
    # print('k1='+str(k1))
    # print("scountlist,ecountlist,smark,emark")
    # print(scountlist,ecountlist,smark,emark)
    records.append(srecord)
    pointsparts.append([spoints])
    try:
        records.append(erecord)
        pointsparts.append([epoints])
    except:
        pass

    itercount = 0
    while (k1 == []) and itercount < 10:
        bufferlat, bufferlon = bufferlat * 5, bufferlon * 5
        records = []
        pointsparts = []
        k1 = []
        k2 = []
        collection = set()
        smark = 0
        emark = 0
        scountlist = 0
        ecountlist = 0

        for road in road_shaperecords:
            if (road.record[0] == str(wz_route[i]).zfill(4)) and (
            direction_match(workzone_DIRECTION[i], road.record[10])):
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        scount = distPL(startkeyuni[i][0], vetice) < 10 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        scountlist = scountlist + scount
                if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        ecount = distPL(endkeyuni[i][0], vetice) < 10 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        ecountlist = ecountlist + ecount

        for road in road_shaperecords:
            if (road.record[0] == str(wz_route[i]).zfill(4)) and (
            direction_match(workzone_DIRECTION[i], road.record[10])):
                collection.add(road)
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(startkeyuni[i][0], vetice) < 10:
                            smark = smark + 1
                            cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                             road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                spoints.append(k1)
                                                break

                                    collection.remove(road)
                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                    road.shape.points[len(road.shape.points) - 1][
                                                                        1]]) < distPP(endkeyuni[i][0], k1):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)
                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)

                            else:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    for jm in range(j + 1):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    k1 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                spoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                spoints.insert(0, k1)
                                                break

                                    collection.remove(road)

                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                    road.shape.points[0][1]]) < distPP(endkeyuni[i][0],
                                                                                                       k1):
                                            srecord = [road.record]
                                            spoints = []
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j + 1):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                            srecord = [road.record]
                                            spoints = []
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                        else:
                            continue


                elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    # print('a')
                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(endkeyuni[i][0], vetice) < 10:
                            emark = emark + 1
                            cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                               road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                # print('d')
                                if emark <= 1:
                                    erecord = [road.record]
                                    epoints = []
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                epoints.append(k2)
                                                break
                                    # print("cosup>0emark<=1")
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass
                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                      road.shape.points[len(road.shape.points) - 1][
                                                                          1]]) < distPP(startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))

                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass


                            else:
                                # print("e")
                                # print(cosup)
                                # print(j)
                                if emark <= 1:
                                    # print(emark)
                                    # print("emark<=1")
                                    erecord = [road.record]
                                    epoints = []
                                    for jm in range(j + 1):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    k2 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                epoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                epoints.insert(0, k2)
                                                break
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass

                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                      road.shape.points[0][1]]) < distPP(
                                            startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break

                                            # print("ecountlist=2")
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                            # print("f")
                                            erecord = [road.record]
                                            epoints = []
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                        else:
                            continue

        itercount = itercount + 1
    # print(itercount)

    # print(k1,k2)
    k1_latlon = k1[1], k1[0]
    try:
        k2_latlon = k2[1], k2[0]
    except:
        k2_latlon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    case_wz_end_lat, case_wz_end_lon = endkeyuni[i][0][1], endkeyuni[i][0][0]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.figure(i)
    # plt.plot(case_wz_end_lon,case_wz_end_lat,'*b',label ='Matched End')
    case_wz_start_lat, case_wz_start_lon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    # print(case_wz_start_lat, case_wz_start_lon)
    # plt.plot(case_wz_start_lon,case_wz_start_lat,'*r',label ='Matched Start')
    # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
    # plt.plot(k2_latlon[1],k2_latlon[0],'og',label ='k2')
    iter_count = 1
    k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2, startkeyuni[i][0]) > 1
    while k12_j and iter_count < 100:
        collection2 = collection.copy()
        for road in collection:
            if distPP(k1_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection2.remove(road)
                # print('l1')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break

        collection3 = collection2.copy()
        for road in collection2:
            if distPP(k2_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection3.remove(road)
                # print('l2')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection4 = collection3.copy()
        for road in collection3:
            if distPP(k1_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection4.remove(road)
                # print('l3')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection5 = collection4.copy()
        for road in collection4:
            if distPP(k2_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection5.remove(road)
                # print('l4')
                break
        iter_count = iter_count + 1
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 5 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 5
        if k12_j == False:
            break
        collection = collection5.copy()
    # print(iter_count)
    # plt.legend(loc='upper right')

    #                elif LineInPointBox(i,startkeyuni,endkeyuni,1e-2,1e-2,road):
    #                    pointsparts.append(road.shape.points)
    #                    records.append(road.record)
    # print(len(pointsparts))
    # print(len(records))
    for idex in range(len(pointsparts)):
        # print(pointsparts[idex])
        # print(records[idex])
        # print(len(records[idex][0]))
        w.line(parts=pointsparts[idex])
        w.record(*records[idex][0])

    w.null()
    w.save('CMU_rcrs_all_events_08-2015_04-2017/shapefile5_bi/SplittedLine_WZ' + str(i))


def FindSplittedLine6_5(i, roads, road_shaperecords, endkeyuni, startkeyuni, wz_route, bufferlat, bufferlon,
                        workzone_DIRECTION):
    w = shapefile.Writer()
    w.fields = roads.fields[1:]
    records = []
    pointsparts = []
    k1 = []
    k2 = []
    collection = set()
    smark = 0
    emark = 0
    scountlist = 0
    ecountlist = 0

    for road in road_shaperecords:
        if road.record[0] == str(wz_route[i]).zfill(4):
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    scount = distPL(startkeyuni[i][0], vetice) < 1 and distPL(endkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    scountlist = scountlist + scount
            if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    ecount = distPL(endkeyuni[i][0], vetice) < 1 and distPL(startkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    ecountlist = ecountlist + ecount

    for road in road_shaperecords:
        if road.record[0] == str(wz_route[i]).zfill(4):
            collection.add(road)
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(startkeyuni[i][0], vetice) < 1 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        smark = smark + 1
                        cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                         road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            spoints.append(k1)
                                            break
                                # print("k1 ori = "+str(k1))

                                collection.remove(road)
                            else:
                                if scountlist < 3:
                                    if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                road.shape.points[len(road.shape.points) - 1][
                                                                    1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        # print("scountlist ==1,k1="+str(k1))
                                        collection.remove(road)
                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j + 1]):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        print(scountlist)
                                        print(smark)
                                        print("road_direction,k1=" + str(k1))
                                        collection.remove(road)

                        else:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                for jm in range(j + 1):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                k1 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            spoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            spoints.insert(0, k1)
                                            break

                                collection.remove(road)

                            else:
                                if scountlist == 1:
                                    if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                road.shape.points[0][1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j + 1):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                        srecord = [road.record]
                                        spoints = []
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                    else:
                        continue


            elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                # print('a')
                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(endkeyuni[i][0], vetice) < 1 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        emark = emark + 1
                        cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                           road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            # print('d')
                            if emark <= 1:
                                erecord = [road.record]
                                epoints = []
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            epoints.append(k2)
                                            break
                                # print("cosup>0emark<=1")
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass
                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - 1][
                                                                      1]]) < distPP(startkeyuni[i][0], k2):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))

                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j + 1]):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass


                        else:
                            # print("e")
                            # print(cosup)
                            # print(j)
                            if emark <= 1:
                                # print(emark)
                                # print("emark<=1")
                                erecord = [road.record]
                                epoints = []
                                for jm in range(j + 1):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                k2 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            epoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            epoints.insert(0, k2)
                                            break
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass

                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                  road.shape.points[0][1]]) < distPP(startkeyuni[i][0],
                                                                                                     k2):
                                        erecord = [road.record]
                                        epoints = []
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break

                                        # print("ecountlist=2")
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                        # print("f")
                                        erecord = [road.record]
                                        epoints = []
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                    else:
                        continue
                        # handle collection, delete the odd/even segnumber that is different from
    # print('k2='+str(k2))
    # print('k1='+str(k1))
    # print("scountlist,ecountlist,smark,emark")
    # print(scountlist,ecountlist,smark,emark)
    records.append(srecord)
    pointsparts.append([spoints])
    try:
        records.append(erecord)
        pointsparts.append([epoints])
    except:
        pass

    itercount = 0
    while (k1 == []) and itercount < 10:
        bufferlat, bufferlon = bufferlat * 5, bufferlon * 5
        records = []
        pointsparts = []
        k1 = []
        k2 = []
        collection = set()
        smark = 0
        emark = 0
        scountlist = 0
        ecountlist = 0

        for road in road_shaperecords:
            if road.record[0] == str(wz_route[i]).zfill(4):
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        scount = distPL(startkeyuni[i][0], vetice) < 1 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        scountlist = scountlist + scount
                if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        ecount = distPL(endkeyuni[i][0], vetice) < 1 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        ecountlist = ecountlist + ecount

        for road in road_shaperecords:
            if road.record[0] == str(wz_route[i]).zfill(4):
                collection.add(road)
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(startkeyuni[i][0], vetice) < 1:
                            smark = smark + 1
                            cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                             road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                spoints.append(k1)
                                                break

                                    collection.remove(road)
                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                    road.shape.points[len(road.shape.points) - 1][
                                                                        1]]) < distPP(endkeyuni[i][0], k1):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)
                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)

                            else:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    for jm in range(j + 1):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    k1 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                spoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                spoints.insert(0, k1)
                                                break

                                    collection.remove(road)

                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                    road.shape.points[0][1]]) < distPP(endkeyuni[i][0],
                                                                                                       k1):
                                            srecord = [road.record]
                                            spoints = []
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j + 1):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                            srecord = [road.record]
                                            spoints = []
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                        else:
                            continue


                elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    # print('a')
                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(endkeyuni[i][0], vetice) < 1:
                            emark = emark + 1
                            cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                               road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                # print('d')
                                if emark <= 1:
                                    erecord = [road.record]
                                    epoints = []
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                epoints.append(k2)
                                                break
                                    # print("cosup>0emark<=1")
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass
                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                      road.shape.points[len(road.shape.points) - 1][
                                                                          1]]) < distPP(startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))

                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass


                            else:
                                # print("e")
                                # print(cosup)
                                # print(j)
                                if emark <= 1:
                                    # print(emark)
                                    # print("emark<=1")
                                    erecord = [road.record]
                                    epoints = []
                                    for jm in range(j + 1):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    k2 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                epoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                epoints.insert(0, k2)
                                                break
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass

                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                      road.shape.points[0][1]]) < distPP(
                                            startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break

                                            # print("ecountlist=2")
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                            # print("f")
                                            erecord = [road.record]
                                            epoints = []
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                        else:
                            continue

        itercount = itercount + 1
    # print(itercount)

    # print(k1,k2)
    k1_latlon = k1[1], k1[0]
    try:
        k2_latlon = k2[1], k2[0]
    except:
        k2_latlon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    case_wz_end_lat, case_wz_end_lon = endkeyuni[i][0][1], endkeyuni[i][0][0]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.figure(i)
    # plt.plot(case_wz_end_lon,case_wz_end_lat,'*b',label ='Matched End')
    case_wz_start_lat, case_wz_start_lon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    # print(case_wz_start_lat, case_wz_start_lon)
    # plt.plot(case_wz_start_lon,case_wz_start_lat,'*r',label ='Matched Start')
    # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
    # plt.plot(k2_latlon[1],k2_latlon[0],'og',label ='k2')
    iter_count = 1
    k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2, startkeyuni[i][0]) > 1
    while k12_j and iter_count < 100:
        collection2 = collection.copy()
        for road in collection:
            if distPP(k1_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection2.remove(road)
                # print('l1')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break

        collection3 = collection2.copy()
        for road in collection2:
            if distPP(k2_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection3.remove(road)
                # print('l2')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection4 = collection3.copy()
        for road in collection3:
            if distPP(k1_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection4.remove(road)
                # print('l3')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection5 = collection4.copy()
        for road in collection4:
            if distPP(k2_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection5.remove(road)
                # print('l4')
                break
        iter_count = iter_count + 1
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 5 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 5
        if k12_j == False:
            break
        collection = collection5.copy()
    # print(iter_count)
    # plt.legend(loc='upper right')

    #                elif LineInPointBox(i,startkeyuni,endkeyuni,1e-2,1e-2,road):
    #                    pointsparts.append(road.shape.points)
    #                    records.append(road.record)
    # print(len(pointsparts))
    # print(len(records))
    for idex in range(len(pointsparts)):
        # print(pointsparts[idex])
        # print(records[idex])
        # print(len(records[idex][0]))
        w.line(parts=pointsparts[idex])
        w.record(*records[idex][0])

    w.null()
    w.save('CMU_rcrs_all_events_08-2015_04-2017/shapefile5/SplittedLine_WZ' + str(i))


def FindSplittedLine7(i, roads, road_shaperecords, endkeyuni, startkeyuni, wz_route, bufferlat, bufferlon,
                      workzone_DIRECTION, fileloc='CMU_rcrs_all_events_08-2015_04-2017/shapefile5/SplittedLine_WZ'):
    w = shapefile.Writer()
    w.fields = roads.fields[1:]
    records = []
    pointsparts = []
    k1 = []
    k2 = []
    collection = set()
    smark = 0
    emark = 0
    scountlist = 0
    ecountlist = 0

    for road in road_shaperecords:
        if road.record[0] == str(wz_route[i]).zfill(4):
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    scount = distPL(startkeyuni[i][0], vetice) < 1 and distPL(endkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    scountlist = scountlist + scount
            if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    ecount = distPL(endkeyuni[i][0], vetice) < 1 and distPL(startkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    ecountlist = ecountlist + ecount

    for road in road_shaperecords:
        if road.record[0] == str(wz_route[i]).zfill(4):
            collection.add(road)
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(startkeyuni[i][0], vetice) < 1 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        smark = smark + 1
                        cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                         road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            spoints.append(k1)
                                            break
                                # print("k1 ori = "+str(k1))

                                collection.remove(road)
                            else:
                                if scountlist < 3:
                                    if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                road.shape.points[len(road.shape.points) - 1][
                                                                    1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        # print("scountlist ==1,k1="+str(k1))
                                        collection.remove(road)
                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j + 1]):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        print(scountlist)
                                        print(smark)
                                        print("road_direction,k1=" + str(k1))
                                        collection.remove(road)

                        else:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                for jm in range(j + 1):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                k1 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            spoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            spoints.insert(0, k1)
                                            break

                                collection.remove(road)

                            else:
                                if scountlist == 1:
                                    if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                road.shape.points[0][1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j + 1):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                        srecord = [road.record]
                                        spoints = []
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                    else:
                        continue


            elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                # print('a')
                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(endkeyuni[i][0], vetice) < 1 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        emark = emark + 1
                        cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                           road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            # print('d')
                            if emark <= 1:
                                erecord = [road.record]
                                epoints = []
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            epoints.append(k2)
                                            break
                                # print("cosup>0emark<=1")
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass
                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - 1][
                                                                      1]]) < distPP(startkeyuni[i][0], k2):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))

                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j + 1]):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass


                        else:
                            # print("e")
                            # print(cosup)
                            # print(j)
                            if emark <= 1:
                                # print(emark)
                                # print("emark<=1")
                                erecord = [road.record]
                                epoints = []
                                for jm in range(j + 1):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                k2 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            epoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            epoints.insert(0, k2)
                                            break
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass

                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                  road.shape.points[0][1]]) < distPP(startkeyuni[i][0],
                                                                                                     k2):
                                        erecord = [road.record]
                                        epoints = []
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break

                                        # print("ecountlist=2")
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                        # print("f")
                                        erecord = [road.record]
                                        epoints = []
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                    else:
                        continue
                        # handle collection, delete the odd/even segnumber that is different from
    # print('k2='+str(k2))
    # print('k1='+str(k1))
    # print("scountlist,ecountlist,smark,emark")
    # print(scountlist,ecountlist,smark,emark)
    records.append(srecord)
    pointsparts.append([spoints])
    try:
        records.append(erecord)
        pointsparts.append([epoints])
    except:
        pass

    itercount = 0
    while (k1 == []) and itercount < 10:
        bufferlat, bufferlon = bufferlat * 5, bufferlon * 5
        records = []
        pointsparts = []
        k1 = []
        k2 = []
        collection = set()
        smark = 0
        emark = 0
        scountlist = 0
        ecountlist = 0

        for road in road_shaperecords:
            if road.record[0] == str(wz_route[i]).zfill(4):
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        scount = distPL(startkeyuni[i][0], vetice) < 1 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        scountlist = scountlist + scount
                if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        ecount = distPL(endkeyuni[i][0], vetice) < 1 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        ecountlist = ecountlist + ecount

        for road in road_shaperecords:
            if road.record[0] == str(wz_route[i]).zfill(4):
                collection.add(road)
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(startkeyuni[i][0], vetice) < 1:
                            smark = smark + 1
                            cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                             road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                spoints.append(k1)
                                                break

                                    collection.remove(road)
                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                    road.shape.points[len(road.shape.points) - 1][
                                                                        1]]) < distPP(endkeyuni[i][0], k1):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)
                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)

                            else:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    for jm in range(j + 1):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    k1 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                spoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                spoints.insert(0, k1)
                                                break

                                    collection.remove(road)

                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                    road.shape.points[0][1]]) < distPP(endkeyuni[i][0],
                                                                                                       k1):
                                            srecord = [road.record]
                                            spoints = []
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j + 1):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                            srecord = [road.record]
                                            spoints = []
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                        else:
                            continue


                elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    # print('a')
                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(endkeyuni[i][0], vetice) < 1:
                            emark = emark + 1
                            cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                               road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                # print('d')
                                if emark <= 1:
                                    erecord = [road.record]
                                    epoints = []
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                epoints.append(k2)
                                                break
                                    # print("cosup>0emark<=1")
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass
                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                      road.shape.points[len(road.shape.points) - 1][
                                                                          1]]) < distPP(startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))

                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass


                            else:
                                # print("e")
                                # print(cosup)
                                # print(j)
                                if emark <= 1:
                                    # print(emark)
                                    # print("emark<=1")
                                    erecord = [road.record]
                                    epoints = []
                                    for jm in range(j + 1):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    k2 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                epoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                epoints.insert(0, k2)
                                                break
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass

                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                      road.shape.points[0][1]]) < distPP(
                                            startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break

                                            # print("ecountlist=2")
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                            # print("f")
                                            erecord = [road.record]
                                            epoints = []
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                        else:
                            continue

        itercount = itercount + 1
    # print(itercount)

    # print(k1,k2)
    k1_latlon = k1[1], k1[0]
    try:
        k2_latlon = k2[1], k2[0]
    except:
        k2_latlon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    case_wz_end_lat, case_wz_end_lon = endkeyuni[i][0][1], endkeyuni[i][0][0]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.figure(i)
    # plt.plot(case_wz_end_lon,case_wz_end_lat,'*b',label ='Matched End')
    case_wz_start_lat, case_wz_start_lon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    # print(case_wz_start_lat, case_wz_start_lon)
    # plt.plot(case_wz_start_lon,case_wz_start_lat,'*r',label ='Matched Start')
    # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
    # plt.plot(k2_latlon[1],k2_latlon[0],'og',label ='k2')
    iter_count = 1
    k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2, startkeyuni[i][0]) > 1
    while k12_j and iter_count < 100:
        collection2 = collection.copy()
        for road in collection:
            if distPP(k1_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection2.remove(road)
                # print('l1')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break

        collection3 = collection2.copy()
        for road in collection2:
            if distPP(k2_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection3.remove(road)
                # print('l2')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection4 = collection3.copy()
        for road in collection3:
            if distPP(k1_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection4.remove(road)
                # print('l3')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection5 = collection4.copy()
        for road in collection4:
            if distPP(k2_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection5.remove(road)
                # print('l4')
                break
        iter_count = iter_count + 1
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 5 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 5
        if k12_j == False:
            break
        collection = collection5.copy()
    # print(iter_count)
    # plt.legend(loc='upper right')

    #                elif LineInPointBox(i,startkeyuni,endkeyuni,1e-2,1e-2,road):
    #                    pointsparts.append(road.shape.points)
    #                    records.append(road.record)
    # print(len(pointsparts))
    # print(len(records))
    for idex in range(len(pointsparts)):
        # print(pointsparts[idex])
        # print(records[idex])
        # print(len(records[idex][0]))
        w.line(parts=pointsparts[idex])
        # w.line( pointsparts[idex])
        w.record(*records[idex][0])

    w.null()
    w.save(fileloc + str(i))


# bi
def FindSplittedLine7_bi(i, roads, road_shaperecords, endkeyuni, startkeyuni, wz_route, bufferlat, bufferlon,
                         workzone_DIRECTION, fileloc):
    w = shapefile.Writer()
    w.fields = roads.fields[1:]
    records = []
    pointsparts = []
    k1 = []
    k2 = []
    collection = set()
    smark = 0
    emark = 0
    scountlist = 0
    ecountlist = 0

    for road in road_shaperecords:
        if (road.record[0] == str(wz_route[i]).zfill(4)) and (direction_match(workzone_DIRECTION[i], road.record[10])):
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    scount = distPL(startkeyuni[i][0], vetice) < 10 and distPL(endkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    scountlist = scountlist + scount
            if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                for j in range(len(road.shape.points) - 1):
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    ecount = distPL(endkeyuni[i][0], vetice) < 10 and distPL(startkeyuni[i][0], vetice) < distPP(
                        endkeyuni[i][0], startkeyuni[i][0])
                    ecountlist = ecountlist + ecount

    for road in road_shaperecords:
        if (road.record[0] == str(wz_route[i]).zfill(4)) and (direction_match(workzone_DIRECTION[i], road.record[10])):
            collection.add(road)
            if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(startkeyuni[i][0], vetice) < 10 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        smark = smark + 1
                        cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                         road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            spoints.append(k1)
                                            break
                                # print("k1 ori = "+str(k1))

                                collection.remove(road)
                            else:
                                if scountlist < 3:
                                    if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                road.shape.points[len(road.shape.points) - 1][
                                                                    1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        # print("scountlist ==1,k1="+str(k1))
                                        collection.remove(road)
                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j + 1]):
                                        srecord = [road.record]
                                        spoints = []
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    spoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    spoints.append(k1)
                                                    break
                                        # print(scountlist,smark)
                                        # print("road_direction,k1="+str(k1))
                                        # print(road.record)
                                        collection.remove(road)

                        else:
                            if smark <= 1:
                                srecord = [road.record]
                                spoints = []
                                for jm in range(j + 1):
                                    spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                k1 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                if cosk1 < 0:
                                    k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            spoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            spoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            spoints.insert(0, k1)
                                            break

                                collection.remove(road)

                            else:
                                if scountlist == 1:
                                    if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                road.shape.points[0][1]]) < distPP(endkeyuni[i][0], k1):
                                        srecord = [road.record]
                                        spoints = []
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j + 1):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                                else:
                                    if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                        srecord = [road.record]
                                        spoints = []
                                        k1 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j):
                                            spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0],
                                                                                                    k1)
                                        if cosk1 < 0:
                                            k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    spoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    spoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    spoints.insert(0, k1)
                                                    break
                                        collection.remove(road)

                    else:
                        continue


            elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                # print('a')
                for j in range(len(road.shape.points) - 1):
                    subpart = []
                    vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                              [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                    if distPL(endkeyuni[i][0], vetice) < 10 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0]):
                        emark = emark + 1
                        cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                           road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                            road.shape.points[j + 1][0], \
                            road.shape.points[j + 1][1]])
                        if cosup > 0:
                            # print('d')
                            if emark <= 1:
                                erecord = [road.record]
                                epoints = []
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                for jm in range(j + 1, len(road.shape.points)):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                       road.shape.points[len(road.shape.points) - 1][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(len(road.shape.points) - j - 2):
                                        vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                      road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                     [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                      road.shape.points[len(road.shape.points) - js - 2][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                        else:
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                            road.shape.points[len(road.shape.points) - js - 1][1]))
                                            epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                            road.shape.points[len(road.shape.points) - js - 2][1]))
                                            epoints.append(k2)
                                            break
                                # print("cosup>0emark<=1")
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass
                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - 1][
                                                                      1]]) < distPP(startkeyuni[i][0], k2):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))

                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j + 1]):
                                        erecord = [road.record]
                                        epoints = []
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for jm in range(j + 1, len(road.shape.points)):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                               road.shape.points[len(road.shape.points) - 1][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(len(road.shape.points) - j - 2):
                                                vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                              road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                             [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                              road.shape.points[len(road.shape.points) - js - 2][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                else:
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                         road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    epoints.remove(
                                                        (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                         road.shape.points[len(road.shape.points) - js - 2][1]))
                                                    epoints.append(k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass


                        else:
                            # print("e")
                            # print(cosup)
                            # print(j)
                            if emark <= 1:
                                # print(emark)
                                # print("emark<=1")
                                erecord = [road.record]
                                epoints = []
                                for jm in range(j + 1):
                                    epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                k2 = ((road.shape.points[0][0], \
                                       road.shape.points[0][1]))
                                cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                if cosk2 < 0:
                                    k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for js in range(j):
                                        vetice_mm = [[road.shape.points[js][0], \
                                                      road.shape.points[js][1]], \
                                                     [road.shape.points[js + 1][0], \
                                                      road.shape.points[js + 1][1]]]
                                        if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                        else:
                                            epoints.remove((road.shape.points[js][0], \
                                                            road.shape.points[js][1]))
                                            epoints.remove((road.shape.points[js + 1][0], \
                                                            road.shape.points[js + 1][1]))
                                            epoints.insert(0, k2)
                                            break
                                # print(k2)
                                try:
                                    collection.remove(road)
                                except:
                                    pass

                            else:
                                if ecountlist == 1:
                                    if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                  road.shape.points[0][1]]) < distPP(startkeyuni[i][0],
                                                                                                     k2):
                                        erecord = [road.record]
                                        epoints = []
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break

                                        # print("ecountlist=2")
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                                else:
                                    if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                        # print("f")
                                        erecord = [road.record]
                                        epoints = []
                                        for jm in range(j + 1):
                                            epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                        epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        k2 = ((road.shape.points[0][0], \
                                               road.shape.points[0][1]))
                                        cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                        if cosk2 < 0:
                                            k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for js in range(j):
                                                vetice_mm = [[road.shape.points[js][0], \
                                                              road.shape.points[js][1]], \
                                                             [road.shape.points[js + 1][0], \
                                                              road.shape.points[js + 1][1]]]
                                                if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                else:
                                                    epoints.remove((road.shape.points[js][0], \
                                                                    road.shape.points[js][1]))
                                                    epoints.remove((road.shape.points[js + 1][0], \
                                                                    road.shape.points[js + 1][1]))
                                                    epoints.insert(0, k2)
                                                    break
                                        # print(k2)
                                        try:
                                            collection.remove(road)
                                        except:
                                            pass
                    else:
                        continue
                        # handle collection, delete the odd/even segnumber that is different from
    # print('k2='+str(k2))
    # print('k1='+str(k1))
    # print("scountlist,ecountlist,smark,emark")
    # print(scountlist,ecountlist,smark,emark)
    records.append(srecord)
    pointsparts.append([spoints])
    try:
        records.append(erecord)
        pointsparts.append([epoints])
    except:
        pass

    itercount = 0
    while (k1 == []) and itercount < 10:
        bufferlat, bufferlon = bufferlat * 5, bufferlon * 5
        records = []
        pointsparts = []
        k1 = []
        k2 = []
        collection = set()
        smark = 0
        emark = 0
        scountlist = 0
        ecountlist = 0

        for road in road_shaperecords:
            if (road.record[0] == str(wz_route[i]).zfill(4)) and (
            direction_match(workzone_DIRECTION[i], road.record[10])):
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        scount = distPL(startkeyuni[i][0], vetice) < 10 and distPL(endkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        scountlist = scountlist + scount
                if PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    for j in range(len(road.shape.points) - 1):
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        ecount = distPL(endkeyuni[i][0], vetice) < 10 and distPL(startkeyuni[i][0], vetice) < distPP(
                            endkeyuni[i][0], startkeyuni[i][0])
                        ecountlist = ecountlist + ecount

        for road in road_shaperecords:
            if (road.record[0] == str(wz_route[i]).zfill(4)) and (
            direction_match(workzone_DIRECTION[i], road.record[10])):
                collection.add(road)
                if PointInLineBox(i, startkeyuni, bufferlat, bufferlon, road.shape.bbox):

                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(startkeyuni[i][0], vetice) < 10:
                            smark = smark + 1
                            cosup = distPP(endkeyuni[i][0], [road.shape.points[j][0], \
                                                             road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                spoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                spoints.append(k1)
                                                break

                                    collection.remove(road)
                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                    road.shape.points[len(road.shape.points) - 1][
                                                                        1]]) < distPP(endkeyuni[i][0], k1):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)
                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            srecord = [road.record]
                                            spoints = []
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k1 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        spoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        spoints.append(k1)
                                                        break
                                            collection.remove(road)

                            else:
                                if smark <= 1:
                                    srecord = [road.record]
                                    spoints = []
                                    for jm in range(j + 1):
                                        spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                    k1 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(startkeyuni[i][0], k1)
                                    if cosk1 < 0:
                                        k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                spoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                spoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                spoints.insert(0, k1)
                                                break

                                    collection.remove(road)

                                else:
                                    if scountlist == 1:
                                        if distPP(endkeyuni[i][0], [road.shape.points[0][0], \
                                                                    road.shape.points[0][1]]) < distPP(endkeyuni[i][0],
                                                                                                       k1):
                                            srecord = [road.record]
                                            spoints = []
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j + 1):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                                    else:
                                        if road_direction(workzone_DIRECTION[i], startkeyuni[i], road.shape.points[j]):
                                            srecord = [road.record]
                                            spoints = []
                                            k1 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j):
                                                spoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            spoints.append((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                            cosk1 = distPP(startkeyuni[i][0], endkeyuni[i][0]) - distPP(
                                                startkeyuni[i][0], k1)
                                            if cosk1 < 0:
                                                k1 = ((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(endkeyuni[i][0], vetice_mm) > 1:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        spoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        spoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        spoints.insert(0, k1)
                                                        break
                                            collection.remove(road)

                        else:
                            continue


                elif PointInLineBox(i, endkeyuni, bufferlat, bufferlon, road.shape.bbox):
                    # print('a')
                    for j in range(len(road.shape.points) - 1):
                        subpart = []
                        vetice = [[road.shape.points[j][0], road.shape.points[j][1]],
                                  [road.shape.points[j + 1][0], road.shape.points[j + 1][1]]]
                        if distPL(endkeyuni[i][0], vetice) < 10:
                            emark = emark + 1
                            cosup = distPP(startkeyuni[i][0], [road.shape.points[j][0], \
                                                               road.shape.points[j][1]]) - distPP(startkeyuni[i][0], [
                                road.shape.points[j + 1][0], \
                                road.shape.points[j + 1][1]])
                            if cosup > 0:
                                # print('d')
                                if emark <= 1:
                                    erecord = [road.record]
                                    epoints = []
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    for jm in range(j + 1, len(road.shape.points)):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                           road.shape.points[len(road.shape.points) - 1][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(len(road.shape.points) - j - 2):
                                            vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                          road.shape.points[len(road.shape.points) - js - 1][1]], \
                                                         [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                          road.shape.points[len(road.shape.points) - js - 2][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                            else:
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                road.shape.points[len(road.shape.points) - js - 1][1]))
                                                epoints.remove((road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                road.shape.points[len(road.shape.points) - js - 2][1]))
                                                epoints.append(k2)
                                                break
                                    # print("cosup>0emark<=1")
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass
                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[len(road.shape.points) - 1][0], \
                                                                      road.shape.points[len(road.shape.points) - 1][
                                                                          1]]) < distPP(startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))

                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i],
                                                          road.shape.points[j + 1]):
                                            erecord = [road.record]
                                            epoints = []
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            for jm in range(j + 1, len(road.shape.points)):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            k2 = ((road.shape.points[len(road.shape.points) - 1][0], \
                                                   road.shape.points[len(road.shape.points) - 1][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(len(road.shape.points) - j - 2):
                                                    vetice_mm = [[road.shape.points[len(road.shape.points) - js - 1][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 1][
                                                                      1]], \
                                                                 [road.shape.points[len(road.shape.points) - js - 2][0], \
                                                                  road.shape.points[len(road.shape.points) - js - 2][
                                                                      1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                    else:
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 1][0], \
                                                             road.shape.points[len(road.shape.points) - js - 1][1]))
                                                        epoints.remove(
                                                            (road.shape.points[len(road.shape.points) - js - 2][0], \
                                                             road.shape.points[len(road.shape.points) - js - 2][1]))
                                                        epoints.append(k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass


                            else:
                                # print("e")
                                # print(cosup)
                                # print(j)
                                if emark <= 1:
                                    # print(emark)
                                    # print("emark<=1")
                                    erecord = [road.record]
                                    epoints = []
                                    for jm in range(j + 1):
                                        epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                    epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                    k2 = ((road.shape.points[0][0], \
                                           road.shape.points[0][1]))
                                    cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0], k2)
                                    if cosk2 < 0:
                                        k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                        for js in range(j):
                                            vetice_mm = [[road.shape.points[js][0], \
                                                          road.shape.points[js][1]], \
                                                         [road.shape.points[js + 1][0], \
                                                          road.shape.points[js + 1][1]]]
                                            if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                            else:
                                                epoints.remove((road.shape.points[js][0], \
                                                                road.shape.points[js][1]))
                                                epoints.remove((road.shape.points[js + 1][0], \
                                                                road.shape.points[js + 1][1]))
                                                epoints.insert(0, k2)
                                                break
                                    # print(k2)
                                    try:
                                        collection.remove(road)
                                    except:
                                        pass

                                else:
                                    if ecountlist == 1:
                                        if distPP(startkeyuni[i][0], [road.shape.points[0][0], \
                                                                      road.shape.points[0][1]]) < distPP(
                                            startkeyuni[i][0], k2):
                                            erecord = [road.record]
                                            epoints = []
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break

                                            # print("ecountlist=2")
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                                    else:
                                        if road_direction(workzone_DIRECTION[i], endkeyuni[i], road.shape.points[j]):
                                            # print("f")
                                            erecord = [road.record]
                                            epoints = []
                                            for jm in range(j + 1):
                                                epoints.append((road.shape.points[jm][0], road.shape.points[jm][1]))
                                            epoints.append((endkeyuni[i][0][0], endkeyuni[i][0][1]))
                                            k2 = ((road.shape.points[0][0], \
                                                   road.shape.points[0][1]))
                                            cosk2 = distPP(endkeyuni[i][0], startkeyuni[i][0]) - distPP(endkeyuni[i][0],
                                                                                                        k2)
                                            if cosk2 < 0:
                                                k2 = ((startkeyuni[i][0][0], startkeyuni[i][0][1]))
                                                for js in range(j):
                                                    vetice_mm = [[road.shape.points[js][0], \
                                                                  road.shape.points[js][1]], \
                                                                 [road.shape.points[js + 1][0], \
                                                                  road.shape.points[js + 1][1]]]
                                                    if distPL(startkeyuni[i][0], vetice_mm) > 1:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                    else:
                                                        epoints.remove((road.shape.points[js][0], \
                                                                        road.shape.points[js][1]))
                                                        epoints.remove((road.shape.points[js + 1][0], \
                                                                        road.shape.points[js + 1][1]))
                                                        epoints.insert(0, k2)
                                                        break
                                            # print(k2)
                                            try:
                                                collection.remove(road)
                                            except:
                                                pass
                        else:
                            continue

        itercount = itercount + 1
    # print(itercount)

    # print(k1,k2)
    k1_latlon = k1[1], k1[0]
    try:
        k2_latlon = k2[1], k2[0]
    except:
        k2_latlon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    case_wz_end_lat, case_wz_end_lon = endkeyuni[i][0][1], endkeyuni[i][0][0]
    # print(case_wz_end_lat, case_wz_end_lon)
    # plt.figure(i)
    # plt.plot(case_wz_end_lon,case_wz_end_lat,'*b',label ='Matched End')
    case_wz_start_lat, case_wz_start_lon = startkeyuni[i][0][1], startkeyuni[i][0][0]
    # print(case_wz_start_lat, case_wz_start_lon)
    # plt.plot(case_wz_start_lon,case_wz_start_lat,'*r',label ='Matched Start')
    # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
    # plt.plot(k2_latlon[1],k2_latlon[0],'og',label ='k2')
    iter_count = 1
    k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2, startkeyuni[i][0]) > 1
    while k12_j and iter_count < 100:
        collection2 = collection.copy()
        for road in collection:
            if distPP(k1_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection2.remove(road)
                # print('l1')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break

        collection3 = collection2.copy()
        for road in collection2:
            if distPP(k2_latlon, [road.shape.points[0][1], road.shape.points[0][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[len(road.shape.points) - 1][1], \
                            road.shape.points[len(road.shape.points) - 1][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection3.remove(road)
                # print('l2')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection4 = collection3.copy()
        for road in collection3:
            if distPP(k1_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k1_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k1_latlon[1],k1_latlon[0],'ob',label ='k1')
                collection4.remove(road)
                # print('l3')
                break
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 1 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 1
        if k12_j == False:
            break
        collection5 = collection4.copy()
        for road in collection4:
            if distPP(k2_latlon, [road.shape.points[len(road.shape.points) - 1][1],
                                  road.shape.points[len(road.shape.points) - 1][0]]) < 1:
                records.append([road.record])
                pointsparts.append([road.shape.points])
                k2_latlon = road.shape.points[0][1], road.shape.points[0][0]
                # plt.plot(k2_latlon[1],k2_latlon[0],'or',label ='k2')
                collection5.remove(road)
                # print('l4')
                break
        iter_count = iter_count + 1
        k1 = k1_latlon[1], k1_latlon[0]
        k2 = k2_latlon[1], k2_latlon[0]
        # print("k1="+str(k1)+", k2="+str(k2))
        k12_j = distPP(k1_latlon, k2_latlon) > 5 and distPP(k1, endkeyuni[i][0]) > 5 and distPP(k2,
                                                                                                startkeyuni[i][0]) > 5
        if k12_j == False:
            break
        collection = collection5.copy()
    # print(iter_count)
    # plt.legend(loc='upper right')

    #                elif LineInPointBox(i,startkeyuni,endkeyuni,1e-2,1e-2,road):
    #                    pointsparts.append(road.shape.points)
    #                    records.append(road.record)
    # print(len(pointsparts))
    # print(len(records))
    for idex in range(len(pointsparts)):
        # print(pointsparts[idex])
        # print(records[idex])
        # print(len(records[idex][0]))
        w.line(parts=pointsparts[idex])
        w.record(*records[idex][0])

    w.null()
    w.save(fileloc + str(i))
