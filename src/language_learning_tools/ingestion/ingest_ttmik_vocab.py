from language_learning_tools.util.korean_util import is_word_all_hangul


def _split_str(x):
    split_by_space = x.split(' ')
    if len(split_by_space) < 2:
        return None
    else:
        return split_by_space[-1], ' '.join(split_by_space[:-1])


def _get_tuple_from_ttmik_line(ttmik_line):
    line_parts = _split_str(ttmik_line)
    if line_parts is None or not is_word_all_hangul(line_parts[0]):
        return None
    else:
        return line_parts


def make_tuples_from_ttmik(ttmik_data):
    kor_eng_tuples = [_get_tuple_from_ttmik_line(_line) for _line in ttmik_data.split('\n')]
    return [_tuple for _tuple in kor_eng_tuples if _tuple is not None]
