
def strip_whitespace_from_tuple_els(_tuple):
    return tuple([_el.strip() for _el in _tuple])


def refine_tuples(vocab_tuples):
    tuples_refined = [strip_whitespace_from_tuple_els(_tuple) for _tuple in vocab_tuples]
    return list(set(tuples_refined))