import os
import geopy.distance
import gpxpy
from gpxpy.gpx import GPX
import time
from scache import index_gpx

def get_distance(pt_1: tuple, pt_2: tuple):
    start_time = time.time()
    d = geopy.distance.geodesic(pt_1, pt_2).m
    return d, time.time() - start_time

def get_sqr_region(pt: tuple, side_size: int):
    d_lat = geopy.distance.geodesic(pt,(pt[0]+0.01, pt[1])).m
    d_lon = geopy.distance.geodesic(pt,(pt[0], pt[1]+0.1)).m
    # print(f"{d_lat}m {d_lon}m")
    # 0.1 нужно динамически поднастроить исходя из масштаба
    delta_lat = 0.01*(side_size/2.0)/d_lat
    delta_lon = 0.1*(side_size/2.0)/d_lon
    return (round(pt[0]+delta_lat,6), round(pt[1]-delta_lon,6)), (round(pt[0]-delta_lat,6), round(pt[1]+delta_lon,6))

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
    #можно выдать рой треков в одном gpx и архив с отдельными треками
    pass

if __name__ == '__main__':
    start_time = time.time()
    # pic_dir = 'tmp'
    pic_dir = 'angara'
    # fsearch = "enisey/err.txt"
    fsearch = "enisey/search.txt"

    points = [
        # {'stag': "галин", 'coords': (51.94419, 102.37698), 'size': 100},
        # {'stag': "люб", 'coords': (51.94541, 102.43996), 'size': 100},
        # {'stag': "дружб", 'coords': (51.95099, 102.45566), 'size': 100},
        # {'stag': "мунк", 'coords': (51.71883, 100.59706), 'size': 100},
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
        # {'stag': "царьводопад", 'coords': (51.95621, 102.36019), 'size': 300},
        # {'stag': "мамай", 'coords': (51.38219, 104.85779), 'size': 100},
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

    # reg_to_find = get_sqr_region(mamai_vdp, 100)
    # sqr_region_2gpx('enisey/regions/sqr_region.gpx', reg_to_find)

    with open(fsearch, 'w') as ss:
        for fname in os.listdir(pic_dir):
            fname = f'{pic_dir}/{fname}'
            locations = []
            with open(fname, 'r', encoding='utf-8') as fgpx:
                parse_start_time = time.time()
                gpx = gpxpy.parse(fgpx)
                parse_time += time.time() - parse_start_time
            index_gpx(fname, gpx)
            gpx_desc = f'{fname}: mdname:\'{gpx.name}\' mdesc:\'{gpx.description}\''
            # gpx_desc = f'{gpx_desc} ele:{gpx.has_elevations()} time:{gpx.has_times()} '
            for track in gpx.tracks:
                try:
                    if len(track.description) < 256:
                        gpx_desc = f'{gpx_desc} trkname:\'{track.name}\' trkdesc:\'{track.description}\''
                    else:
                        gpx_desc = f'{gpx_desc} trkname:\'{track.name}\' trkdesc:TOOBIG'
                except (TypeError):
                    gpx_desc = f'{gpx_desc} trkname:\'{track.name}\' trkdesc:\'{track.description}\''
                for trkseg in track.segments:
                    # trkseg.get_speed()
                    for trkpt in trkseg.points:
                        pt = (float(trkpt.latitude), float(trkpt.longitude))
                        for point in points:
                            reg_to_find = get_sqr_region(point['coords'], point['size'])
                            d = is_in_sqr_region(reg_to_find, pt)
                            dcalc_time += d[1]
                            if d[0]:
                                if 'OK' not in locations:
                                    gpx_desc = f'{gpx_desc}'
                                    locations.append('OK')
                                if point['stag'] not in locations:
                                    locations.append(point['stag'])

            gpx_desc = f'{gpx_desc} loc:'
            for location in locations:
                gpx_desc = f'{gpx_desc} {location}'

            try:
                ss.write(f'{gpx_desc}\n')
            except (UnicodeEncodeError) as ee:
                gpx_desc = f"WERR {gpx_desc}"
            print(gpx_desc)

    full_time = time.time() - start_time
    dcalc_time_prc = round(100*dcalc_time/full_time,1)
    parse_time_prc = round(100*parse_time/full_time,1)
    print(f'Elapsed time: {time.time() - start_time} Calc time: {dcalc_time}({dcalc_time_prc}%) Parse time: {parse_time}({parse_time_prc}%)')

        # print(round(get_distance(pt_1,pt_2),  0))
