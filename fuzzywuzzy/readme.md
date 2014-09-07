FuzzyWuzzy
==========

Fuzzy string matching like a boss.

# Requirements

-  Python 2.4 or higher
-  difflib
-  python-Levenshtein (optional, provides a 4-10x speedup in String Matching)

# Installation

## With ```pip```

```bash
pip install fuzzywuzzy
```

## With ```git```

```bash
git clone git://github.com/seatgeek/fuzzywuzzy.git fuzzywuzzy
cd fuzzywuzzy
python setup.py install
```

# Manual

1. Download: http://github.com/seatgeek/fuzzywuzzy/zipball/master
2. Unzip the resulting file
3. Run ``python setup.py install`` in the resulting folder

# Usage

```python
>>> from fuzzywuzzy import fuzz
>>> from fuzzywuzzy import process
```

# Simple Ratio

```python
>>> fuzz.ratio("this is a test", "this is a test!")
    96
```

# Partial Ratio

```python
>>> fuzz.partial_ratio("this is a test", "this is a test!")
    100
```

# Token Sort Ratio

```python
>>> fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
    90
>>> fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
    100
```

# Token Set Ratio

```python

>>> fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
    84
>>> fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
    100
```

# Process

```python
>>> choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
>>> process.extract("new york jets", choices, limit=2)
    [('New York Jets', 100), ('New York Giants', 78)]
>>> process.extractOne("cowboys", choices)
    ("Dallas Cowboys", 90)
```

# License

Copyright © 2014 SeatGeek, Inc.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
