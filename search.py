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
    print(f"{d_lat}m {d_lon}m")
    # 0.1 нужно динамически поднастроить исходя из масштаба
    delta_lat = 0.01*(side_size/2.0)/d_lat
    delta_lon = 0.1*(side_size/2.0)/d_lon
    return (round(pt[0]+delta_lat,6), round(pt[1]-delta_lon,6)), (round(pt[0]-delta_lat,6), round(pt[1]+delta_lon,6))

def sqr_region_2gpx(path: str, region: tuple):
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Create points:
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(region[0][0], region[0][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(region[0][0], region[1][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(region[1][0], region[1][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(region[1][0], region[0][1]))
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(region[0][0], region[0][1]))
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
    galina = (51.94419, 102.37698)
    lovepeak = (51.94541, 102.43996)
    druzhba = (51.95099, 102.45566)
    munku =(51.71883, 100.59706)
    vit = (51.97477, 104.10470)
    idol =(51.95990, 104.08796)
    ulya = (51.92763, 102.64003)
    katka =(51.75186, 100.60565)
    arkhey = (52.00675, 105.31717)
    energetik =(51.95326, 102.50881)
    bronenos = (51.95626, 102.47578)
    trehglav_uzh = (51.96388, 102.36955)




    start_time = time.time()
    dcalc_time = 0
    parse_time = 0

    reg_to_find = get_sqr_region(trehglav_uzh, 500)
    sqr_region_2gpx('enisey/mumu.gpx', reg_to_find)


    for fname in os.listdir(pic_dir):
        fname = f'{pic_dir}/{fname}'
        # print(f'\n{fname}: ', end='')
        with open(fname, 'r', encoding='utf-8') as fgpx:
            parse_start_time = time.time()
            gpx = gpxpy.parse(fgpx)
            parse_time += time.time() - parse_start_time
            for track in gpx.tracks:
                for trkseg in track.segments:
                    for trkpt in trkseg.points:
                        pt = (float(trkpt.latitude), float(trkpt.longitude))
                        d = is_in_sqr_region(reg_to_find, pt)
                        dcalc_time += d[1]
                        if d[0]:
                            print(fname)
                            break
    full_time = time.time() - start_time
    dcalc_time_prc = round(100*dcalc_time/full_time,1)
    parse_time_prc = round(100*parse_time/full_time,1)
    print(f'Elapsed time: {time.time() - start_time} Calc time: {dcalc_time}({dcalc_time_prc}%) Parse time: {parse_time}({parse_time_prc}%)')
        # print(round(get_distance(pt_1,pt_2),  0))
