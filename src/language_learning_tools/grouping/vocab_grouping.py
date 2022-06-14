import re

import pandas as pd

STOP_WORDS = {
    'a',
    'at',
    'or',
    'to',
    'of',
    'in',
    'be',
    'that',
    'this',
    'for',
    'when',
    'the',
    'and',
    'do',
    'from'
}
SPECIAL_PHRASES = [
    ('when modifying a counting unit that follows', 'when_modifying_a_counting_unit_that_follows'),
    ('counting unit', 'counting_unit')
]


def get_non_stop_words(x):
    x_no_punct = re.sub('[()/|,]', ' ', x)
    for orig_phrase, new_phrase in SPECIAL_PHRASES:
        x_no_punct = x_no_punct.replace(orig_phrase, new_phrase)
    words = x_no_punct.split(' ')
    non_stop_words = [_word for _word in words if len(_word) > 0 and _word not in STOP_WORDS]
    non_stop_words_out = list(set(non_stop_words))
    non_stop_words_out.sort()
    return tuple(non_stop_words_out)


def get_all_substsrs(_str):
    return [_str[i: j] for i in range(len(_str))
            for j in range(i + 1, len(_str) + 1)]


def get_hanja_substrs(x):
    hanja_wo_hada = x[:-2] if x.endswith('하다') else x
    if len(hanja_wo_hada) < 1:
        return 'X'
    else:
        return get_all_substsrs(hanja_wo_hada)


def get_hangul_substrs(x):
    hangul_wo_hada = x[:-2] if x.endswith('하다') else x
    hangul_wo_hada = x[:-1] if hangul_wo_hada.endswith('다') else hangul_wo_hada
    if len(hangul_wo_hada) < 1:
        return 'X'
    else:
        return get_all_substsrs(hangul_wo_hada)


def get_hangul_hanja_tuples(x):
    hangul_substrs = get_hangul_substrs(x[0])
    hanja_substrs = get_hanja_substrs(x[1])
    if 'X' in hanja_substrs:
        return tuple([(hangul_ch, 'X') for hangul_ch in hangul_substrs])
    else:
        return tuple(zip(hangul_substrs, hanja_substrs))


def add_col_with_parts(lang_df, parts_col_name, col_to_split, func_for_splitting):
    lang_df[parts_col_name] = lang_df[col_to_split].apply(func_for_splitting)
    lang_df = lang_df.drop_duplicates()
    return lang_df


# TODO: DEPRECATE
# def get_kor_english_duplicate_def_df(kor_eng_tuples_df,
#                                      english_col_name,
#                                      korean_col_name,
#                                      english_parts_col_name=ENGLISH_PARTS_COL_NAME):
#     eng_kor_dict_dup_entries = kor_eng_tuples_df \
#         .groupby([korean_col_name, english_parts_col_name]) \
#         .agg([list, 'count'])[english_col_name] \
#         .reset_index().rename(columns={
#             'list': ENGLISH_DEFS_COL_NAME,
#             'count': NUM_ENGLISH_DEFS_COL_NAME
#         })
#
#     return eng_kor_dict_dup_entries[eng_kor_dict_dup_entries[NUM_ENGLISH_DEFS_COL_NAME] > 1]

def add_col_with_count(_df, col_to_add_count, count_col_name):
    col_other_than_count = list(set(_df.columns).difference({col_to_add_count}))[0]

    num_occ_per_value = _df \
        .groupby(col_to_add_count) \
        .agg('count')[col_other_than_count] \
        .rename(count_col_name)

    return _df.join(num_occ_per_value, on=col_to_add_count)


def group_lang_df_by_parts(lang_df,
                           col_to_break_up,
                           func_for_parsing_col,
                           part_col_name,
                           col_sort_order_after_parts=None,
                           col_for_counting_num_defs=None,
                           func_to_call_after_split=None):

    if col_for_counting_num_defs is None:
        col_for_counting_num_defs = part_col_name

    if col_sort_order_after_parts is None:
        col_sort_order_after_parts = []

    col_with_list_of_parts_name = f'{col_to_break_up}_parts'
    num_parts_col_name = f'{col_to_break_up}_num_parts'
    rank_col_name = f'{part_col_name}_rank'
    rank_tuple_col_name = f'{part_col_name}_rank_tuple'

    lang_df_with_parts = add_col_with_parts(
        lang_df,
        col_with_list_of_parts_name,
        col_to_break_up,
        func_for_parsing_col)

    lang_df_expanded = lang_df_with_parts\
        .explode(col_with_list_of_parts_name).rename(columns={
            col_with_list_of_parts_name: part_col_name
        })

    if func_to_call_after_split is not None:
        lang_df_expanded = func_to_call_after_split(lang_df_expanded)

    lang_df_expanded = add_col_with_count(lang_df_expanded,
                                          col_for_counting_num_defs,
                                          num_parts_col_name)

    parts_in_multiple_words = lang_df_expanded[
        lang_df_expanded[num_parts_col_name] > 1]

    parts_in_multiple_words[num_parts_col_name] = \
        parts_in_multiple_words[num_parts_col_name].apply(lambda x: int(x))

    sort_order = [num_parts_col_name, part_col_name]
    sort_order.extend(col_sort_order_after_parts)

    parts_in_multiple_words[rank_tuple_col_name] = parts_in_multiple_words.apply(
        lambda row: (row[num_parts_col_name],
                     row[part_col_name]), axis=1)

    part_rank_df = parts_in_multiple_words[[rank_tuple_col_name]].drop_duplicates()
    part_rank_df[rank_col_name] = part_rank_df[rank_tuple_col_name].rank(method='min').apply(lambda x: int(x))
    part_rank_df = part_rank_df.set_index(rank_tuple_col_name)
    parts_in_multiple_words = parts_in_multiple_words.join(part_rank_df, on=rank_tuple_col_name)

    out_df = parts_in_multiple_words.sort_values(sort_order, ascending=False)
    return out_df
