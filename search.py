import os
import geopy.distance
import gpxpy
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

if __name__ == '__main__':

    pic_dir = 'angara'

    points = [
        # {'name': "galina", 'coords': (51.94419, 102.37698), 'size': 100},
        # {'name': "lovepeak", 'coords': (51.94541, 102.43996), 'size': 100},
        # {'name': "druzhba", 'coords': (51.95099, 102.45566), 'size': 100},
        # {'name': "munka", 'coords': (51.71883, 100.59706), 'size': 100},
        {'name': "hulugaisha", 'coords': (51.74442, 100.98550), 'size': 100},
        {'name': "sibizmir", 'coords': (51.75060, 100.92989), 'size': 100},
        # {'name': "vityaz", 'coords': (51.97477, 104.10470), 'size': 200},
        # {'name': "idol", 'coords': (51.95990, 104.08796), 'size': 200},
        # {'name': "cherepaha", 'coords': (51.95648, 104.08997), 'size': 200},
        # {'name': "zerkala", 'coords': (51.97020, 104.13447), 'size': 200},
        # {'name': "verblud", 'coords': (51.97502, 104.14206), 'size': 200},
        # {'name': "starkrep", 'coords': (51.99310, 104.14044), 'size': 200},
        # {'name': "sk-obzor", 'coords': (51.94495, 103.91873), 'size': 200},
        # {'name': "sk-vorona", 'coords': (51.94314, 103.93111), 'size': 200},
        # {'name': "sk-shakhtay", 'coords': (51.94209, 103.95802), 'size': 200},
        # {'name': "sk-staruha", 'coords': (51.94667, 104.13498), 'size': 200},
        # {'name': "sk-medvezhata", 'coords': (51.96172, 104.14123), 'size': 200},
        # {'name': "ulyabor", 'coords': (51.92763, 102.64003), 'size': 100},
        {'name': "oz_serebr", 'coords': (51.91614, 102.61360), 'size': 300},
        # {'name': "katka", 'coords': (51.75186, 100.60565), 'size': 100},
        # {'name': "arkhey", 'coords': (52.00675, 105.31717), 'size': 100},
        {'name': "ohotnichya", 'coords': (52.13878, 105.46341), 'size': 100},
        # {'name': "energetik", 'coords': (51.95326, 102.50881), 'size': 100},
        # {'name': "bronenosets", 'coords': (51.95626, 102.47578), 'size': 100},
        # {'name': "trehglav_uzh", 'coords': (51.96388, 102.36955), 'size': 100},
        {'name': "tsar_vdp", 'coords': (51.95621, 102.36019), 'size': 300},
        # {'name': "mamai_vdp", 'coords': (51.38219, 104.85779), 'size': 100},
        # {'name': "porozh", 'coords': (51.43389, 104.03761), 'size': 100},
        # {'name': "cherskogo", 'coords': (51.51563, 103.62597), 'size': 100},
        # {'name': "talcin", 'coords': (51.35050, 104.58954), 'size': 100},
        {'name': "bosan", 'coords': (51.44329, 103.37566), 'size': 100},
        {'name': "oz-serdce", 'coords': (51.50997, 103.62532), 'size': 300},
        {'name': "sk-parusa", 'coords': (51.73974, 103.85860), 'size': 500},
    ]

    galina = (51.94419, 102.37698)
    lovepeak = (51.94541, 102.43996)
    druzhba = (51.95099, 102.45566)
    munku =(51.71883, 100.59706)
    vit = (51.97477, 104.10470)
    idol =(51.95990, 104.08796)
    cherep = (51.95648, 104.08997)
    zerkala = (51.97020, 104.13447)
    verblud = (51.97502, 104.14206)
    starkrep = (51.99310, 104.14044)
    ulyabor = (51.92763, 102.64003)
    katka =(51.75186, 100.60565)
    arkhey = (52.00675, 105.31717)
    energetik =(51.95326, 102.50881)
    bronenos = (51.95626, 102.47578)
    trehglav_uzh = (51.96388, 102.36955)
    mamai_vdp = (51.38219, 104.85779)


    start_time = time.time()
    dcalc_time = 0
    parse_time = 0

    # reg_to_find = get_sqr_region(mamai_vdp, 100)
    # sqr_region_2gpx('enisey/regions/sqr_region.gpx', reg_to_find)

    with open("enisey/search.txt", 'w') as ss:
        for fname in os.listdir(pic_dir):
            fname = f'{pic_dir}/{fname}'
            locations = []
            gpx_desc = f'{fname}: '
            with open(fname, 'r', encoding='utf-8') as fgpx:
                parse_start_time = time.time()
                gpx = gpxpy.parse(fgpx)
                parse_time += time.time() - parse_start_time
            if gpx.has_elevations():
                gpx_desc = f'{gpx_desc}ele:yes '
            else:
                gpx_desc = f'{gpx_desc}ele:no '
            if gpx.has_times():
                gpx_desc = f'{gpx_desc}times:yes '
            else:
                gpx_desc = f'{gpx_desc}times:no '
            gpx_desc = f'{gpx_desc}loc:[ '
            for track in gpx.tracks:
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

            for location in locations:
                gpx_desc = f'{gpx_desc}{location},'
            gpx_desc = f'{gpx_desc}\b]'
            print(gpx_desc)
            ss.write(f'{gpx_desc}\n')

    full_time = time.time() - start_time
    dcalc_time_prc = round(100*dcalc_time/full_time,1)
    parse_time_prc = round(100*parse_time/full_time,1)
    print(f'Elapsed time: {time.time() - start_time} Calc time: {dcalc_time}({dcalc_time_prc}%) Parse time: {parse_time}({parse_time_prc}%)')

        # print(round(get_distance(pt_1,pt_2),  0))
