import gpxpy
from index import GPXIndex


def add_points(fname: str) -> None:
    with open(fname, "r", encoding='utf-8') as fgpx:
        try:
            gpx = gpxpy.parse(fgpx)
        except:
            print("Что-то пошло не так...")
            exit(0)
        index = GPXIndex("index00")
        index.add_points(gpx)


if __name__ == '__main__':
    add_points("enisey/points.gpx")
