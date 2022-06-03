from language_learning_tools.ingestion.raw_vocab_to_csv import text_files_to_single_csv
from language_learning_tools.ingestion.hanja_dict_ingest import hanja_dict_text_to_tuples

text_files_to_single_csv([('input_external_files/hanja-0.0.7/dic4.txt', hanja_dict_text_to_tuples)],
                         'output/hanja_hangul_pairs.csv',
                         ['hanja_word', 'hangul_word'])
