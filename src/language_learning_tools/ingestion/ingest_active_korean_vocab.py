from language_learning_tools.util.korean_util import is_word_all_hangul


def make_tuples_from_active_korean(active_korean_raw_data):
    active_korean_words = []
    for _line in active_korean_raw_data.split('\n'):
        for _word in _line.split(' '):
            active_korean_words.append(_word)

    active_korean_tuples = []

    #list alternates with korean string followed by strings saying the english definition
    current_korean_word = ''
    current_english_phrase = []
    for _word in active_korean_words:
        if len(_word) > 0 and is_word_all_hangul(_word):
            if len(current_korean_word) > 0:
                active_korean_tuples.append((current_korean_word, ' '.join(current_english_phrase)))
            current_korean_word = _word
            current_english_phrase = []
        else:
            current_english_phrase.append(_word)

    if len(current_korean_word) > 0:
        active_korean_tuples.append((current_korean_word, ' '.join(current_english_phrase)))

    return active_korean_tuples