import os
import geopy.distance
import gpxpy
import time

def get_distance(pt_1: tuple, pt_2: tuple):
    start_time = time.time()
    d = geopy.distance.geodesic(pt_1, pt_2).m
    return d, time.time() - start_time

if __name__ == '__main__':

    pic_dir = 'angara'
    galina = (51.94419, 102.37698)
    lovepeak = (51.94541, 102.43996)

    start_time = time.time()
    dcalc_time = 0
    parse_time = 0
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
                        d = get_distance(lovepeak, pt)
                        dcalc_time += d[1]
                        if d[0] < 50:
                            print(fname)
                            break
    full_time = time.time() - start_time
    dcalc_time_prc = round(100*dcalc_time/full_time,1)
    parse_time_prc = round(100*parse_time/full_time,1)
    print('Elapsed time: ', time.time() - start_time, 'Calc time: ', dcalc_time, 'Parse time: ', parse_time)
    print(f'Elapsed time: {time.time() - start_time} Calc time: {dcalc_time}({dcalc_time_prc}%) Parse time: {parse_time}({parse_time_prc}%)')
        # print(round(get_distance(pt_1,pt_2),  0))
