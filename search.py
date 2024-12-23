import os
import geopy.distance
import gpxpy
import time

def get_distance(pt_1: tuple, pt_2: tuple):
    return geopy.distance.geodesic(pt_1, pt_2).m

if __name__ == '__main__':

    pic_dir = 'angara'
    galina = (51.94419, 102.37698)

    start_time = time.time()
    for fname in os.listdir(pic_dir):
        fname = f'{pic_dir}/{fname}'
        # print(f'\n{fname}: ', end='')
        with  open(fname, 'r', encoding='utf-8') as fgpx:
            gpx = gpxpy.parse(fgpx)
            for track in gpx.tracks:
                for trkseg in track.segments:
                    for trkpt in trkseg.points:
                        pt = (float(trkpt.latitude), float(trkpt.longitude))
                        # print(f"{trkpt.latitude}\t{trkpt.longitude}")
                        if get_distance(galina, pt) < 50:
                            print(fname)
                            break

    print('Elapsed time: ', time.time() - start_time)
        # print(round(get_distance(pt_1,pt_2),  0))
