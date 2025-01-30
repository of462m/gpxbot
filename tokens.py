import re
from gpxpy.gpx import GPX


def str_clean(s: str):
    res = list()
    pr = (
        'на', 'по', 'из', 'от', 'за', 'до', 'перед', 'без', 'через', 'над', 'про',
        'под', 'для', 'после', 'при', 'между', 'около', 'среди', 'вокруг', 'мимо',
        'возле', 'вдоль', 'спереди', 'слева', 'справа,' 'сзади', 'не', 'км', 'туда',
        'обратно', 'же',
    )
    mon = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
           'янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек',
           )
    mday = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
            'пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс',
            )

    strava = ('strava', 'by', 'stravatogpx', 'app')
    # ё к е !!!
    remove_symbols_queue0 = '\n,;:\'"=()!?[]<>{}|*&^%$#@^|~_+-/\\'

    for symbol in remove_symbols_queue0:
        s = s.replace(symbol, ' ')
        s = re.sub(r'\d{1,4}', r'', s)

    for word in s.lower().split():
        word = re.sub(r'^\d{1,4}', r'', word)
        # word = re.sub(r'ст\.(\w+)', r'старая \1', word)
        # word = re.sub(r'ст\.', r'старая', word)
        word = re.sub(r'^ск\.(\w+)?$', r'скал \1', word)
        # word = re.sub(r'^ск\.', r'скал', word)
        word = re.sub(r'^п\.(\w+)?$', r'пик \1', word)
        # word = re.sub(r'^п\.', r'пик', word)
        word = re.sub(r'^пер\.(\w+)?$', r'перевал \1', word)
        # word = re.sub(r'^пер\.', r'перевал', word)
        word = re.sub(r'^оз\.(\w+)?$', r'озеро \1', word)
        # word = re.sub(r'^оз\.', r'озеро', word)
        word = re.sub(r'^р\.(\w+)?$', r'река \1', word)
        # word = re.sub(r'^р\.', r'река', word)
        word = re.sub(r'^руч\.(\w+)?$', r'ручей \1', word)
        # word = re.sub(r'^руч\.', r'ручей', word)
        word = re.sub(r'^зим\.(\w+)?$', r'зимовье \1', word)
        # word = re.sub(r'^зим\.', r'зимовье', word)
        word = re.sub(r'^м\.(\w+)?$', r'мыс \1', word)
        word = re.sub(r'^бух\.(\w+)?$', r'бухта \1', word)
        word = re.sub(r'^пещ\.(\w+)?$', r'пещера \1', word)
        word = re.sub(r'^ст\.(\w+)?$', r'станция старая \1', word)
        word = re.sub(r'^ур\.(\w+)?$', r'урочище \1', word)
        word = re.sub(r'^о\.(\w+)?$', r'остров озеро \1', word)

        word = word.replace('.', ' ')
        for token in word.split():
            if len(token) > 1 and token not in [*pr, *strava, *mon, *mday]:
                res.append(token)
                res = list(dict.fromkeys(res))
    return ' '.join(res)


def get_wtokens(gpx: GPX):
    return ['абра', 'кодабра']


def get_ptokens(gpx: GPX):
    pass


def get_rtokens(gpx: GPX):
    pass
