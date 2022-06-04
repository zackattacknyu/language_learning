import pandas as pd

INPUT_CSV_PATH = 'input_edited_files/TEMP_english_hangul_hanja_tups_fixed_3.csv'
OUTPUT_CSV_PATH = 'output/english_hangul_hanja_tups_to_memorize.csv'


tups_to_memorize = pd.read_csv(INPUT_CSV_PATH)

hangul_hanja_pairs = tups_to_memorize[tups_to_memorize['hanja_word_with_x']\
    .apply(lambda x: 'X' not in x)]\
    [['hangul_word', 'hanja_word_with_x']]\
    .to_dict(orient='records')

hangul_to_hanja_dict = {
    _pair['hangul_word']: _pair['hanja_word_with_x']
    for _pair in hangul_hanja_pairs
}


def get_hanja_for_hangul(hangul_word):
    if hangul_word in hangul_to_hanja_dict:
        return hangul_to_hanja_dict[hangul_word]
    elif hangul_word.endswith('하다'):
        hangul_wo_hada = hangul_word[:-2]
        if hangul_wo_hada in hangul_to_hanja_dict:
            return f'{hangul_to_hanja_dict[hangul_wo_hada]}하다'
    return 'X'


output_df = tups_to_memorize[['hangul_word', 'English_translation']]
output_df['hanja_word_with_x'] = output_df['hangul_word'].apply(get_hanja_for_hangul)

output_df.to_csv(OUTPUT_CSV_PATH, index=False)
