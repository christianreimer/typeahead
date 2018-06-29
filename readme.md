## Typeahead

Server based typeahead/autocomplete service.

The plan is to develop the following properties:

* Immediate result for queries of length 1 or 2 characters
* Parallel search for likely misspellings of the query term
* Return results sorted by likelihood and capped at a max
* Change the weights/values of different terms based on usage
* Context aware such that command sequences can be built up 
