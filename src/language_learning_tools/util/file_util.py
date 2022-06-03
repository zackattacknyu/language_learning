import pandas as pd


def tuples_to_csv(csv_file_path, tuples, csv_col_names):
    rename_dict = dict(list(enumerate(csv_col_names)))
    out_df = pd.DataFrame(tuples).rename(columns=rename_dict)
    out_df.to_csv(csv_file_path, index=False)


def text_file_to_tuples(text_file_path, text_str_to_vocab_tuples_func):
    with open(text_file_path, 'r') as f:
        raw_text_str = f.read()
    return text_str_to_vocab_tuples_func(raw_text_str)