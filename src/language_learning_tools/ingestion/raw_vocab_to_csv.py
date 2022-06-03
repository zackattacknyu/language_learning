from language_learning_tools.util.file_util import tuples_to_csv, text_file_to_tuples
from language_learning_tools.util.data_transforms import refine_tuples


def text_files_to_single_csv(text_file_func_tuples, output_csv_path, csv_col_names):
    raw_tuples = []
    for text_file_path, text_file_to_tuple_func in text_file_func_tuples:
        raw_tuples.extend(text_file_to_tuples(text_file_path, text_file_to_tuple_func))
    output_tuples = refine_tuples(raw_tuples)
    tuples_to_csv(output_csv_path, output_tuples, csv_col_names)
