# is <sup>[![Version Badge][npm-version-svg]][npm-url]</sup>

[![Build Status][travis-svg]][travis-url]
[![dependency status][deps-svg]][deps-url]
[![dev dependency status][dev-deps-svg]][dev-deps-url]
[![License][license-image]][license-url]
[![Downloads][downloads-image]][downloads-url]

[![npm badge][npm-badge-png]][npm-url]

[![browser support][testling-png]][testling-url]

The definitive JavaScript type testing library

To be or not to be? This is the library!

## Installation

As a node.js module

```shell
$ npm install is
```

As a component
```shell
$ component install enricomarino/is
```

## API

### general

 - ``is.a`` (value, type) or ``is.type`` (value, type)
 - ``is.defined`` (value)
 - ``is.empty`` (value)
 - ``is.equal`` (value, other)
 - ``is.hosted`` (value, host)
 - ``is.instance`` (value, constructor)
 - ``is.instanceof`` (value, constructor) - deprecated, because in ES3 browsers, "instanceof" is a reserved word
 - ``is.nil`` (value)
 - ``is.null`` (value) - deprecated, because in ES3 browsers, "null" is a reserved word
 - ``is.undef`` (value)
 - ``is.undefined`` (value) - deprecated, because in ES3 browsers, "undefined" is a reserved word

### arguments

 - ``is.args`` (value)
 - ``is.arguments`` (value) - deprecated, because "arguments" is a reserved word
 - ``is.args.empty`` (value)

### array

 - ``is.array`` (value)
 - ``is.array.empty`` (value)
 - ``is.arraylike`` (value)

### boolean

 - ``is.bool`` (value)
 - ``is.boolean`` (value) - deprecated, because in ES3 browsers, "boolean" is a reserved word
 - ``is.false`` (value) - deprecated, because in ES3 browsers, "false" is a reserved word
 - ``is.true`` (value) - deprecated, because in ES3 browsers, "true" is a reserved word

### date

 - ``is.date`` (value)

### element

 - ``is.element`` (value)

### error

 - ``is.error`` (value)

### function

 - ``is.fn`` (value)
 - ``is.function`` (value) - deprecated, because in ES3 browsers, "function" is a reserved word

### number

 - ``is.number`` (value)
 - ``is.infinite`` (value)
 - ``is.decimal`` (value)
 - ``is.divisibleBy`` (value, n)
 - ``is.integer`` (value)
 - ``is.int`` (value) - deprecated, because in ES3 browsers, "int" is a reserved word
 - ``is.maximum`` (value, others)
 - ``is.minimum`` (value, others)
 - ``is.nan`` (value)
 - ``is.even`` (value)
 - ``is.odd`` (value)
 - ``is.ge`` (value, other)
 - ``is.gt`` (value, other)
 - ``is.le`` (value, other)
 - ``is.lt`` (value, other)
 - ``is.within`` (value, start, finish)

### object

 - ``is.object`` (value)

### regexp

 - ``is.regexp`` (value)

### string

 - ``is.string`` (value)

### encoded binary

 - ``is.base64`` (value)
 - ``is.hex`` (value)

### Symbols
 - ``is.symbol`` (value)

### BigInts
 - ``is.bigint`` (value)

## Contributors

- [Jordan Harband](https://github.com/ljharb)

[npm-url]: https://npmjs.org/package/is
[npm-version-svg]: http://versionbadg.es/enricomarino/is.svg
[travis-svg]: https://travis-ci.org/enricomarino/is.svg
[travis-url]: https://travis-ci.org/enricomarino/is
[deps-svg]: https://david-dm.org/enricomarino/is.svg
[deps-url]: https://david-dm.org/enricomarino/is
[dev-deps-svg]: https://david-dm.org/enricomarino/is/dev-status.svg
[dev-deps-url]: https://david-dm.org/enricomarino/is#info=devDependencies
[testling-png]: https://ci.testling.com/enricomarino/is.png
[testling-url]: https://ci.testling.com/enricomarino/is
[npm-badge-png]: https://nodei.co/npm/is.png?downloads=true&stars=true
[license-image]: http://img.shields.io/npm/l/is.svg
[license-url]: LICENSE.md
[downloads-image]: http://img.shields.io/npm/dm/is.svg
[downloads-url]: http://npm-stat.com/charts.html?package=is
