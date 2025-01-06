import os
import geopy.distance
import gpxpy
from gpxpy.gpx import GPX
import time

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

    # Нарисовать карту углов!!! Посмотреть объекты в углах
    # Гипотеза - цели живут в углах
    start_time = time.time()
    get_bounds_time = 0

    pic_dir = 'angara'

    mygpx = gpxpy.gpx.GPX()
    init_new_gpx(mygpx)
    for fname in os.listdir(pic_dir):
        fname = f'{pic_dir}/{fname}'
        with open(fname, 'r', encoding='utf-8') as fgpx:
            gpx = gpxpy.parse(fgpx)
        get_bounds_start_time = time.time()
        bounds = gpx.get_bounds()
        get_bounds_time += time.time() - get_bounds_start_time

        try:
            if geopy.distance.geodesic(
                    (bounds.min_latitude, bounds.min_longitude),
                    (bounds.max_latitude,bounds.max_longitude)).km < 30.0:
                pt_A = (bounds.max_latitude, bounds.min_longitude)
                pt_B = (bounds.max_latitude, bounds.max_longitude)
                pt_C = (bounds.min_latitude, bounds.max_longitude)
                pt_D = (bounds.min_latitude, bounds.min_longitude)

                reg_A = get_sqr_region(pt_A, 300)
                reg_B = get_sqr_region(pt_B, 300)
                reg_C = get_sqr_region(pt_C, 300)
                reg_D = get_sqr_region(pt_D, 300)

                # add_sqr_trk_2gpx(mygpx, (bounds.min_latitude, bounds.max_latitude), (bounds.min_longitude, bounds.max_longitude), fname)
                add_sqr_trk_2gpx(mygpx, (reg_A[1][0], reg_A[0][0]), (reg_A[0][1],reg_A[1][1]), fname)
                add_sqr_trk_2gpx(mygpx, (reg_B[1][0], reg_B[0][0]), (reg_B[0][1],reg_B[1][1]), fname)
                add_sqr_trk_2gpx(mygpx, (reg_C[1][0], reg_C[0][0]), (reg_C[0][1],reg_C[1][1]), fname)
                add_sqr_trk_2gpx(mygpx, (reg_D[1][0], reg_D[0][0]), (reg_D[0][1],reg_D[1][1]), fname)

                print(f"{fname}:\tLAT: {bounds.min_latitude} {bounds.max_latitude} LON: {bounds.min_longitude} {bounds.max_longitude}")
        except(AttributeError) as ee:
            print(f"{fname}: {ee}")

        with open("enisey/sqr4map.gpx", 'w', encoding='utf-8') as gpx_to_file:
            gpx_to_file.write(mygpx.to_xml())
    full_time = time.time() - start_time
    getbound_time_prc = round(100 * get_bounds_time / full_time, 1)
    print(
        f'Elapsed time: {time.time() - start_time} getBounds time: {get_bounds_time}({getbound_time_prc}%)')
    exit(0)


    points = [
        {'stag': "галин", 'coords': (51.94419, 102.37698), 'size': 100},
        {'stag': "люб", 'coords': (51.94541, 102.43996), 'size': 100},
        {'stag': "дружб", 'coords': (51.95099, 102.45566), 'size': 100},
        {'stag': "мунк", 'coords': (51.71883, 100.59706), 'size': 100},
        {'stag': "хулугайш", 'coords': (51.74442, 100.98550), 'size': 100},
        {'stag': "сибизмир", 'coords': (51.75060, 100.92989), 'size': 100},
        {'stag': "витяз", 'coords': (51.97477, 104.10470), 'size': 200},
        {'stag': "идол", 'coords': (51.95990, 104.08796), 'size': 200},
        {'stag': "черепах", 'coords': (51.95648, 104.08997), 'size': 200},
        {'stag': "зеркал", 'coords': (51.97020, 104.13447), 'size': 200},
        {'stag': "verblud", 'coords': (51.97502, 104.14206), 'size': 200},
        {'stag': "starkrep", 'coords': (51.99310, 104.14044), 'size': 200},
        {'stag': "sk-obzor", 'coords': (51.94495, 103.91873), 'size': 200},
        {'stag': "sk-vorona", 'coords': (51.94314, 103.93111), 'size': 200},
        {'stag': "sk-shakhtay", 'coords': (51.94209, 103.95802), 'size': 200},
        {'stag': "sk-staruha", 'coords': (51.94667, 104.13498), 'size': 200},
        {'stag': "sk-medvezhata", 'coords': (51.96172, 104.14123), 'size': 200},
        {'stag': "ulyabor", 'coords': (51.92763, 102.64003), 'size': 100},
        {'stag': "oz_serebr", 'coords': (51.91614, 102.61360), 'size': 300},
        {'stag': "katka", 'coords': (51.75186, 100.60565), 'size': 100},
        {'stag': "архе", 'coords': (52.00675, 105.31717), 'size': 100},
        {'stag': "ohotnichya", 'coords': (52.13878, 105.46341), 'size': 100},
        {'stag': "energetik", 'coords': (51.95326, 102.50881), 'size': 100},
        {'stag': "bronenosets", 'coords': (51.95626, 102.47578), 'size': 100},
        {'stag': "трехглав", 'coords': (51.96388, 102.36955), 'size': 100},
        {'stag': "царьводопад", 'coords': (51.95621, 102.36019), 'size': 300},
        {'stag': "мамай", 'coords': (51.38219, 104.85779), 'size': 100},
        {'stag': "порожист", 'coords': (51.43389, 104.03761), 'size': 100},
        {'stag': "черск", 'coords': (51.51563, 103.62597), 'size': 100},
        {'stag': "тальцинск", 'coords': (51.35050, 104.58954), 'size': 100},
        {'stag': "босан", 'coords': (51.44329, 103.37566), 'size': 100},
        {'stag': "сердце", 'coords': (51.50997, 103.62532), 'size': 300},
        {'stag': "паруса", 'coords': (51.73974, 103.85860), 'size': 500},
        {'stag': "козий", 'coords': (52.44374, 103.13353), 'size': 500},
    ]



    dcalc_time = 0
    parse_time = 0

    # reg_to_find = get_sqr_region(mamai_vdp, 100)
    # sqr_region_2gpx('enisey/regions/sqr_region.gpx', reg_to_find)

    with open("enisey/search.txt", 'w') as ss:
        for fname in os.listdir(pic_dir):
            fname = f'{pic_dir}/{fname}'
            locations = []
            with open(fname, 'r', encoding='utf-8') as fgpx:
                parse_start_time = time.time()
                gpx = gpxpy.parse(fgpx)
                parse_time += time.time() - parse_start_time
            # pr
            # int(gpx.get_bounds().min_latitude, gpx.get_bounds().max_latitude)
            gpx_desc = f'{fname}: mdname:\'{gpx.name}\' mdesc:\'{gpx.description}\''
            # gpx_desc = f'{gpx_desc} ele:{gpx.has_elevations()} time:{gpx.has_times()} '
            for track in gpx.tracks:
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
                                    gpx_desc = f'{gpx_desc}\b'
                                    locations.append('OK')
                                if point['name'] not in locations:
                                    locations.append(point['name'])



            gpx_desc = f'{gpx_desc} loc:'
            for location in locations:
                gpx_desc = f'{gpx_desc} {location}'
            print(gpx_desc)
            ss.write(f'{gpx_desc}\n')

    full_time = time.time() - start_time
    dcalc_time_prc = round(100*dcalc_time/full_time,1)
    parse_time_prc = round(100*parse_time/full_time,1)
    print(f'Elapsed time: {time.time() - start_time} Calc time: {dcalc_time}({dcalc_time_prc}%) Parse time: {parse_time}({parse_time_prc}%)')

        # print(round(get_distance(pt_1,pt_2),  0))
