import os
import re
from gpxpy.gpx import GPX


# п.Доктор - почистить через регулярку
# убираем предлоги https://skysmart.ru/articles/russian/razryady-predlogov
# цифры, даты, 178-й километр
# Бабха-Чертики
# перевал пер. пик п. гора

def str_clean(s: str):
    res = list()
    pr = (
        'на', 'по', 'из', 'от', 'за', 'до', 'перед', 'без', 'через', 'над', 'про',
        'под', 'для', 'после', 'при', 'между', 'около', 'среди', 'вокруг', 'мимо',
        'возле', 'вдоль', 'спереди', 'слева', 'справа,' 'сзади',
    )
    mon = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
           'янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек',
           )

    strava = ('strava', 'by', 'stravatogpx', 'app')
    remove_symbols_queue0 = ',;:\'=()!?[]<>{}|*&^%$#@^|~_+-/\\'

    for symbol in remove_symbols_queue0:
        s = s.replace(symbol, ' ')
        s = re.sub(r'\d{1,4}', r'', s)

    for word in s.lower().split():
        word = re.sub(r'^\d{1,4}', r'', word)
        # word = re.sub(r'ст\.(\w+)', r'старая \1', word)
        # word = re.sub(r'ст\.', r'старая', word)
        word = re.sub(r'^ск\.(\w+)', r'скал \1', word)
        word = re.sub(r'^ск\.', r'скал', word)
        word = re.sub(r'^п\.(\w+)', r'пик \1', word)
        word = re.sub(r'^п\.', r'пик', word)
        word = re.sub(r'^пер\.(\w+)', r'перевал \1', word)
        word = re.sub(r'^пер\.', r'перевал', word)
        word = re.sub(r'^оз\.(\w+)', r'озеро \1', word)
        word = re.sub(r'^оз\.', r'озеро', word)
        word = re.sub(r'^р\.(\w+)', r'река \1', word)
        word = re.sub(r'^р\.', r'река', word)
        word = re.sub(r'^руч\.(\w+)', r'ручей \1', word)
        word = re.sub(r'^руч\.', r'ручей', word)


        # word = re.sub(r'\d{4}[_.-]\d\d[_.-]\d\d', r'', word)
        # word = re.sub(r'\d\d[_.-]\d\d[_.-]\d{4}', r'', word)
        # word = re.sub(r'\d\d[:-]\d\d([:-]\d\d)?', r'', word)

        # word = re.sub(r'^(\w+)[.:]$', r'\1', word)

        # is_time = re.match('\d{4}[_.-]\d\d[_.-]\d\d', word) \
        #           or re.match('\d\d[:-]\d\d([:-]\d\d)?', word) \
        #           or re.match('\d\d[_.-]\d\d[_.-]\d{4}', word)

        if len(word) > 1:
            # if word not in pr and word not in strava and word not in mon and not is_time:
            if word not in [*pr, *strava, *mon]:
                res.append(word)
    return ' '.join(res)


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
