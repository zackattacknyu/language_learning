from language_learning_tools.ingestion.ingest_ttmik_vocab import make_tuples_from_ttmik
from language_learning_tools.ingestion.ingest_active_korean_vocab import make_tuples_from_active_korean
from language_learning_tools.ingestion.raw_vocab_to_csv import text_files_to_single_csv


TEXT_FILE_FUNC_TUPLES = [
    ('input_external_files/ttmik_level_1.txt', make_tuples_from_ttmik),
    ('input_external_files/ttmik_level_2.txt', make_tuples_from_ttmik),
    ('input_external_files/active_korean_1_and_2.txt', make_tuples_from_active_korean)
]

OUTPUT_CSV_FILE = 'output/korean_english_tuples.csv'
OUTPUT_CSV_COL_NAMES = ['Korean', 'English']

text_files_to_single_csv(TEXT_FILE_FUNC_TUPLES, OUTPUT_CSV_FILE, OUTPUT_CSV_COL_NAMES)

