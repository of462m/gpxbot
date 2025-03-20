import gpxpy
from gpxpy.gpx import GPX
from gpxindex.index import get_trk_season

# п.Доктор - почистить через регулярку
# убираем предлоги https://skysmart.ru/articles/russian/razryady-predlogov
# цифры, даты, 178-й километр
from gpxindex.tokens import tokenize


def index_gpx(fname: str, gpx: GPX, index_dir: str='index'):
    with open('enisey/eng.txt', 'a', encoding='utf-8') as ff:
        sstr = list()
        if gpx.name:
            sstr.append(gpx.name)
        # trk-ов может быть несколько!
        for trk in gpx.tracks:
            if trk.name:
                sstr.append(trk.name)
            if trk.description:
                if len(trk.description) < 256:
                    sstr.append(trk.description)
            ff.write(f"{fname}[trk]: season: {get_trk_season(gpx)} sstr:\'{' '.join(sstr)}\' w-tokens:\'{tokenize(' '.join(sstr))}\'\n")
        for rte in gpx.routes:
            if rte.name:
                sstr.append(rte.name)
            ff.write(f"{fname}[rte]: season: {get_trk_season(gpx)} sstr:\'{' '.join(sstr)}\' w-tokens:\'{tokenize(' '.join(sstr))}\'\n")
def raw_gpx(fname: str, gpx: GPX, raw_dir: str='dat/trk'):
    pass


if __name__ == '__main__':
    with open("gpx/test.gpx", "r", encoding='utf-8') as fgpx:
        gpx = gpxpy.parse(fgpx)
    for wpt in gpx.waypoints:
        for ext in wpt.extensions:
            print(f"{ext.tag}: {ext.text}")