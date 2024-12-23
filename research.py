import gpxpy

fname = "angara/289.gpx"

if __name__ == '__main__':
    with  open(fname, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        print(len(gpx.waypoints))
        # for waypoint in gpx.waypoints:
        #     print(f'{isval}\tcreator: {gpx.creator}\t\t\t{waypoint.name}')
        # for track in gpx.tracks:
        #     try:
        #         if track.name.lower().find('монды') != -1:
        #             print(f'FIND {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
        #         else:
        #             print(f'NOTFIND: {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
        #     except AttributeError:
        #         print(f'NOTFIND(exc): {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')