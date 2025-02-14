import re
import numpy as np
import requests
import json
import os
from sklearn.feature_extraction.text import CountVectorizer

# Operator replacements
d = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "1 -", "NOT": "1 -",
    "(": "(", ")": ")"
}

PEP_URL: str = "https://peps.python.org/"
PEP_PATTERN = "pep-[0-9]+"

def process_pep_data(pep_entries):
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
    cv = CountVectorizer(lowercase=True, binary=True)  
    sparse_matrix = cv.fit_transform(documents)
    td_matrix = sparse_matrix.T  # T-D matrix
    terms = cv.get_feature_names_out()
    t2i = cv.vocabulary_  # T-to-I dictionary
    return td_matrix, terms, t2i, cv, sparse_matrix

# Rewrite query to Boo
def rewrite_token(t):
    return d.get(t, f'td_matrix[t2i["{t}"]]')  # Replace operators or map terms

def rewrite_query(query):
    return " ".join(rewrite_token(t) for t in query.split())

# Process and evaluate the query
def process_query(query, td_matrix, t2i, documents):
    rewritten_query = rewrite_query(query)
    
    try:
        # Evaluate 
        # Manually log op
        if "AND" in rewritten_query or "or" in rewritten_query:  
            terms_in_query = rewritten_query.split()  # Split 
            doc_hits = None  # Initialize

            for term in terms_in_query:
                if term not in ["AND", "OR"]:
                    term_matrix = td_matrix[t2i.get(term, -1)]  
                    term_matrix = term_matrix.toarray()  
                    term_hits = term_matrix > 0  

                    # Apply AND or OR 
                    if doc_hits is None:
                        doc_hits = term_hits
                    elif "AND" in terms_in_query:
                        doc_hits = np.logical_and(doc_hits, term_hits)
                    elif "OR" in terms_in_query:
                        doc_hits = np.logical_or(doc_hits, term_hits)

            # Get indices
            doc_hits_list = np.where(doc_hits)[0]  # Indices of documents that match the query

        else:  # If no AND or OR, process as single term
            term_hits = td_matrix[t2i.get(rewritten_query, -1)].toarray() > 0
            doc_hits_list = np.where(term_hits)[0]

        # Check
        if len(doc_hits_list) == 0:
            print(f"\nNo results for query: {query}")
            return

        # Print 
        print(f"\nFound {len(doc_hits_list)} matching documents:")
        for i, doc_idx in enumerate(doc_hits_list[:max_results]):
            doc = documents[doc_idx]
            print(f"\nMatching doc #{i + 1}:")
            print(doc[:max_length] + "..." if len(doc) > max_length else doc)

    except KeyError as e:
        print(f"Term '{e.args[0]}' not found in documents.")
    except SyntaxError:
        print(f"Error: Invalid query syntax -> '{query}'")
    except Exception as e:
        print(f"Error processing query: {e}")

# Run SE in e loop
def run_search_engine(documents, td_matrix, t2i):
    while True:
        query = input("\nEnter your query (or type 'quit' to exit): ")
        if query.lower() == 'quit' or query == '':
            break
        process_query(query, td_matrix, t2i, documents)

def main() -> None:
    if not(os.path.exists("./pep_data.json")):
           pep_data = get_pep_data()
           save_pep_data(pep_data)

    # Changed to a single filepath since only one pep_data file now
    # -- M. Summanen
    file_path = "./pep_data.json"

    # Load docs
    documents = load_documents_from_files(file_path)
    print(documents)


    """
    The Below code has been commented out for testing purposes when
    implementing the PEP functionality.

    TODO: Uncomment when needed
    -- M. Summanen
    """
    #if documents:
        # Initialize 
    #    td_matrix, terms, t2i, cv, sparse_matrix = initialize_search_engine(documents)

        # Start 
        # run_search_engine(documents, td_matrix, t2i)

    #else:
        # print("No documents were loaded from the files.")
    
if __name__ == "__main__":
    main()
