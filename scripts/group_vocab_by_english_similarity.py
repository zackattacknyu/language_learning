from language_learning_tools.grouping.vocab_grouping import \
    get_non_stop_words, \
    group_lang_df_by_parts
import pandas as pd

INPUT_CSV_PATH = 'input_generated_files/english_hangul_hanja_tups_to_memorize.csv'
OUTPUT_CSV_PATH = 'output/tups_grouped_by_english_def.csv'
ENGLISH_COL_NAME = 'English_translation'
KOREAN_COL_NAME = 'hangul_word'
HANJA_COL_NAME = 'hanja_word_with_x'

ENGLISH_PARTS_COL_NAME = 'English_def_parts'
ENGLISH_DEFS_COL_NAME = 'English_definitions'
NUM_ENGLISH_DEFS_COL_NAME = 'num_English_definitions'
WORD_IN_ENGLISH_DEF_COL_NAME = 'word_in_English_def'

eng_kor_df = pd.read_csv(INPUT_CSV_PATH)

output_df = group_lang_df_by_parts(
    eng_kor_df,
    ENGLISH_COL_NAME,
    get_non_stop_words,
    WORD_IN_ENGLISH_DEF_COL_NAME,
    [KOREAN_COL_NAME, HANJA_COL_NAME, ENGLISH_COL_NAME]
)

output_df.to_csv(OUTPUT_CSV_PATH, index=False)

