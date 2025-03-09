from flask import Flask, request, render_template
import json

from src import boolean_search as bosrch
from src import rank_search as rascrh
from src import search_logic as srchengine
from src import visualize_data as visdata

PEP_DATA = "./pep_data.json"
GRAPH_PATH = "./static/term_graph.png"

app = Flask(__name__)

def load_pep_data():
    with open(PEP_DATA, "r", encoding="utf-8") as file:
        return json.load(file)

documents = load_pep_data()
pep_numbers = list(documents.keys())
pep_contents = []
pep_amount = len(pep_numbers)

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
    
    try:
        graphs = _search["use_graphs"]
        graphs = True
    except KeyError:
        graphs = False
    
    count = _search["amount"]

    if not(count.isdigit()):
        count = 5
    else:
        count = int(count)

    results = []
    numbers = []
    links = []
    
    if query == "":
        return render_template("empty_query.html")
    
    match method:
        case "boolean":
            results = srchengine.run_search_engine(boolean_matrix,boolean_vectorizer,pep_numbers,"boolean",query, count)

            if graphs:
                visdata.createPlot(len(results), pep_amount, GRAPH_PATH)

            for entry in results:
                numbers.append(entry)

        case "ranked":
            results = srchengine.run_search_engine(ranked_matrix,ranked_vectorizer,pep_numbers,"ranked",query, count)
            
            if graphs:
                visdata.createPlot(len(results), pep_amount, GRAPH_PATH)

            for entry in results:
                numbers.append(entry[0])
    if graphs:
        return render_template("search_graphs.html", count=count, numbers=numbers, metadata=documents)
    else:
       return render_template("search.html", count=count, numbers=numbers, metadata=documents)
#Results route    
@app.route("/results", methods=["POST"])
def results():
    numbers = request.form.getlist("numbers")
    count = request.form.get("count", type=int, default=0)
    return render_template("results.html", numbers=numbers, count=count, metadata=documents)

if __name__ == "__main__":
    app.run(debug=True)
