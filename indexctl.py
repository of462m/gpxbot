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
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g', '--gpx', action='store_true', help='Operate with gpx-tracks')
    group.add_argument('-p', '--points', action='store_true', help='Operate with gpx-formatted POINTS files')
    group.add_argument('-r', '--regions', action='store_true', help='Operate with gpx-formatted REGIONS files')
    parser.add_argument('-s', '--src', help='Source directory', required=True)
    parser.add_argument('-d', '--dst', help='Destination directory', required=True)
    args = parser.parse_args()
    print(args.__dict__)
    # if args.reindex:
    #     print("REINDEX")
    # add_points("enisey/points.gpx", "index00")
