import os
import json
import gpxpy
from gpxpy.gpx import GPX
from trash import md5_checksum


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

    def add_gpx_from_file(self, gpx_filename: str, gpx_href: str):

        fid = md5_checksum(gpx_filename)
        if os.path.isfile(f"{self.__index_dir}/{fid}.json"):
            print(f"File {gpx_filename} md5-hash: {fid} exists.")
            return None

        fjson = {"id": fid, "gpx-original-fname": os.path.split(gpx_filename)[1], "url": gpx_href, }

        # проверить схему, если не норм - fjson.update({"schema-valid":"False"}) else fjson.update({"schema-valid":"True"})

        with open(gpx_filename, 'r', encoding='utf-8') as fgpx:
            try:
                gpx = gpxpy.parse(fgpx)
            except:
                print(f"Parse Error: {gpx_filename}")
                return None
        fjson.update({"gpx-version": gpx.version})
        # wtokens = get_wtokens(gpx)
        # ptokens = get_ptokens(?)
        # rtokens = get_rtokens(?)

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

    def search(self, stokens_list):
        # возвращаем отсортированный массив tuples'ов формата (имя,ссылка, коэфф.релевантности)
        # в сервисе - соответствующий json
        pass


if __name__ == '__main__':
    gpx_dir = 'angara-w'
    href_dir = 'angara-l'

    index = GPXIndex("index00")
    for fname in os.listdir("angara-w"):
        gpx_fname = f"angara-w/{fname}"
        gpx_href_fname = f"angara-l/{fname.split('.')[0]}.href"
        with open(gpx_href_fname, "r") as fhref:
            url = fhref.readline().strip('\n')
        index.add_gpx_from_file(gpx_fname, url)

    # os.makedirs(os.path.dirname(путь_к_файлу), exist_ok=True)  # Создаём структуру каталогов
    # open(путь_к_файлу, 'a').close()  # И вот появился файл
