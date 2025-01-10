import gpxpy



if __name__ == '__main__':
    fdir = 'regions'
    fname = f"{fdir}/kbzd_reg.gpx"
    fname_rd = f"{fdir}/kbzd_reg.rawdata"
    with open(fname, 'r', encoding='utf-8') as fgpx:
        gpx = gpxpy.parse(fgpx)
    with open(fname_rd, 'w') as fdata:
        for trk in gpx.tracks:
            for trkseg in trk.segments:
                for wpt in trkseg.points:
                    fdata.write(f"{wpt.latitude} {wpt.longitude} {wpt.time}\n")