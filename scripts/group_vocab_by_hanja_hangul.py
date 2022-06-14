from language_learning_tools.grouping.vocab_grouping import \
    get_hangul_substrs, \
    group_lang_df_by_parts, \
    get_hangul_hanja_tuples
import pandas as pd

INPUT_CSV_PATH = 'input_generated_files/english_hangul_hanja_tups_to_memorize.csv'
OUTPUT_CSV_PATH = 'output/tups_grouped_by_hangul_hanja.csv'
OUTPUT_CSV_PATH_2 = 'output/tups_grouped_by_hangul.csv'
ENGLISH_COL_NAME = 'English_translation'
KOREAN_COL_NAME = 'hangul_word'
HANJA_COL_NAME = 'hanja_word_with_x'

HANJA_HANGUL_TUPLE = 'hangul_hanja_tuple'
HANJA_HANGUL_CHAR_TUPLE = 'hangul_hanja_char_tuple'

HANJA_PARTS_COL_NAME = 'hanja_parts'

HANGUL_SEQ = 'hangul_seq'
HANJA_SEQ = 'hanja_seq'

eng_kor_df = pd.read_csv(INPUT_CSV_PATH)
eng_kor_df[HANJA_HANGUL_TUPLE] = eng_kor_df.apply(lambda row: (row[KOREAN_COL_NAME], row[HANJA_COL_NAME]), axis=1)


def add_hanja_hangul_seqs(_df):
    _df[HANGUL_SEQ] = _df[HANJA_HANGUL_CHAR_TUPLE].apply(lambda x: x[0])
    _df[HANJA_SEQ] = _df[HANJA_HANGUL_CHAR_TUPLE].apply(lambda x: x[1])
    return _df


hanja_chars_output_df = group_lang_df_by_parts(
    eng_kor_df,
    HANJA_HANGUL_TUPLE,
    get_hangul_hanja_tuples,
    HANJA_HANGUL_CHAR_TUPLE,
    [KOREAN_COL_NAME, HANJA_COL_NAME, ENGLISH_COL_NAME],
    func_to_call_after_split=add_hanja_hangul_seqs)

hangul_chars_output_df = group_lang_df_by_parts(
    eng_kor_df,
    HANJA_HANGUL_TUPLE,
    get_hangul_hanja_tuples,
    HANJA_HANGUL_CHAR_TUPLE,
    [KOREAN_COL_NAME, HANJA_COL_NAME, ENGLISH_COL_NAME],
    col_for_counting_num_defs=HANGUL_SEQ,
    func_to_call_after_split=add_hanja_hangul_seqs)


hanja_chars_output_df = add_hanja_hangul_seqs(hanja_chars_output_df)
hanja_chars_output_df.to_csv(OUTPUT_CSV_PATH, index=False)

hangul_chars_output_df = add_hanja_hangul_seqs(hangul_chars_output_df)
hangul_chars_output_df.to_csv(OUTPUT_CSV_PATH_2, index=False)
