import gpxpy

fname = "angara/289.gpx"
# mond = (51.82069, 100.89603, 51.66572, 101.14872)
mond = (51.85732, 100.33554, 51.68566, 100.85739)






if __name__ == '__main__':
    with  open(fname, 'r', encoding='utf-8') as gpx_from_file:
        gpx = gpxpy.parse(gpx_from_file)
    gpxgen = gpxpy.gpx.GPX()
    gpxgen.creator = 'Taras I.Madzhara'
    gpxgen.author_email = 'taras@icc.ru'

    for wpt in gpx.waypoints:
        lat, lon, nam = wpt.latitude, wpt.longitude, wpt.name
        if lat > mond[2]:
            if lat < mond[0]:
                if lon > mond[1]:
                    if lon < mond[3]:
                        gpx_wpt = gpxpy.gpx.GPXWaypoint(longitude=lon, latitude=lat,name=nam)
                        gpxgen.waypoints.append(gpx_wpt)
    with open("enisey/primunk.gpx", 'w', encoding='utf-8') as gpx_to_file:
        gpx_to_file.write(gpxgen.to_xml())


    # print(len(gpx.waypoints))
    # for waypoint in gpx.waypoints:





        # for track in gpx.tracks:
        #     try:
        #         if track.name.lower().find('монды') != -1:
        #             print(f'FIND {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
        #         else:
        #             print(f'NOTFIND: {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
        #     except AttributeError:
        #         print(f'NOTFIND(exc): {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')