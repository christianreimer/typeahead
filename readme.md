### Typeahead

Typeahead service with the following properties:
* Immidiate result for queries of length 1 or 2 characters
* Will simultanisely search for likely misspellings of the query term
* Will return results sorted by likelihood

### Design

Request ->  TA Server 
            -> Generate N most likely alternative spellings
            -> Send N requests in parallel to trie servers
            -> Collect result, sort, and return



`vocabulary` is the set of tokens (words) the system knows. Each token can have
different capitalization, but all tokens are stored in the trie using lower case

`typeahead` takes as input a query string, finds the most likely alternatives,
queries for each in parallel, sorts the end result, and sends it back

Whenever a final token is selected, the value of that token is increased

On startup, generate a mapping from all 1 or 2 character query strings to the
set of tokens they map to. Limit this to the N most likely (otherwise it would
be the entire vocabulary)

