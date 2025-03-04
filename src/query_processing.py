import numpy as np

LOGIC_DICTIONARY = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "!", "NOT": "!",
    "(": "BSRT", ")": "BEND"}

LOGIC_WORDS = list(LOGIC_DICTIONARY.keys())
LOGIC_OPERATORS = list(set(LOGIC_DICTIONARY.values()))


def _rewrite_query(query):
    """Rewrites search-query

    Replaces logic operators with variants from LOGIC_DICTIONARY. Makes
    other words lowercase. If multiple words are found with no logic
    operators, inserts "&" between them.

    :param query: the search query to rewrite

    :returns: rewritten search query.
    """
    _tmp_split = query.split()

    for _index in range(len(_tmp_split)):
        if _tmp_split[_index] in LOGIC_WORDS:
            _tmp_split[_index] = LOGIC_DICTIONARY[_tmp_split[_index]]
        else:
            _tmp_split[_index] = _tmp_split[_index].lower()
            
    if not(any(operator in _tmp_split for operator in LOGIC_OPERATORS)) \
    and (len(_tmp_split) > 1):
        _tmp = list(enumerate(_tmp_split))
        _needed = [1]
        
        for i in range(len(_tmp)):
            if (_tmp[i][0] % 2 == 0) and not(_tmp[i][0] == 0):
                _needed.append(_tmp[i][0])
        
        _extra_i = 0
        for i in range(len(_needed)):
            _tmp_split.insert(_needed[i] + _extra_i, "&")
            _extra_i += 1

    return " ".join(_tmp_split)

def _get_new_hits(term_matrix, doc_hits, relation_to_previous, not_effect):
    """Get new hits for the query.

    :param term_matrix: The occurrence matrix of the current term.
    :param doc_hits: The occurrence matrices for all previous terms
    :param relation_to_previous: The logic-relation to between
    term_matrix and doc_hits
    :param not_effect: NOT operator. Reverses occurrences for
    term_matrix

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
    """Function for implementing NOT-operator

    Imitates NOT by turning value into 0, if appears, and 1, if absent.

    :param term_matrix: the term matrix on which to use NOT.

    :returns: term_matrix with NOT applied
    """
    for y,x in np.ndindex(term_matrix.shape):
        if term_matrix[y,x] > 0:
            term_matrix[y, x] = 0
        else:
            term_matrix[y, x] = 1

    return term_matrix

def process_query(query, td_matrix, t2i):
    """Main function for processing queries

    Processes a given query, according ot specifics about it such as
    logic operators and amount of terms.

    :param query: the query to process
    :param td_matrix: term matrix for the dataset
    :param t2i: dictionary for converting terms to indices in td_matrix.

    :returns: results for the query as matrix.
    """
    rewritten_query = _rewrite_query(query)

    try:
        # If logic operators are not present, process as singular term.
        if any(operator in rewritten_query for operator in LOGIC_OPERATORS):
            terms_in_query = rewritten_query.split()

            doc_hits = None
            relation_to_previous = "AND"
            not_effect = None
            first_time = True

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
