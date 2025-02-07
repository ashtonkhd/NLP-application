import re
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer

# Operator replacements
d = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "1 -", "NOT": "1 -",
    "(": "(", ")": ")"
}

# Load docs
def load_documents_from_files(file_paths):
    documents = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                articles = content.split('\n</article>\n')  # Assuming each article is separated by </article>
                documents.extend([article.strip() for article in articles if article.strip()])
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

# Files
file_paths = [
    "wiki.txt",  
    "wiki_a.txt"  
]

# Load docs
documents = load_documents_from_files(file_paths)

if documents:
    # Initialize 
    td_matrix, terms, t2i, cv, sparse_matrix = initialize_search_engine(documents)

    # Start 
    run_search_engine(documents, td_matrix, t2i)
else:
    print("No documents were loaded from the files.")
