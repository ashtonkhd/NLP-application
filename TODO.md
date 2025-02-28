# Simple PEP-searcher

A simple tool to search queries from Python Enhancement Proposals using
different types of searching engines.

## Todo

- [ ] Add Semantic Search option

- [ ] Prettify the user interface

- [ ] Add support for lower case logic operators (reason: CAPS is getting bother some)

- [ ] Add safe guards for attempting to get more results than amount of peps
  - [ ] Instead of straight results to iterator, use iterator while it is lesser or equal to length of results list.

## In Progress

- [ ] Fix search logic
  - [x] Add support for NOT-operator
    - [ ] Verify that NOT-operator works properly.
  - [ ] Add support for brackets

## Done

- [x] Make TD-IDF search not give false positive results (listing places with no hits as hits)


