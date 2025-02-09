import argparse
import gpxpy
from gpxpy.gpx import GPX
from index import GPXIndex


def get_gpx(fname: str) -> GPX:
    with open(fname, "r", encoding='utf-8') as fgpx:
        try:
            gpx = gpxpy.parse(fgpx)
        except:
            print("Что-то пошло не так...")
            exit(0)
    return gpx


def add_points(fname: str, index: str, reindex: bool = False) -> None:
    index = GPXIndex(index)
    index.add_points(get_gpx(fname))


def add_region(fname: str, index: str, reindex: bool = False) -> None:
    pass


def add_gpx_track(fname: str, index: str) -> None:
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', type=str, help='command')
    parser.add_argument('obj', type=str, help='object')
    parser.add_argument('filename', type=str, help='filename')
    parser.add_argument('--reindex')
    args = parser.parse_args()
    print(args.cmd)
    if args.reindex:
        print("REINDEX")
    # add_points("enisey/points.gpx", "index00")
