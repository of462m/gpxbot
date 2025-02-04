import hashlib
import os
import json
import gpxpy
from lxml import etree
from gpxpy.gpx import GPX
from Levenshtein import jaro_winkler, distance as l_distance
from tokens import tokenize, get_wtokens, get_ptokens, get_rtokens
from scache import index_gpx


# from normalize import is_match_xml_schema
def md5_checksum(filepath, tail: int = 8):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()[-tail:]


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

    def add_point(self, lat: float, lon: float, size: float, p_tokens: list):
        pass

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
