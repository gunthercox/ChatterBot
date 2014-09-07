#!/usr/bin/env python
# encoding: utf-8
"""
process.py

Copyright (c) 2011 Adam Cohen

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import itertools

from . import fuzz
from . import utils


def extract(query, choices, processor=None, scorer=None, limit=5):
    """Find best matches in a list or dictionary of choices, return a
    list of tuples containing the match and it's score. If a dictionery
    is used, also returns the key for each match.

    Arguments:
        query       -- an object representing the thing we want to find
        choices     -- a list or dictionary of objects we are attempting
                       to extract values from. The dictionary should
                       consist of {key: str} pairs.
        scorer      -- f(OBJ, QUERY) --> INT. We will return the objects
                       with the highest score by default, we use
                       score.WRatio() and both OBJ and QUERY should be
                       strings
        processor   -- f(OBJ_A) --> OBJ_B, where the output is an input
                       to scorer for example, "processor = lambda x:
                       x[0]" would return the first element in a
                       collection x (of, say, strings) this would then
                       be used in the scoring collection by default, we
                       use utils.full_process()

    """
    if choices is None or len(choices) == 0:
        return []

    # default, turn whatever the choice is into a workable string
    if processor is None:
        processor = lambda x: utils.full_process(x)

    # default: wratio
    if scorer is None:
        scorer = fuzz.WRatio

    sl = list()

    if isinstance(choices, dict):
        for key, choice in choices.items():
            processed = processor(choice)
            score = scorer(query, processed)
            tuple = (choice, score, key)
            sl.append(tuple)

    elif isinstance(choices, list):
        for choice in choices:
            processed = processor(choice)
            score = scorer(query, processed)
            tuple = (choice, score)
            sl.append(tuple)

    sl.sort(key=lambda i: i[1], reverse=True)
    return sl[:limit]


def extractBests(query, choices, processor=None, scorer=None, score_cutoff=0, limit=5):
    """Find best matches above a score in a list of choices, return a
    list of tuples containing the match and it's score.

    Convenience method which returns the choices with best scores, see
    extract() for full arguments list

    Optional parameter: score_cutoff.
        If the choice has a score of less than or equal to score_cutoff
        it will not be included on result list

    """

    best_list = extract(query, choices, processor, scorer, limit)
    if len(best_list) > 0:
        return list(itertools.takewhile(lambda x: x[1] > score_cutoff, best_list))
    else:
        return []


def extractOne(query, choices, processor=None, scorer=None, score_cutoff=0):
    """Find the best match above a score in a list of choices, return a
    tuple containing the match and it's score if it's above the treshold
    or None.

    Convenience method which returns the single best choice, see
    extract() for full arguments list

    Optional parameter: score_cutoff.
        If the best choice has a score of less than or equal to
        score_cutoff we will return none (intuition: not a good enough
        match)

    """

    best_list = extract(query, choices, processor, scorer, limit=1)
    if len(best_list) > 0:
        best = best_list[0]
        if best[1] > score_cutoff:
            return best
        else:
            return None
    else:
        return None
