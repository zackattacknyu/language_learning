from language_learning_tools.grouping.vocab_grouping import \
    get_hangul_parts, \
    group_lang_df_by_parts
import pandas as pd

INPUT_CSV_PATH = 'input_generated_files/english_hangul_hanja_tups_to_memorize.csv'
OUTPUT_CSV_PATH = 'output/tups_grouped_by_hanja.csv'
ENGLISH_COL_NAME = 'English_translation'
KOREAN_COL_NAME = 'hangul_word'
HANJA_COL_NAME = 'hanja_word_with_x'

HANJA_CHAR_COL_NAME = 'hanja_char'
NUM_WITH_HANJA_COL_NAME = 'num_with_hanja_char'

HANJA_PARTS_COL_NAME = 'hanja_parts'

eng_kor_df = pd.read_csv(INPUT_CSV_PATH)

eng_kor_df = eng_kor_df[eng_kor_df[HANJA_COL_NAME].apply(lambda x: 'X' not in x)]

hanja_chars_output_df = group_lang_df_by_parts(
    eng_kor_df,
    HANJA_COL_NAME,
    get_hangul_parts,
    HANJA_CHAR_COL_NAME,
    NUM_WITH_HANJA_COL_NAME,
    [HANJA_COL_NAME, KOREAN_COL_NAME, ENGLISH_COL_NAME])

hanja_chars_output_df.to_csv(OUTPUT_CSV_PATH, index=False)

