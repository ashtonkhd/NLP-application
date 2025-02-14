import re
import numpy as np
import requests
import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup

# Operator replacements
d = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "1 -", "NOT": "1 -",
    "(": "(", ")": ")"
}

LOGICAL_OPERATORS = ["&", "|"]

PEP_URL: str = "https://peps.python.org/"
PEP_PATTERN = "pep-[0-9]+"

def process_pep_data(pep_entries):
    """Processes raw pep_data into usable data

    Takes the pep entries, uses requests to get their content and then
    uses BeautifulSoup to take all the text from the paragraphs. This is
    then combined into a single string and finally added as a dictionary
    entry.

    :param pep_entries: list of pep URLs

    :returns: a dictionary of pep-numbers with their content
    """
    total_entries = len(pep_entries)
    current_entry = 1

    proper_pep_data = {}
    
    for entry in pep_entries:
        print(f"[{(current_entry/total_entries)*100:.2f}%] prosessing {entry[0:-1]}")
        entry_link = f"{PEP_URL}{entry}"
        entry_request = requests.get(entry_link)
        entry_data = BeautifulSoup(entry_request.content, 'html.parser')

        para_text = []
        
        for para in entry_data.find_all('p'):
            para_text.append(para.text)


        proper_pep_data.update({entry[0:-1]: " ".join(para_text)})
        current_entry += 1

    return proper_pep_data

def get_pep_data():
    """Gets peps from pep 0 (pep index)

    Uses requests to download all pep links from PEP_URL (found via regex
    matching with PEP_PATTERN). Then uses :func: `process_pep_data()` to
    turn them into a dictionary of usable data.

    :returns: a dictionary of processed pep_data.
    
    """
    pep_index = requests.get(PEP_URL)
    html_data = BeautifulSoup(pep_index.content, 'html.parser')

    pep_entries = []
    
    for link in html_data.find_all('a', href=True):
        if re.search(PEP_PATTERN, link['href']) != None:
            pep_number = link['href']
            
            if '#' in pep_number:
                pass
            else:
                if pep_number in pep_entries:
                    pass
                else:
                    pep_entries.append(pep_number)

    processed = process_pep_data(pep_entries)

    return processed

def save_pep_data(pep_data):
    with open("./pep_data.json", "w", encoding='utf-8') as target:
        json.dump(pep_data, target)

    

# Load docs
def load_documents_from_files(file_path):
    """Reads the data from document files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as source:
            documents = json.load(source)
    #for file_path in file_paths:
        #try:
            #with open(file_path, 'r', encoding='utf-8') as f:
                #content = f.read()
                #articles = content.split('\n</article>\n')  # Assuming each article is separated by </article>
                #documents.extend([article.strip() for article in articles if article.strip()])
    except Exception as e:
        print(f"Error reading the file {file_path}: {e}")
        
    return documents

# Initialize 
def initialize_search_engine(documents):
    cv = CountVectorizer(lowercase=True, binary=False)
    _matrix = cv.fit_transform(documents).T.todense()
    #sparse_matrix = cv.fit_transform(documents)
    #td_matrix = sparse_matrix.T  # T-D matrix
    #terms = cv.get_feature_names_out()
    #t2i = cv.vocabulary_  # T-to-I dictionary
    return _matrix, cv

# Rewrite query to Boo
def rewrite_token(t):
    return d.get(t, f'td_matrix[t2i["{t}"]]')  # Replace operators or map terms

def rewrite_query(query):
    split_query = query.split()

    for index in range(len(split_query)):
        if split_query[index] in list(d.keys()):
            split_query[index] = d[split_query[index]]

    return " ".join(split_query)
            
    #return " ".join(rewrite_token(t) for t in query.split())

# Process and evaluate the query
def process_query(query, td_matrix, t2i, documents):
    rewritten_query = rewrite_query(query)
    
    try:

        """
        I have commented out this code for testing purposes.
        -- M. Summanen
        """
        # TODO: Complete query functionality

        # Evaluate
        if ("&" in rewritten_query) or ("|" in rewritten_query):
            terms_in_query = rewritten_query.split()
            doc_hits = None

            relation_to_previous = None
            
            for term in terms_in_query:
                if not(term in LOGICAL_OPERATORS):
                    term_matrix = td_matrix[t2i[term]]

                    # Apply AND or OR 
                    if doc_hits is None:
                        doc_hits = term_matrix
                    else:
                        new_doc_hits = []
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


        else:  # If no AND or OR, process as single term
            term = rewritten_query
            term_matrix = td_matrix[t2i[term]]
            print(term_matrix)

        # Check
        #if len(doc_hits_list) == 0:
            #print(f"\nNo results for query: {query}")
            #return

        # Print 
        #print(f"\nFound {len(doc_hits_list)} matching documents:")
        #for i, doc_idx in enumerate(doc_hits_list[:max_results]):
            #doc = documents[doc_idx]
            #print(f"\nMatching doc #{i + 1}:")
            #print(doc[:max_length] + "..." if len(doc) > max_length else doc)

    except KeyError as e:
        print(f"Term '{e.args[0]}' not found in documents.")
    except SyntaxError:
        print(f"Error: Invalid query syntax -> '{query}'")
    except Exception as e:
        print(f"Error processing query: {e}")

# Run SE in e loop
def run_search_engine(matrix, cv, pep_numbers):
    t2i = cv.vocabulary_
    while True:
        query = input("\nEnter your query (or type 'quit' to exit): ")
        if query.lower() == 'quit' or query == '':
            break
        process_query(query, matrix, t2i, pep_numbers)

def main() -> None:
    if not(os.path.exists("./pep_data.json")):
           pep_data = get_pep_data()
           save_pep_data(pep_data)

    # Changed to a single filepath since only one pep_data file now
    # -- M. Summanen
    file_path = "./pep_data.json"

    # Load docs
    documents = load_documents_from_files(file_path)
    pep_numbers = list(documents.keys())
    pep_contents = list(documents.values())

    pep_matrix = None
    
    if not(len(pep_contents) == 0):
        # Initialize
        pep_matrix, vectorizer = initialize_search_engine(pep_contents)
        run_search_engine(pep_matrix, vectorizer, pep_numbers)

    else:
        print("Unable to load pep_data.json. Exiting...")
        exit()
    
if __name__ == "__main__":
    main()
