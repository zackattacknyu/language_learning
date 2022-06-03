import pandas as pd

from language_learning_tools.grouping.vocab_grouping import \
    get_kor_english_duplicate_def_df, \
    get_kor_eng_df_with_english_parts

eng_kor_df = pd.read_csv('input_edited_files/korean_english_tuples_to_memorize.csv')

eng_kor_df_with_eng_parts = get_kor_eng_df_with_english_parts(eng_kor_df, 'English', 'Korean')

eng_kor_df_dup_entries = get_kor_english_duplicate_def_df(eng_kor_df_with_eng_parts, 'English', 'Korean')

eng_kor_df_dup_entries.to_csv('output/duplicate_korean_english_tuples.csv')
