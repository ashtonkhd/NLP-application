from flask import Flask, request, render_template
import json

from src import boolean_search as bosrch
from src import rank_search as rascrh
from src import search_logic as srchengine

app = Flask(__name__)

def load_pep_data():
    with open("pep_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

documents = load_pep_data()
pep_numbers = list(documents.keys())
pep_contents = []

for number in pep_numbers:
    pep_contents.append(documents[number]["content"])

# Initialisation
boolean_matrix, boolean_vectorizer = bosrch.initialize_binary_engine(pep_contents)
ranked_matrix, ranked_vectorizer = rascrh.initialize_ranked_engine(pep_contents)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    _search = request.form
    query = _search["query"]
    method = _search["method"]
    
    count = _search["amount"]

    if not(count.isdigit()):
        count = 5
    else:
        count = int(count)

    results = []
    numbers = []
    links = []
    
    match method:
        case "boolean":
            results = srchengine.run_search_engine(boolean_matrix,boolean_vectorizer,pep_numbers,"boolean",query, count)

            for entry in results:
                numbers.append(entry)

        case "ranked":
            results = srchengine.run_search_engine(ranked_matrix,ranked_vectorizer,pep_numbers,"ranked",query, count)

            for entry in results:
                numbers.append(entry[0])
    
    return render_template("search.html", count=count, numbers=numbers, metadata=documents)

if __name__ == "__main__":
    app.run(debug=True)
