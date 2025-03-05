# PEP-Searcher

Python Enhancement Proposal Searcher, or PEP-Searcher for short, is a
simple tool for information retrieval from PEPs. Due to the fact that there
exist a large quantity of PEPs and they can contain helpful information
from code-formatting to future plans for the language as a whole, this tool
is meant to make it easier for people to find what they want to know.

[toc]

## Installation

To install PEP-searcher, you only need to clone the repo and make sure that
the following external modules are available for use:

- flask [REQUIRED]
- numpy [REQUIRED]
- scikit-learn [REQUIRED]
- matplotlib [REQUIRED]
- requests [OPTIONAL]
- beautifulsoup4 [OPTIONAL]

## Using

### Creating/Recreating the dataset

If the file 'pep_data.json' does not exist in the projects root directory,
or you wish to update the program's dataset, you will need to regenerate it
with the script *./src/recollect_pep.py*. For this you will additionally
need both the **requests** and **beautifulsoup4** modules (marked as
optional in the list above).

### Starting the application

To start the application you need to run the command `python app.py` while
in the project's root directory. 

### Query format

Unfortunately, the query format is not as lax as it is in something like
Google or DuckDuckGo, or other search engines. The following queries work
with PEP-searcher.

```
python AND/and firefox
NOT/not python AND/and firefox
python AND/and NOT/not firefox
```

Note: In the examples given, `AND/and` indicate that both upper and
lowercased variants work, not that the term `AND/and` itself is the
expected operator.
