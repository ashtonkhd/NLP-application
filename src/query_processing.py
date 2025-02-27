import numpy as np

LOGIC_DICTIONARY = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "!", "NOT": "!",
    "(": "BSRT", ")": "BEND"}

LOGIC_WORDS = list(LOGIC_DICTIONARY.keys())
LOGIC_OPERATORS = list(set(LOGIC_DICTIONARY.values()))


def _rewrite_query(query):
    _tmp_split = query.split()

    for _index in range(len(_tmp_split)):
        if _tmp_split[_index] in LOGIC_WORDS:
            _tmp_split[_index] = LOGIC_DICTIONARY[_tmp_split[_index]]
        else:
            _tmp_split[_index] = _tmp_split[_index].lower()

    return " ".join(_tmp_split)

def _get_new_hits(term_matrix, doc_hits, relation_to_previous, not_effect):
    """Get new hits for the query.

    :param term_matrix: The occurrence matrix of the current term.
    :param doc_hits: The occurrence matrices for all previous terms
    :param relation_to_previous: The logic-relation to between term_matrix and doc_hits
    :param not_effect: NOT operator. Reverses occurrences for term_matrix

    :returns: new doc_hits matrix.
    """
    _tmp = []
    match relation_to_previous:
        case "AND":
            for y, x in np.ndindex(term_matrix.shape):
                if not_effect:
                    if not(term_matrix[y, x] != 0) and (doc_hits[y,x] != 0):
                        _tmp.append(int(term_matrix[y, x] + doc_hits[y, x]))

                    else:
                        _tmp.append(0)

                else:
                    if (term_matrix[y, x] != 0) and (doc_hits[y,x] != 0):
                        _tmp.append(int(term_matrix[y, x] + doc_hits[y, x]))
                    else:
                        _tmp.append(0)

        case "OR":
            for y,x in np.ndindex(term_matrix.shape):
                if not_effect:
                    if not(term_matrix[y, x] != 0) or (doc_hits[y,x] != 0):
                        _tmp.append(int(term_matrix[y, x] + doc_hits[y, x]))

                else:
                    if (term_matrix[y,x] != 0) or (doc_hits[y,x] != 0):
                        _tmp.append(int(term_matrix[y, x] + doc_hits[y, x]))

        case _:
            raise SyntaxError

    if not_effect:
        not_effect = False

    return np.matrix(_tmp), not_effect

def _get_reverse_hits(term_matrix):
    for y,x in np.ndindex(term_matrix.shape):
        if term_matrix[y,x] > 0:
            term_matrix[y, x] = 0
        else:
            term_matrix[y, x] = 1

    return term_matrix

def process_query(query, td_matrix, t2i):
    rewritten_query = _rewrite_query(query)

    try:
        # If logic operators are not present, process as singular term.
        if any(operator in rewritten_query for operator in LOGIC_OPERATORS):
            terms_in_query = rewritten_query.split()

            doc_hits = None
            relation_to_previous = None
            not_effect = None # Whether to take reserve value (not-operator)
            first_time = True # For some reason going by doc_hits = None, stopped working.

            for term in terms_in_query:
                if not(term in LOGIC_OPERATORS):
                    term_matrix = td_matrix[t2i[term]]

                    if first_time:
                        if not not_effect:
                            doc_hits = term_matrix
                            first_time = False
                        else:
                            doc_hits = _get_reverse_hits(term_matrix)
                            first_time = False

                    else:
                        
                        doc_hits, not_effect = _get_new_hits(term_matrix, doc_hits, relation_to_previous, not_effect)

                else:
                    match term:
                        case "&":
                            relation_to_previous = "AND"
                        case "|":
                            relation_to_previous = "OR"
                        case "!":
                            not_effect = True

        else:
            term = rewritten_query.split()[0]
            doc_hits = td_matrix[t2i[term]]

        return doc_hits, True

    except KeyError as e:
        print(f"Term: '{e} not found in any documents.")
        return None, False
    except SyntaxError:
        print(f"Incorrect query syntax -> '{query}'")
        return None, False
    except Exception as e:
        print(f"Unhandled exception: {e}")
