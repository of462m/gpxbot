import hashlib
import os
import json
import io

import geopy.distance
import gpxpy
from lxml import etree
from gpxpy.gpx import GPX
from Levenshtein import jaro_winkler, distance as l_distance

from tokens import tokenize, get_wtokens, get_ptokens, get_rtokens


# from normalize import is_match_xml_schema
def md5_checksum(filepath: str, tail: int = 8) -> str:
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()[-tail:]


def get_max(a: float, b: float) -> float:
    return a if a > b else b


def get_min(a: float, b: float) -> float:
    return a if a < b else b


def get_sqr_region(pt: tuple, side_size: int) -> tuple:
    d_lat = geopy.distance.geodesic(pt, (pt[0] + 0.01, pt[1])).m
    d_lon = geopy.distance.geodesic(pt, (pt[0], pt[1] + 0.1)).m
    # print(f"{d_lat}m {d_lon}m")
    # 0.1 нужно динамически поднастроить исходя из масштаба
    delta_lat = 0.01 * (side_size / 2.0) / d_lat
    delta_lon = 0.1 * (side_size / 2.0) / d_lon
    return round(pt[0] - delta_lat, 6), round(pt[1] - delta_lon, 6), \
           round(pt[0] + delta_lat, 6), round(pt[1] + delta_lon, 6)


class RegBounds:
    __slots__ = ('min_lat', 'min_lon', 'max_lat', 'max_lon',)

    def reset(self) -> None:
        self.min_lat, self.max_lat = 90.0, -90.0
        self.min_lon, self.max_lon = 180.0, -180.0

    def __init__(self):
        self.reset()

    def recalc(self, lat: float, lon: float) -> None:
        self.min_lat = get_min(self.min_lat, lat)
        self.min_lon = get_min(self.min_lon, lon)
        self.max_lat = get_max(self.max_lat, lat)
        self.max_lon = get_max(self.max_lon, lon)

    def __repr__(self):
        # return f"MIN: {self.min_lat} {self.min_lon} MAX: {self.max_lat} {self.max_lon}"
        return f"{round(self.min_lat, 6)} {round(self.min_lon, 6)} {round(self.max_lat, 6)} {round(self.max_lon, 6)}"


class GPXIndex:

    @property
    def root_dir(self):
        return self.__root_dir

    def __init__(self, root_dir):
        self.__root_dir = root_dir
        self.__gpx_data_dir = f"{root_dir}/data/"
        self.__index_dir = f"{root_dir}/index/"
        self.__points_dir = f"{root_dir}/points/"
        self.__regions_dir = f"{root_dir}/regions/"
        self.__wtrie_dir = f"{root_dir}/wtrie/"

        if not os.path.isdir(root_dir):
            os.makedirs(self.__gpx_data_dir)
            os.makedirs(self.__index_dir)
            os.makedirs(self.__points_dir)
            os.makedirs(self.__regions_dir)
            os.makedirs(self.__wtrie_dir)

        self.__gpx10_xmlschema_doc = etree.parse('gpx10.xsd')
        self.__gpx10_xmlschema = etree.XMLSchema(self.__gpx10_xmlschema_doc)
        self.__gpx11_xmlschema_doc = etree.parse('gpx11.xsd')
        self.__gpx11_xmlschema = etree.XMLSchema(self.__gpx11_xmlschema_doc)

    def __add_to_wtrie(self, fid: str, tokens: list) -> None:
        for token in tokens:
            wtrie_path = '/'.join(list(token[:3]))
            os.makedirs(f"{self.__wtrie_dir}{wtrie_path}", exist_ok=True)
            open(f"{self.__wtrie_dir}{wtrie_path}/{fid}", 'a').close()

    def __get_from_wtrie(self, tokens: list) -> list:
        token_fids = list()
        for token in tokens:
            wtrie_path = '/'.join(list(token[:3]))
            if os.path.isdir(f"{self.__wtrie_dir}{wtrie_path}"):
                for fname in os.listdir(f"{self.__wtrie_dir}{wtrie_path}"):
                    if os.path.isfile(f"{self.__wtrie_dir}{wtrie_path}/{fname}"):
                        token_fids.append(fname)
        return list(dict.fromkeys(token_fids))

    def __get_from_json(self, fid: str) -> dict:
        with open(f"{self.__index_dir}{fid}.json", "r", encoding='utf-8') as ff:
            return json.load(ff)

    def add_gpx_to_data(self, gpx: GPX, fid: str) -> None:
        bounds = RegBounds()
        linesnum = 0

        with io.StringIO() as sbuf:
            for track in gpx.tracks:
                for trkseg in track.segments:
                    linesnum += len(trkseg.points)
                    for trkpoint in trkseg.points:
                        sbuf.write(f"{trkpoint.latitude} {trkpoint.longitude}\n")
                        bounds.recalc(trkpoint.latitude, trkpoint.longitude)
            for route in gpx.routes:
                linesnum += len(route.points)
                for rtept in route.points:
                    sbuf.write(f"{rtept.latitude} {rtept.longitude}\n")
                    bounds.recalc(rtept.latitude, rtept.longitude)
            linesnum += len(gpx.waypoints)
            for wpt in gpx.waypoints:
                sbuf.write(f"{wpt.latitude} {wpt.longitude}\n")
                bounds.recalc(wpt.latitude, wpt.longitude)

            sbuf.seek(0)
            with open(f"{self.__gpx_data_dir}{fid}.dat", "w", encoding='utf-8') as fdat:
                fdat.write(f"{linesnum}\n")
                fdat.write(f"{bounds}\n")
                for line in sbuf.readlines():
                    fdat.write(line)

    def add_gpx_from_file(self, gpx_filename: str, gpx_href: str = None):
        # если gpx_href = None - размещаем у себя
        fid = md5_checksum(gpx_filename)
        if os.path.isfile(f"{self.__index_dir}/{fid}.json"):
            print(f"File {gpx_filename} md5-hash: {fid} exists.")
            return None

        fjson = {"id": fid, "filename": os.path.split(gpx_filename)[1], "url": gpx_href, }
        # fjson.update({"author-tg-id": author_tg_id, "author-tg-name": author_tg_name})
        # fjson.update({"upload-time": upload_time})
        # проверить схему, если не норм - fjson.update({"match-gpx-xml-schema": "False"})
        # else fjson.update({"match-gpx-xml-schema": "True"})
        # is_match_xml_schema
        # fjson.update({"match-gpx-xml-schema": is_match_gpx_xml_schema(?)})

        with open(gpx_filename, 'r', encoding='utf-8') as fgpx:
            try:
                gpx = gpxpy.parse(fgpx)
            except:
                print(f"Parse Error: {gpx_filename}")
                return None
        # create_data

        fjson.update({"gpx-version": gpx.version})
        if gpx.name:
            fjson.update({"gpx-name": gpx.name})
        if gpx.description:
            fjson.update({"gpx-desc": gpx.description})
        # index_gpx(gpx_filename, gpx)
        wtokens = get_wtokens(gpx)
        if len(wtokens):
            self.__add_to_wtrie(fid, wtokens)
            fjson.update({"w-tokens": wtokens})

        # ptokens = get_ptokens(?)
        # if ptokens fjson.update({"p-tokens": ptokens})
        # rtokens = get_rtokens(?)
        # if rtokens fjson.update({"r-tokens": rtokens})
        # self.wtrie_insert(?)

        with open(f"{self.__index_dir}/{fid}.json", "w") as ff:
            # json.dump(fjson, ff, sort_keys=False, ensure_ascii=False)
            json.dump(fjson, ff, sort_keys=False, ensure_ascii=False, indent=3)

        return 1

    def add_gpx_from_buf(self):
        pass

    def add_points(self, gpx_points: GPX):
        with open(f"{self.__points_dir}{gpx_points.name}.dat", "w", encoding='utf-8') as fdat:
            for point in gpx_points.waypoints:
                name_tokens = point.name.split()
                size = float(name_tokens[0])
                p_tokens = ' '.join(name_tokens[1:])
                sqr_region = get_sqr_region((point.latitude, point.longitude), size)
                fdat.write(f"{sqr_region[0]} {sqr_region[1]} {sqr_region[2]} {sqr_region[3]} {p_tokens}\n")

    def add_region(self, gpx_region: GPX, r_tokens: list):
        pass

    def search(self, tokens_str: str):
        tokens = tokenize(tokens_str)
        # для чистки хвостов из places-токенов
        #
        max_metric = len(tokens)
        res_fids = list()
        tokens_fids = self.__get_from_wtrie(tokens)
        for tokens_fid in tokens_fids:
            fid_data = self.__get_from_json(tokens_fid)
            # убрать в отдельную ф-цию в metric:
            fid_max = 0
            for token in tokens:
                max_w = 0
                for wtoken in fid_data['w-tokens']:
                    max_w = max(max_w, jaro_winkler(token, wtoken, score_cutoff=0.88))
                fid_max += max_w
            # вот по сюда (ввести коэфф-т уменьшения для places-токенов)
            fid_data.update({"w": round(fid_max, 4)})
            # fid_data.pop("w-tokens")
            if fid_max:
                res_fids.append(fid_data)
        res_fids = sorted(res_fids, key=lambda d: d['w'], reverse=True)
        res = {"search-str": tokens_str, "search-tokens": tokens, "results-number": len(res_fids),
               "search-results": res_fids}
        print(json.dumps(res, ensure_ascii=False))


if __name__ == '__main__':

    index = GPXIndex("index01")
    index.search('любовь')
    exit(0)
    # for fname in os.listdir("angara-tmp"):
    for fname in os.listdir("angara-tmp"):
        gpx_fname = f"angara-tmp/{fname}"
        gpx_href_fname = f"angara-l/{fname.split('.')[0]}.href"
        with open(gpx_href_fname, "r") as fhref:
            url = fhref.readline().strip('\n')
        index.add_gpx_from_file(gpx_fname, url)
