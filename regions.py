import gpxpy
from gpxpy.gpx import GPX

def get_gpx_season(gpx: GPX):
    ms = ('зима', 'зима', 'весна',
          'весна','весна', 'лето',
          'лето', 'лето', 'осень',
          'осень', 'осень', 'зима',
          )
    if gpx.has_times():
        return ms[gpx.tracks[0].segments[0].points[0].time.month - 1]
    else:
        return ''




    pass

if __name__ == '__main__':
    fdir = 'regions'
    fname = f"{fdir}/unconvex.gpx"
    fname_rd = f"{fdir}/unconvex.dat"
    with open(fname, 'r', encoding='utf-8') as fgpx:
        gpx = gpxpy.parse(fgpx)
    print(get_gpx_season(gpx))
    with open(fname_rd, 'w') as fdata:
        for trk in gpx.tracks:
            for trkseg in trk.segments:
                for wpt in trkseg.points:
                    # fdata.write(f"{wpt.latitude} {wpt.longitude} {wpt.time.month}\n")
                    fdata.write(f"{wpt.latitude} {wpt.longitude}\n")