# PEP-Searcher: Module Documentation

[toc]

## src.boolean_search

`src.boolean_search` is one of the smaller modules of the project,
containing only a single function.

```
initialize_binary_engine(documents)
    documents => list of strings
    
    => returns CountVectorizer and a term matrix with, binary setting,
       fitted for the provided documents
```

## src.query_processing

`src.query_processing` is the module containing the main code for the
query functionality of the program and other query related functions. Its
main entry function is `process_query()`

```
process_query(query, td_matrix, t2i)
    query     => the search query provided by the user
    td_matrix => term matrix for the given dataset
    t2i       => mapping (dictionary) of terms to indices of td_matrix
    
    => returns results for the given query.
```

Other functions in `src.query_processing` are not intended to be called
from outside the module, and thus have been named with an underline prefix.
Calling any of such functions from outside their file is not advised as it
can result in unintended behaviour.

## src.rank_search

`src.rank_search` is the ranked version of `src.boolean_search`. The
only difference between them is that the former creates the CountVectorizer
with the parameter `binary=False`

```
initialize_ranked_engine(documents)
    documents => a list of strings
    
    => returns CountVectorizer and term matrix fitted for the provided
       documents
```

## src.recollect_pep

`src.recollect_pep` is not part of the main functionality of the program.
Instead it is a module for the optional recollection of PEP dataset,
`pep_data.json` according to the pep api, `pep_metadata.json`.

**Running** src.recollect_pep should be **done** with it
**as the main program**, **and** additionally **requires** the otherwise
optional **beautifulsoup4** and **requests** modules.

The main function of src.recollect_pep is `getPepContents()` though
accessing it directly is not advised as expected parameters are only
provided if the `src.recollect_pep` is the main program.

```
getPepContents(pep_data: dict[str, typing.Any])
    => returns dictionary of pep with number, title, authors, url and
       content
```

## src.search_logic

`src.search_logic` is the module that functions as the main program loop
for the search-part of the program. Its main function is
`run_search_engine()`, which is responsible for taking the user query, and
passing it along with other needed parameters to
`src.query_processing.process_query()`. Then either ranking the output
given by it, if using ranked search, or converting it to a binary variant,
if using boolean search.

```
run_search_engine(matrix, cv, pep_numbers, model, query, show=5)
    matrix => term matrix for the search engine
    cs     => CountVectorizer for the search model
    model  => the search model to use
    query  => The search query to process with
              src.query_processing.process_query()
    show   => the mount of results to return or "show" to the user.
    
    => retuns a list of results for the query, limited by show.
```

## src.visualize_data

`src.visualize_data` is the module responsible for creating a pie chart
showing what portion of the total amount of PEPs in the data base were
retrieved as results for the user submittedd search query. **IT IS NOT THE
HOW MANY DOCUMENTS CONTAINED THE QUERY, JUST HOW MANY RESULTS WERE
RETRIEVED**

```
createPlot(amount_with, total, path):
    amount_with => the amount of results retrieved
    total       => total amount of documents/PEPS
    path        => temporary save location, as flask needs it be an image
                   for it to be able to be added to the html-template.
```
