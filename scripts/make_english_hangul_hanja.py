import pandas as pd

kor_eng_tuples = pd.read_csv('output/korean_english_tuples.csv')
hangul_hanja_pairs = pd.read_csv('output/hanja_hangul_pairs.csv')

hangul_hanja_english_df = kor_eng_tuples.join(hangul_hanja_pairs.set_index('hangul_word'), on='Korean')

hangul_hanja_english_df.to_csv('output/enlish_hangul_hanja_tuples_naive.csv', index=False)

hangul_hanja_set = hangul_hanja_english_df[hangul_hanja_english_df['hanja_word'].apply(lambda x: str(x) != 'nan')]\
    .groupby('Korean').agg(list)['hanja_word'].reset_index()

hangul_hanja_pairs_to_check = hangul_hanja_set[hangul_hanja_set['hanja_word'].apply(lambda x: len(x) > 1)]

hangul_hanja_pairs_to_check.to_csv('output/english_hangul_hanja_tuples_to_check.csv', index=False)