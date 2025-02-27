# Simple PEP-searcher

A simple tool to search queries from Python Enhancement Proposals using
different types of searching engines.

## Todo

- [ ] Add Semantic Search option

- [ ] Prettify the user interface

## In Progress

- [ ] Fix search logic
  - [x] Make lower case queries work
  - [x] Add support for NOT-operator
    - [ ] Verify that NOT-operator works properly.
  - [ ] Add support for brackets
  - [ ] Make TD-IDF search not give false positive results (listing places with no hits as hits)

## Done

- [x] Fix issues with the User "Show" box.
  - [x] Make empty input not break the program.
  - [x] Make inputting non-integer not break the program.

- [x] Find a way to combine \_process\_query\_boolean and \_process\_query\_ranked.



