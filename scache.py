import os
import re
from gpxpy.gpx import GPX


# п.Доктор - почистить через регулярку
# убираем предлоги https://skysmart.ru/articles/russian/razryady-predlogov
# цифры, даты, 178-й километр
# Бабха-Чертики
# перевал пер. пик п. гора

def str_clean(s: str):
    res = ''
    pr = [
        'на', 'по', 'из', 'от', 'за', 'до', 'перед', 'без', 'через', 'над', 'про',
        'под', 'для', 'после', 'при', 'между', 'около', 'среди', 'вокруг', 'мимо',
        'возле', 'вдоль',
    ]
    remove_symbols = ',()!?+[]/<>{}|*&^%$#@'
    replace_symbols = '_'
    for symbol in remove_symbols:
        s = s.replace(symbol, '')
    for symbol in replace_symbols:
        s = s.replace(symbol, ' ')
    for word in s.lower().split():
        is_time = re.match('\d{4}-\d\d-\d\d', word) or re.match('\d\d[:-]\d\d([:-]\d\d)?', word) \
                  or re.match('\d\d\.\d\d.\d{4}', word)
        if len(word) > 1:
            if word not in pr:
                if not is_time:
                    res = f'{res} {word}'
    return res


def index_gpx(fname: str, gpx: GPX):
    with open('enisey/eng.txt', 'a', encoding='utf-8') as ff:
        for track in gpx.tracks:
            if track.name:
                ff.write(f"{fname}: trkname:\'{track.name}\' clean:\'{str_clean(track.name)}\'\n")


if __name__ == '__main__':
    pass
    # fname = 'enisey/a/b/ab'
    # fpath = os.path.dirname(fname)
    #
    # if not os.path.exists(fpath):
    #     os.makedirs(fpath)
