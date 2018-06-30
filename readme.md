## Typeahead

[![Build Status](https://travis-ci.org/christianreimer/typeahead.svg?branch=master)](https://travis-ci.org/christianreimer/typeahead) [![Coverage Status](https://coveralls.io/repos/github/christianreimer/typeahead/badge.svg?branch=master)](https://coveralls.io/github/christianreimer/typeahead?branch=master) [![Python Version](https://img.shields.io/badge/python-3.6-blue.svg)](https://img.shields.io/badge/python-3.6-blue.svg)

Server based typeahead/autocomplete service.

The plan is to develop the following properties:

* Immediate result for queries of length 1 or 2 characters
* Parallel search for likely misspellings of the query term
* Return results sorted by likelihood and capped at a max
* Change the weights/values of different terms based on usage
* Context aware such that command sequences can be built up 
