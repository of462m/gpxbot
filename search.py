import math
import os
from io import StringIO
import geopy.distance
import gpxpy
from gpxpy.gpx import GPX, GPXBounds
import time
from math import sin, cos, acos
import hashlib
from index import md5_checksum
from scache import index_gpx


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


def get_sqr_region(pt: tuple, side_size: int):
    d_lat = geopy.distance.geodesic(pt, (pt[0] + 0.01, pt[1])).m
    d_lon = geopy.distance.geodesic(pt, (pt[0], pt[1] + 0.1)).m
    # print(f"{d_lat}m {d_lon}m")
    # 0.1 нужно динамически поднастроить исходя из масштаба
    delta_lat = 0.01 * (side_size / 2.0) / d_lat
    delta_lon = 0.1 * (side_size / 2.0) / d_lon
    return (round(pt[0] + delta_lat, 6), round(pt[1] - delta_lon, 6)), (
        round(pt[0] - delta_lat, 6), round(pt[1] + delta_lon, 6))


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


def get_max(a: float, b: float) -> float:
    return a if a > b else b


def get_min(a: float, b: float) -> float:
    return a if a < b else b


class RegBounds:
    __slots__ = ('min_lat', 'min_lon', 'max_lat', 'max_lon',)

    def __init__(self):
        self.min_lat, self.max_lat = 90.0, -90.0
        self.min_lon, self.max_lon = 180.0, -180.0

    def recalc(self, lat: float, lon: float):
        self.min_lat = get_min(self.min_lat, lat)
        self.min_lon = get_min(self.min_lon, lon)
        self.max_lat = get_max(self.max_lat, lat)
        self.max_lon = get_max(self.max_lon, lon)

    def __repr__(self):
        return f"MIN: {self.min_lat} {self.min_lon} MAX: {self.max_lat} {self.max_lon}"


def add_gpx_to_data(gpx: GPX, fid: str) -> None:
    bounds = RegBounds()
    orbounds = gpx.get_bounds()
    if orbounds:
        print(f"MIN: {orbounds.min_latitude} {orbounds.min_longitude} MAX: {orbounds.max_latitude} {orbounds.max_longitude}")
    gpx_data_dir = 'index00/data/'
    linesnum = 0
    for track in gpx.tracks:
        for trkseg in track.segments:
            linesnum = len(trkseg.points)
    linesnum += len(gpx.waypoints)
    for route in gpx.routes:
        linesnum += len(route.points)

    with open(f"{gpx_data_dir}{fid}.dat", "w", encoding='utf-8') as fdat:
        # with open(f"{gpx_data_dir}{fid}.dat", "w", encoding='utf-8') as fdat:
        fdat.write(f"{linesnum}\n")
        for track in gpx.tracks:
            for trkseg in track.segments:
                for trkpoint in trkseg.points:
                    fdat.write(f"{trkpoint.latitude} {trkpoint.longitude}\n")
                    bounds.recalc(trkpoint.latitude, trkpoint.longitude)
        for route in gpx.routes:
            for rtept in route.points:
                fdat.write(f"{rtept.latitude} {rtept.longitude}\n")
                bounds.recalc(rtept.latitude, rtept.longitude)
        for wpt in gpx.waypoints:
            fdat.write(f"{wpt.latitude} {wpt.longitude}\n")
            bounds.recalc(wpt.latitude, wpt.longitude)
        fdat.write(f"{bounds}")


if __name__ == '__main__':

    # start_time = time.time()
    pic_dir = 'angara-tmp-00'

    # сюда добавить описательные поля (list), которое будет выдаваться в описании выдачи
    # пик Галина, бухта Ая, итд - p-tokens, кароч! stag уходит в небытие.
    # перевести алгоритм построения индекса в Си
    points = [
        # {'stag': "галин", 'coords': (51.94419, 102.37698), 'size': 100},
        # {'stag': "люб", 'coords': (51.94541, 102.43996), 'size': 100},
        # {'stag': "дружб", 'coords': (51.95099, 102.45566), 'size': 100},
        # {'stag': "мунк", 'coords': (51.71883, 100.59706), 'size': 100},
        # {'stag': "нухэн", 'coords': (51.78165 100.68972), 'size': 100},
        # {'stag': "хулугайш", 'coords': (51.74442, 100.98550), 'size': 100},
        # {'stag': "сибизмир", 'coords': (51.75060, 100.92989), 'size': 100},
        # {'stag': "витяз", 'coords': (51.97477, 104.10470), 'size': 200},
        # {'stag': "идол", 'coords': (51.95990, 104.08796), 'size': 200},
        # {'stag': "черепах", 'coords': (51.95648, 104.08997), 'size': 200},
        # {'stag': "зеркал", 'coords': (51.97020, 104.13447), 'size': 200},
        # {'stag': "verblud", 'coords': (51.97502, 104.14206), 'size': 200},
        # {'stag': "starkrep", 'coords': (51.99310, 104.14044), 'size': 200},
        # {'stag': "sk-obzor", 'coords': (51.94495, 103.91873), 'size': 200},
        # {'stag': "ворон", 'coords': (51.94314, 103.93111), 'size': 200},
        # {'stag': "шахтай", 'coords': (51.94209, 103.95802), 'size': 200},
        # {'stag': "химер", 'coords': (52.12894, 103.59098), 'size': 300},
        # {'stag': "старух", 'coords': (51.94667, 104.13498), 'size': 200},
        # {'stag': "медвежат", 'coords': (51.96172, 104.14123), 'size': 200},
        # {'stag': "улябор", 'coords': (51.92763, 102.64003), 'size': 100},
        # {'stag': "серебрян", 'coords': (51.91614, 102.61360), 'size': 300},
        # {'stag': "катьк", 'coords': (51.75186, 100.60565), 'size': 100},
        # {'stag': "архе", 'coords': (52.00675, 105.31717), 'size': 100},
        # {'stag': "охотнич", 'coords': (52.13878, 105.46341), 'size': 100},
        # {'stag': "энергетик", 'coords': (51.95326, 102.50881), 'size': 100},
        # {'stag': "новокшен", 'coords': (51.94430, 102.50823), 'size': 100},
        # {'stag': "доктор", 'coords': (51.95279, 102.53312), 'size': 100},
        # {'stag': "портер", 'coords': (51.96374, 102.52549), 'size': 100},
        # {'stag': "броненос", 'coords': (51.95626, 102.47578), 'size': 100},
        # {'stag': "трехглав", 'coords': (51.96388, 102.36955), 'size': 100},
        # {'stag': "соан", 'coords': (51.96421, 102.23718), 'size': 100},
        # {'stag': "царьводопад", 'coords': (51.95621, 102.36019), 'size': 300},
        # {'stag': "мамай???", 'coords': (51.38219, 104.85779), 'size': 100},
        # {'stag': "порожист", 'coords': (51.43389, 104.03761), 'size': 100},
        # {'stag': "черск", 'coords': (51.51563, 103.62597), 'size': 100},
        # {'stag': "тальцинск", 'coords': (51.35050, 104.58954), 'size': 100},
        # {'stag': "босан", 'coords': (51.44329, 103.37566), 'size': 100},
        # {'stag': "сердце", 'coords': (51.50997, 103.62532), 'size': 300},
        # {'stag': "парус", 'coords': (51.73974, 103.85860), 'size': 500},
        # {'stag': "козий", 'coords': (52.44374, 103.13353), 'size': 500},
    ]

    dcalc_time = 0
    parse_time = 0

    for pname in os.listdir(pic_dir):
        fname = f'{pic_dir}/{pname}'
        with open(fname, 'r', encoding='utf-8') as fgpx:
            gpx = gpxpy.parse(fgpx)
        add_gpx_to_data(gpx, md5_checksum(fname))
