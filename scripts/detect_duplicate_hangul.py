import pandas as pd


english_hangul_hanja = pd.read_csv('input_edited_files/english_hangul_hanja_tuples__no_repeat_hangul_hanja.csv')

tups_by_hangul_hanja = english_hangul_hanja\
    .groupby(['Korean', 'hanja_word'])\
    .agg('count')['English']\
    .reset_index().rename(columns = {
        'English': 'num_pairs'
    })

assert tups_by_hangul_hanja['num_pairs'].max() < 2


