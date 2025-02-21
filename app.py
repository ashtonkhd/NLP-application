from flask import Flask, request, render_template, jsonify
import json
from src import boolean_search as bosrch
from src import rank_search as rascrh
from src import search_logic as srchengine

app = Flask(__name__)

def load_pep_data():
    with open("data/pep_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

documents = load_pep_data()
pep_numbers = list(documents.keys())
pep_contents = list(documents.values())

# Initialisation
boolean_matrix, boolean_vectorizer = bosrch.initialize_binary_engine(pep_contents)
ranked_matrix, ranked_vectorizer = rascrh.initialize_ranked_engine(pep_contents)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query", "")
    method = request.json.get("method", "boolean")

    if method == "boolean":
        results = srchengine.run_search_engine(boolean_matrix, boolean_vectorizer, pep_numbers, "boolean", query)
    elif method == "tf-idf":
        results = srchengine.run_search_engine(ranked_matrix, ranked_vectorizer, pep_numbers, "ranked", query)
    else:
        results = []  # Semantic engine 
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)