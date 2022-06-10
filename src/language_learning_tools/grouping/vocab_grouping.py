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


def get_hanja_parts(x):
    hanja_wo_hada = x[:-2] if x.endswith('하다') else x
    return tuple(hanja_wo_hada)


def get_hangul_parts(x):
    hangul_wo_hada = x[:-2] if x.endswith('하다') else x
    hangul_wo_hada = x[:-1] if hangul_wo_hada.endswith('다') else hangul_wo_hada
    return tuple(hangul_wo_hada)


def get_hangul_hanja_tuples(x):
    hangul_chars = get_hangul_parts(x[0])
    hanja_chars = get_hanja_parts(x[1])
    if 'X' in hanja_chars:
        return tuple([(hangul_ch, 'X') for hangul_ch in hangul_chars])
    else:
        return tuple(zip(hangul_chars, hanja_chars))


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


def explode_df_by_list_col(lang_df,
                           list_col,
                           col_with_parts_name,
                           num_parts_col_name):
    lang_df_with_parts = lang_df \
        .explode(list_col).rename(columns={
            list_col: col_with_parts_name
        })

    ref_cols = set(lang_df_with_parts.columns).difference({col_with_parts_name})
    ref_col = list(ref_cols)[0]

    num_defs_per_word = lang_df_with_parts \
        .groupby(col_with_parts_name) \
        .agg('count')[ref_col] \
        .rename(num_parts_col_name)

    return lang_df_with_parts \
        .join(num_defs_per_word, on=col_with_parts_name)


def group_lang_df_by_parts(lang_df,
                           col_to_break_up,
                           func_for_parsing_col,
                           part_col_name,
                           col_sort_output_order_after_parts=[]):

    col_with_list_of_parts_name = f'{col_to_break_up}_parts'
    num_parts_col_name = f'{col_to_break_up}_num_parts'

    lang_df_with_parts = add_col_with_parts(
        lang_df,
        col_with_list_of_parts_name,
        col_to_break_up,
        func_for_parsing_col)

    lang_df_expanded = explode_df_by_list_col(
        lang_df_with_parts,
        col_with_list_of_parts_name,
        part_col_name,
        num_parts_col_name)

    parts_in_multiple_words = lang_df_expanded[
        lang_df_expanded[num_parts_col_name] > 1]

    parts_in_multiple_words[num_parts_col_name] = \
        parts_in_multiple_words[num_parts_col_name].apply(lambda x: int(x))

    sort_order = [num_parts_col_name, part_col_name]
    sort_order.extend(col_sort_output_order_after_parts)

    output_order = [part_col_name]
    output_order.extend(col_sort_output_order_after_parts)

    out_df = parts_in_multiple_words.sort_values(sort_order, ascending=False)
    return out_df[output_order]