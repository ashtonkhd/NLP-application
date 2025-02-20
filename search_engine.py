import re
import numpy as np
import requests
import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup


# I have seperated the program into multiple files in order to make each
# file less of a bother to work with than one long file would be. I have
# attempted to name them as clearly as possible. If you object to this
# method, do please tell.
# -- M. Summanen

from src import boolean_search as bosrch
from src import rank_search as rascrh
from src import search_logic as srchengine

# Operator replacements
d = {
    "and": "&", "AND": "&",
    "or": "|", "OR": "|",
    "not": "1 -", "NOT": "1 -",
    "(": "(", ")": ")"
}

LOGICAL_OPERATORS = ["&", "|"]
ACCEPTED_SEARCH_STYLES = ["ranked", "boolean"]

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

    # REMINDME: change path to 'data/pep_data.json'
    
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

# Rewrite query to Boo
def rewrite_token(t):
    return d.get(t, f'td_matrix[t2i["{t}"]]')  # Replace operators or map terms
            
def main() -> None:
     # REMINDME: change path to 'data/pep_data.json'
    if not(os.path.exists("./pep_data.json")):
           pep_data = get_pep_data()
           save_pep_data(pep_data)

    # Changed to a single filepath since only one pep_data file now
    # -- M. Summanen
    # REMINDME: change path to 'data/pep_data.json'
    file_path = "./pep_data.json"

    # Load docs
    documents = load_documents_from_files(file_path)
    pep_numbers = list(documents.keys())
    pep_contents = list(documents.values())

    pep_matrix = None

    # Support for Boolean, ranked, etc.
    search_style = ""
    while not(search_style in ACCEPTED_SEARCH_STYLES):
        search_style = input("Search method [Boolean, ranked]: ").lower()

        
    if not(len(pep_contents) == 0):
        match search_style:

            # TODO: Make run_search_engine() run differently depending
            # on search engine type.
            
            case "ranked":
                pep_matrix, vectorizer = rascrh.initialize_ranked_engine(pep_contents)
                model = "ranked"

            case "boolean":
                pep_matrix, vectorizer = bosrch.initialize_binary_engine(pep_contents)
                model = "boolean"

        srchengine.run_search_engine(pep_matrix, vectorizer, pep_numbers, model)

    else:
        print("Unable to load pep_data.json. Exiting...")
        exit()
    
if __name__ == "__main__":
    main()
