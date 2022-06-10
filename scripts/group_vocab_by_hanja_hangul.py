from language_learning_tools.grouping.vocab_grouping import \
    get_hangul_parts, \
    group_lang_df_by_parts, \
    get_hangul_hanja_tuples
import pandas as pd

INPUT_CSV_PATH = 'input_generated_files/english_hangul_hanja_tups_to_memorize.csv'
OUTPUT_CSV_PATH = 'output/tups_grouped_by_hangul_hanja.csv'
ENGLISH_COL_NAME = 'English_translation'
KOREAN_COL_NAME = 'hangul_word'
HANJA_COL_NAME = 'hanja_word_with_x'

HANJA_HANGUL_TUPLE = 'hangul_hanja_tuple'
HANJA_HANGUL_CHAR_TUPLE = 'hangul_hanja_char_tuple'

HANJA_CHAR_COL_NAME = 'hanja_char'

HANJA_PARTS_COL_NAME = 'hanja_parts'

eng_kor_df = pd.read_csv(INPUT_CSV_PATH)

eng_kor_df[HANJA_HANGUL_TUPLE] = eng_kor_df.apply(lambda row: (row[KOREAN_COL_NAME], row[HANJA_COL_NAME]), axis=1)

hanja_chars_output_df = group_lang_df_by_parts(
    eng_kor_df,
    HANJA_HANGUL_TUPLE,
    get_hangul_hanja_tuples,
    HANJA_HANGUL_CHAR_TUPLE,
    [KOREAN_COL_NAME, HANJA_COL_NAME, ENGLISH_COL_NAME])

hanja_chars_output_df['hangul_char'] = hanja_chars_output_df['hangul_hanja_char_tuple'].apply(lambda x: x[0])
hanja_chars_output_df['hanja_char'] = hanja_chars_output_df['hangul_hanja_char_tuple'].apply(lambda x: x[1])

hangul_hanja_rank = hanja_chars_output_df[['hangul_hanja_char_tuple']]\
    .drop_duplicates()\
    .reset_index()\
    .reset_index()[['level_0', 'hangul_hanja_char_tuple']].rename(columns={
        'level_0': 'tuple_rank'
    }).set_index('hangul_hanja_char_tuple')

hanja_chars_output_df = hanja_chars_output_df.join(hangul_hanja_rank, on='hangul_hanja_char_tuple')

hangul_hanja_out_df = hanja_chars_output_df[
    ['hangul_char',
     'hanja_char',
     KOREAN_COL_NAME,
     HANJA_COL_NAME,
     ENGLISH_COL_NAME,
     'tuple_rank']
]

hangul_hanja_out_df.to_csv(OUTPUT_CSV_PATH, index=False)

