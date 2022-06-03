from language_learning_tools.grouping.vocab_grouping import \
    get_kor_english_duplicate_def_df, \
    get_kor_eng_df_with_english_parts, \
    explode_kor_eng_df_by_eng_parts, \
    NUM_DEFS_WITH_WORD_COL_NAME, \
    WORD_IN_ENGLISH_DEF_COL_NAME
import pandas as pd

INPUT_CSV_PATH = 'input_edited_files/korean_english_tuples_to_memorize.csv'
OUTPUT_CSV_PATH = 'output/pairs_grouped_by_english_def.csv'
ENGLISH_COL_NAME = 'English'
KOREAN_COL_NAME = 'Korean'

eng_kor_df = pd.read_csv(INPUT_CSV_PATH)

eng_kor_df_with_eng_parts = get_kor_eng_df_with_english_parts(
    eng_kor_df,
    ENGLISH_COL_NAME,
    KOREAN_COL_NAME)

eng_kor_df_dup_entries = get_kor_english_duplicate_def_df(eng_kor_df_with_eng_parts,
                                                          ENGLISH_COL_NAME,
                                                          KOREAN_COL_NAME)

assert eng_kor_df_dup_entries.shape[0] < 1

eng_kor_df_by_eng_parts_with_num_defs = explode_kor_eng_df_by_eng_parts(
    eng_kor_df_with_eng_parts, KOREAN_COL_NAME)

eng_words_in_multiple_defs = eng_kor_df_by_eng_parts_with_num_defs[
    eng_kor_df_by_eng_parts_with_num_defs[NUM_DEFS_WITH_WORD_COL_NAME] > 1]

eng_words_in_multiple_defs[NUM_DEFS_WITH_WORD_COL_NAME] = \
    eng_words_in_multiple_defs[NUM_DEFS_WITH_WORD_COL_NAME].apply(lambda x: int(x))

eng_words_in_multiple_defs\
    .sort_values([NUM_DEFS_WITH_WORD_COL_NAME,
                  WORD_IN_ENGLISH_DEF_COL_NAME,
                  KOREAN_COL_NAME,
                  ENGLISH_COL_NAME], ascending=False)\
    .to_csv(OUTPUT_CSV_PATH, index=False)

