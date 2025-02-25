from Levenshtein import jaro_winkler

places = (
    'пик', 'перевал', 'озеро', 'река', 'ручей', 'водопад', 'ущелье', 'хребет', 'пещера', 'бухта', 'залив', 'мыс',
    'урочище', 'зимовье', 'остров', 'падь', 'скала', 'скальник', 'станция',
)


def get_score(fid_data: dict, search_tokens: list) -> list:
    score = list()
    for tokens_key in ('w-token', 'p-token', 'r-token'):
        max_value = 0
        for search_token in search_tokens:
            max_t = 0
            if fid_data[tokens_key]:
                for token in fid_data[tokens_key]:
                    max_t = max(max_t, jaro_winkler(search_token, token, score_cutoff=0.88))
            max_value += max_t
        score.append(max_value)
    return score



if __name__ == '__main__':
    pass
