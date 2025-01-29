import os
import json
import gpxpy
from lxml import etree
from gpxpy.gpx import GPX
from trash import md5_checksum
from tokens import get_wtokens, get_ptokens, get_rtokens
from scache import index_gpx


# from normalize import is_match_xml_schema


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
        # if wtokens fjson.update({"w-tokens": wtokens})
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

    def search(self, stokens_list=None):
        # возвращаем отсортированный массив tuples'ов формата:
        # (суммарный к-т релевантности, частные к-ты w,p и r, имя,ссылка, )
        # в сервисе - соответствующий json
        # aa = [(12.4544, '00022.gpx', 'https://angara.net/2024/10/02/22.gpx'),
        #       (23.23443, '00023.gpx', 'https://angara.net/2024/10/03/23.gpx'),
        #       (11.234343, '00024.gpx', 'https://angara.net/2023/12/31/24.gpx')
        #       ]
        # aa.sort(reverse=True)
        # return aa
        pass


if __name__ == '__main__':

    index = GPXIndex("index00")

    # for fname in os.listdir("angara-tmp"):
    for fname in os.listdir("angara-w"):
        gpx_fname = f"angara-w/{fname}"
        gpx_href_fname = f"angara-l/{fname.split('.')[0]}.href"
        with open(gpx_href_fname, "r") as fhref:
            url = fhref.readline().strip('\n')
        index.add_gpx_from_file(gpx_fname, url)

    # os.makedirs("index00/wtrie/a/b/f", exist_ok=True)  # Создаём структуру каталогов
    # open("index00/wtrie/a/b/f/5fc0ee56", 'a').close()  # И вот появился файл`
    # os.makedirs("index00/wtrie/a/b/f", exist_ok=True)
    # open("index00/wtrie/a/b/f/5fc0ee57", 'a').close()
