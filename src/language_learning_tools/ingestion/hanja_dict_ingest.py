def hanja_dict_text_to_tuples(hanja_hungul_txt):
    hanja_hangul_lines = hanja_hungul_txt.split('\n')
    hanja_hangul_lines_to_use = [line for line in hanja_hangul_lines if not line.startswith('#')]
    hanja_hangul_pairs_raw = [tuple(line.split('\t')) for line in hanja_hangul_lines_to_use]
    return [pair for pair in hanja_hangul_pairs_raw if len(pair) == 2]
