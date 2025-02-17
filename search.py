import math
import os
import geopy.distance
import gpxpy
from gpxpy.gpx import GPX
import time
from math import sin, cos, acos
from index import md5_checksum, GPXIndex


def get_curve_delta(pt: tuple, delta: float = 0.1):
    llat = geopy.distance.geodesic(pt, (pt[0] + delta, pt[1])).m
    llon = geopy.distance.geodesic(pt, (pt[0], pt[1] + delta)).m
    return delta * llat / llon


def get_distance(pt_1: tuple, pt_2: tuple):
    start_time = time.time()
    d = geopy.distance.geodesic(pt_1, pt_2).m
    return d, time.time() - start_time


def deg2rad(phi: float):
    return math.pi * phi / 180


def get_distance_simple(pt_1: tuple, pt_2: tuple):
    start_time = time.time()
    rpt_1 = (deg2rad(pt_1[0]), deg2rad(pt_1[1]))
    rpt_2 = (deg2rad(pt_2[0]), deg2rad(pt_2[1]))

    acos_arg = sin(rpt_1[0]) * sin(rpt_2[0]) + cos(rpt_1[0]) * cos(rpt_2[0]) * cos(rpt_1[1] - rpt_2[1])
    d = 1000 * acos(acos_arg) * 6371
    return d, time.time() - start_time


def sqr_region_2gpx(path: str, sqr_region: tuple):
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Create points:
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(sqr_region[0][0], sqr_region[0][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(sqr_region[0][0], sqr_region[1][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(sqr_region[1][0], sqr_region[1][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(sqr_region[1][0], sqr_region[0][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(sqr_region[0][0], sqr_region[0][1]))
    with open(path, 'w', encoding='utf-8') as gpx_to_file:
        gpx_to_file.write(gpx.to_xml())


def is_in_sqr_region(region: tuple, pt: tuple):
    # region - ( (лев.верх), (прав.нижн.) )
    start_time = time.time()
    if pt[0] > region[1][0]:
        if pt[0] < region[0][0]:
            if pt[1] > region[0][1]:
                if pt[1] < region[1][1]:
                    return True, time.time() - start_time
    return False, time.time() - start_time


def init_new_gpx(gpx: GPX):
    gpx.creator = 'GPXBaikal telebot v. 0.1D'
    gpx.author_name = 'Taras I. Madzhara'
    gpx.author_email = 'marf51@mail.ru'


def add_sqr_trk_2gpx(gpx: GPX, ptLAT: tuple, ptLON: tuple, tname: str):
    trk = gpxpy.gpx.GPXTrack(name=tname)
    gpx.tracks.append(trk)
    trkseg = gpxpy.gpx.GPXTrackSegment()
    trk.segments.append(trkseg)
    trkseg.points.append(gpxpy.gpx.GPXTrackPoint(latitude=ptLAT[0], longitude=ptLON[0]))
    trkseg.points.append(gpxpy.gpx.GPXTrackPoint(latitude=ptLAT[0], longitude=ptLON[1]))
    trkseg.points.append(gpxpy.gpx.GPXTrackPoint(latitude=ptLAT[1], longitude=ptLON[1]))
    trkseg.points.append(gpxpy.gpx.GPXTrackPoint(latitude=ptLAT[1], longitude=ptLON[0]))
    trkseg.points.append(gpxpy.gpx.GPXTrackPoint(latitude=ptLAT[0], longitude=ptLON[0]))


def get_tracks_by_coords():
    # можно выдать рой треков в одном gpx и архив с отдельными треками
    pass





if __name__ == '__main__':

    # start_time = time.time()
    pic_dir = 'angara-w'



    dcalc_time = 0
    parse_time = 0

    gpx = gpxpy.gpx.GPX()
    gpx.name = "points"
    for point in points:
        gpx_wpt = gpxpy.gpx.GPXWaypoint(longitude=float(point['coords'][1]),
                                        latitude=float(point['coords'][0]),
                                        name=f"{point['size']} {point['stag']}")
        gpx.waypoints.append(gpx_wpt)
        with open("enisey/points.gpx", 'w', encoding='utf-8') as gpx_to_file:
            gpx_to_file.write(gpx.to_xml())
    exit(0)
    start_time = time.time()
    parse_time = 0
    index = GPXIndex('index00')
    for pname in os.listdir(pic_dir):
        fname = f'{pic_dir}/{pname}'
        print(fname)
        with open(fname, 'r', encoding='utf-8') as fgpx:
            start_parse_time = time.time()
            gpx = gpxpy.parse(fgpx)
            parse_time += time.time() - start_parse_time
        index.add_gpx_to_data(gpx, md5_checksum(fname))
    total_elapsed_time = time.time() - start_time
    print(f"Total: {total_elapsed_time} Parse: {parse_time} ({round(100*parse_time/total_elapsed_time,2)}%)")
