import numpy as np

from . import query_processing as quproc

def _boolean_convert(ranked):
    _tmp = ranked
    _new_ranked = []

    for tup in range(len(_tmp)):
        if _tmp[tup][1] > 0:
            _new_ranked.append((_tmp[tup][0], 1))
        else:
            _new_ranked.append((_tmp[tup][0], 0))

    return _new_ranked

def _rank_hits(hit_matrix, mode):
    ranked = []
    _mode_ranked = []

    for y, x in np.ndindex(hit_matrix.shape):
        ranked.append((x, int(hit_matrix[y, x])))

    match mode:
        case "boolean":
            # Replaces ranked occurrences with either 1 (appears) or 0 (doesn't appear)
            _mode_ranked = _boolean_convert(ranked)
        case "ranked":
            _mode_ranked = ranked

    _mode_ranked.sort(key=lambda tup: tup[1], reverse=True)

    return _mode_ranked

    
def run_search_engine(matrix, cv, pep_numbers, model, query, show=5):
    t2i = cv.vocabulary_
    _return_documents = []
    
    match model:
        case "ranked":
            results, got_hits = quproc.process_query(query, matrix, t2i)

            if got_hits:
                ranked_list = _rank_hits(results, "ranked")

                for i in range(show):
                    if not(ranked_list[i][1] == 0):
                        _return_documents.append((f"{pep_numbers[ranked_list[i][0]]}", int(ranked_list[i][1])))

        case "boolean":
            results, got_hits = quproc.process_query(query, matrix, t2i)

            if got_hits:
                # Some of the results are zero, so this makes
                # all the 1s go before them.
                result_list = _rank_hits(results, "boolean")

                for i in range(show):
                    if not(result_list[i][1] == 0):
                        _return_documents.append(pep_numbers[result_list[i][0]])

    return _return_documents
