import re

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
    'do'
}
SPECIAL_PHRASES = [
    ('when modifying a counting unit that follows', 'when_modifying_a_counting_unit_that_follows'),
    ('counting unit', 'counting_unit')
]

ENGLISH_PARTS_COL_NAME = 'English_def_parts'
ENGLISH_DEFS_COL_NAME = 'English_definitions'
NUM_ENGLISH_DEFS_COL_NAME = 'num_English_definitions'
WORD_IN_ENGLISH_DEF_COL_NAME = 'word_in_English_def'
NUM_DEFS_WITH_WORD_COL_NAME = 'num_definitions_with_word'


def get_non_stop_words(x):
    x_no_punct = re.sub('[()/|,]', ' ', x)
    for orig_phrase, new_phrase in SPECIAL_PHRASES:
        x_no_punct = x_no_punct.replace(orig_phrase, new_phrase)
    words = x_no_punct.split(' ')
    non_stop_words = [_word for _word in words if len(_word) > 0 and _word not in STOP_WORDS]
    non_stop_words_out = list(set(non_stop_words))
    non_stop_words_out.sort()
    return tuple(non_stop_words_out)


def get_kor_eng_df_with_english_parts(kor_eng_tuples_df, english_col_name, korean_col_name):
    kor_eng_tuples_df[ENGLISH_PARTS_COL_NAME] = kor_eng_tuples_df[english_col_name].apply(get_non_stop_words)
    kor_eng_tuples_df = kor_eng_tuples_df.drop_duplicates()
    return kor_eng_tuples_df


def get_kor_english_duplicate_def_df(kor_eng_tuples_df,
                                     english_col_name,
                                     korean_col_name,
                                     english_parts_col_name=ENGLISH_PARTS_COL_NAME):
    eng_kor_dict_dup_entries = kor_eng_tuples_df \
        .groupby([korean_col_name, english_parts_col_name]) \
        .agg([list, 'count'])[english_col_name] \
        .reset_index().rename(columns={
            'list': ENGLISH_DEFS_COL_NAME,
            'count': NUM_ENGLISH_DEFS_COL_NAME
        })

    return eng_kor_dict_dup_entries[eng_kor_dict_dup_entries[NUM_ENGLISH_DEFS_COL_NAME] > 1]


def explode_kor_eng_df_by_eng_parts(kor_eng_df,
                                    korean_col_name,
                                    english_parts_col_name=ENGLISH_PARTS_COL_NAME):
    eng_kor_df_by_eng_parts = kor_eng_df \
        .explode(english_parts_col_name).rename(columns={
            english_parts_col_name: WORD_IN_ENGLISH_DEF_COL_NAME
        })

    num_defs_per_word = eng_kor_df_by_eng_parts \
        .groupby(WORD_IN_ENGLISH_DEF_COL_NAME) \
        .agg('count')[korean_col_name] \
        .rename(NUM_DEFS_WITH_WORD_COL_NAME)

    return eng_kor_df_by_eng_parts \
        .join(num_defs_per_word, on=WORD_IN_ENGLISH_DEF_COL_NAME)

