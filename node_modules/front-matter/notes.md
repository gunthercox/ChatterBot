
* [ ] benchmarks
* [ ] browser tests
* [ ] streaming support
* [ ] custom parsers
* [ ] rename attributes?
* [ ] sauce labs browser badge
* [ ] should the yaml parser be separate?
* [ ] Add benchmark results to the README
* [ ] Add a note about size to the README
* [ ] Add standard

* [ ] Add notes for collaborators about publishing

Should we create an org for static site authors?

https://github.com/juliangruber/balanced-match/blob/master/index.js

* [ ] streaming support?
* [ ] Since the name of this package is very generic, it would be nice to be able to specify a separators and parsers. For example, parse front-matter as CSON when a *** separator is used:

***
title: 'Hello'
greatDocumentaries: [
    'earthlings.com'
    'forksoverknives.com'
    'cowspiracy.com'
]
***

* [ ] Something like below will break front-matter. It thinks the content between the horizontal lines is metadata.

# hello world

this is a markdown document

---

some text here

---

foo
This can be avoided by declaring an empty metadata, but maybe a proper fix is to only look for metadata in the beginning of the file.

---
---

etc

* [ ] browser tests

# Hello world!
