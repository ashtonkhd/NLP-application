import numpy as np

# Constants
LOGIC_DICTIONARY = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "1 -", "NOT": "1 -",
    "(": "(", ")": ")"}

LOGIC_OPERATORS = ["&", "|"]

def _rewrite_query(query):
    split_query = query.split()

    for index in range(len(split_query)):
        if split_query[index] in list(LOGIC_DICTIONARY.keys()):
            split_query[index] = LOGIC_DICTIONARY[split_query[index]]

    return " ".join(split_query)

def _process_query_ranked(query, td_matrix, t2i):
    rewritten_query = _rewrite_query(query)
    
    try:
        # Check for logic operators, assume single term otherwise.
        if ("&" in rewritten_query) or ("|" in rewritten_query):
            terms_in_query = rewritten_query.split()
            
            doc_hits = None
            relation_to_previous = None
            first_time = True # The previous way just stopped working -M. Summanen

            for term in terms_in_query:
                if not(term in LOGIC_OPERATORS):
                    term_matrix = td_matrix[t2i[term]]

                    if first_time == True:
                        doc_hits = term_matrix
                        first_time = False

                    else:
                        new_doc_hits = []
                        # Apply logical functionality
                        match relation_to_previous:
                            case "AND":
                                for y, x in np.ndindex(term_matrix.shape):
                                    if (term_matrix[y, x] != 0) and (doc_hits[y, x] != 0):
                                        new_doc_hits.append(int(term_matrix[y, x] + doc_hits[y, x]))
                                    else:
                                        new_doc_hits.append(0)

                                doc_hits = np.matrix(new_doc_hits)

                            case "OR":
                                for y, x in np.ndindex(term_matrix.shape):
                                    if (term_matrix[y, x] != 0) or (doc_hits[y, x] != 0):
                                        new_doc_hits.append(int(term_matrix[y, x] + doc_hits[y, x]))

                                doc_hits = np.matrix(new_doc_hits)
                else:
                    match term:
                        case "&":
                            relation_to_previous = "AND"
                        case "|":
                            relation_to_previous = "OR"
        else:
            term = rewritten_query
            term_matrix = td_matrix[t2i[term]]
            doc_hits = term_matrix

        return doc_hits, True

    except KeyError as e:
        print(f"Term not found in any documents.")
        return None, False
    except SyntaxError:
        print(f"Invalid query syntax -> '{query}'")
        return None, False
    except Exception as e:
        print(f"Error processing query: {e}")
        return None, False
                

def _rank_hits(hit_matrix):
    ranked = []

    for y, x in np.ndindex(hit_matrix.shape):
        ranked.append((x, int(hit_matrix[y, x])))

    ranked.sort(key=lambda tup: tup[1], reverse=True)

    return ranked

def run_search_engine(matrix, cv, pep_numbers, model):
    t2i = cv.vocabulary_

    # The search engine runs indefinitely, unless break is used.
    while True:
        query = input("\nEnter your query (or type 'quit' to exit): ")

        if query.lower() == 'quit' or query == '':
            break

        match model:
            case "ranked":
                results, got_hits = _process_query_ranked(query, matrix, t2i)

                if (got_hits):
                    ranked_list = _rank_hits(results)

                    print("Results in:")
                    for i in range(5):
                        print(f"{pep_numbers[ranked_list[i][0]]}: {ranked_list[i][1]}")
        
