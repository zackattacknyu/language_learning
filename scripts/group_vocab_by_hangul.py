from language_learning_tools.grouping.vocab_grouping import \
    get_hangul_parts, \
    group_lang_df_by_parts
import pandas as pd

INPUT_CSV_PATH = 'input_generated_files/english_hangul_hanja_tups_to_memorize.csv'
OUTPUT_CSV_PATH = 'output/tups_grouped_by_hangul.csv'
ENGLISH_COL_NAME = 'English_translation'
KOREAN_COL_NAME = 'hangul_word'
HANJA_COL_NAME = 'hanja_word_with_x'

HANGUL_CHAR_COL_NAME = 'hangul_char'
NUM_WITH_HANGUL_COL_NAME = 'num_with_hangul_char'

eng_kor_df = pd.read_csv(INPUT_CSV_PATH)

hanja_chars_output_df = group_lang_df_by_parts(
    eng_kor_df,
    KOREAN_COL_NAME,
    get_hangul_parts,
    HANGUL_CHAR_COL_NAME,
    [KOREAN_COL_NAME, HANJA_COL_NAME, ENGLISH_COL_NAME])

hanja_chars_output_df.to_csv(OUTPUT_CSV_PATH, index=False)

