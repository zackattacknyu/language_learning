import pandas as pd

ENGLISH_COL_NAME = 'English_translation'
KOREAN_COL_NAME = 'hangul_word'
HANJA_COL_NAME = 'hanja_word_with_x'

DEF_COLS = [ENGLISH_COL_NAME,
            KOREAN_COL_NAME,
            HANJA_COL_NAME]

HANJA_HANGUL_TUPLE = 'hangul_hanja_tuple'
HANJA_HANGUL_CHAR_TUPLE = 'hangul_hanja_char_tuple'

HANJA_CHAR_COL_NAME = 'hanja_char'

HANJA_PARTS_COL_NAME = 'hanja_parts'

ALL_TUPS_FILE = 'input_generated_files/english_hangul_hanja_tups_to_memorize.csv'
TUPS_GRPED_BY_HANJA_HANGUL = 'output/tups_grouped_by_hangul_hanja.csv'
TUPS_GRPED_BY_ENGLISH_DF = 'output/tups_grouped_by_english_def.csv'

tups_df = pd.read_csv(ALL_TUPS_FILE)
tups_hanja_group = pd.read_csv(TUPS_GRPED_BY_HANJA_HANGUL)
tups_english_group = pd.read_csv(TUPS_GRPED_BY_ENGLISH_DF)


existing_defs_df = pd.concat([
    tups_hanja_group[DEF_COLS],
    tups_english_group[DEF_COLS]
]).drop_duplicates()


existing_defs_df['def_already_exists'] = True
tups_with_existence = tups_df.join(existing_defs_df.set_index(DEF_COLS), on=DEF_COLS)


tups_not_covered = tups_with_existence[tups_with_existence['def_already_exists'].apply(lambda x: x is not True)]

tups_not_covered[DEF_COLS].sort_values(KOREAN_COL_NAME).to_csv('output/tups_with_no_group.csv')


