# node.extend

A port of jQuery.extend that **actually works** on node.js

[![Build Status][travis-svg]][travis-url]
[![dependency status][deps-svg]][deps-url]
[![dev dependency status][dev-deps-svg]][dev-deps-url]

[![browser support][testling-png]][testling-url]


## Description

None of the existing ones on npm really work therefore I ported it myself.



## Usage

To install this module in your current working directory (which should already contain a package.json), run

```
npm install node.extend
```

You can additionally just list the module in your [package.json](https://npmjs.org/doc/json.html) and run npm install.

Then, require this package where you need it:

```
var extend = require('node.extend');
```

The syntax for merging two objects is as follows:

```
var destObject = extend({}, sourceObject);
// Where sourceObject is the object whose properties will be copied into another.
// NOTE: In this situation, this is not a deep merge. See below on how to handle a deep merge.
```

For information about how the clone works internally, view source in lib/extend.js or checkout the doc from [jQuery][]

### A Note About Deep Merge (avoiding pass-by-reference cloning)

In order to force a deep merge, when extending an object, you must pass boolean true as the first argument to extend:

```
var destObject = extend(true, {}, sourceObject);
// Where sourceObject is the object whose properties will be copied into another.
```

See [this article](http://www.jon-carlos.com/2013/is-javascript-call-by-value-or-call-by-reference/) for more information about the need for deep merges in JavaScript.

## Credit

- Jordan Harband [@ljharb][]



## License

Copyright 2011, John Resig
Dual licensed under the MIT or GPL Version 2 licenses.
http://jquery.org/license

[testling-png]: https://ci.testling.com/dreamerslab/node.extend.png
[testling-url]: https://ci.testling.com/dreamerslab/node.extend
[travis-svg]: https://travis-ci.org/dreamerslab/node.extend.svg
[travis-url]: https://travis-ci.org/dreamerslab/node.extend
[deps-svg]: https://david-dm.org/dreamerslab/node.extend.svg
[deps-url]: https://david-dm.org/dreamerslab/node.extend
[dev-deps-svg]: https://david-dm.org/dreamerslab/node.extend/dev-status.svg
[dev-deps-url]: https://david-dm.org/dreamerslab/node.extend#info=devDependencies
[jQuery]: http://api.jquery.com/jQuery.extend/
[@ljharb]: https://twitter.com/ljharb

