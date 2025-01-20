import os
import gpxpy
from gpxpy.gpx import GPX



class GPX_Index():

    @property
    def root_dir(self):
        return self.__root_dir

    @property
    def href_dir(self):
        return self.__href_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def wtrie_dir(self):
        return self.__wtrie_dir

    def __init__(self, root_dir):
        self.__root_dir = root_dir
        self.__href_dir = f"{root_dir}/href/"
        self.__data_dir = f"{root_dir}/data/"
        self.__wtrie_dir = f"{root_dir}/wtrie/"

    def init(self):
        os.makedirs(self.__href_dir)
        os.makedirs(self.__data_dir)
        os.makedirs(self.__wtrie_dir)

    def add_gpx(self, gpx_filename):
        pass

    def search(self, search_str):
        #возвращаем отсортированный массив tuples'ов формата (имя,ссылка,коэфф. релевантности,)
        pass


if __name__ == '__main__':
    gpx_dir = 'angara-w'
    href_dir = 'angara-l'

    index = GPX_Index("index00")
    # index.init()

    # os.makedirs(os.path.dirname(путь_к_файлу), exist_ok=True)  # Создаём структуру каталогов
    # open(путь_к_файлу, 'a').close()  # И вот появился файл
