/* globals window, document, HTMLElement */

'use strict';

var test = require('tape');
var is = require('../index.js');

var forEach = require('foreach');
var toStr = Object.prototype.toString;

var genFn = require('make-generator-function');

test('is.type', function (t) {
  var booleans = [true, false];
  forEach(booleans, function (boolean) {
    t.ok(is.type(boolean, 'boolean'), '"' + boolean + '" is a boolean');
  });

  var numbers = [1, 0 / 1, 0 / -1, NaN, Infinity, -Infinity];
  forEach(numbers, function (number) {
    t.ok(is.type(number, 'number'), '"' + number + '" is a number');
  });

  var objects = [{}, null, new Date()];
  forEach(objects, function (object) {
    t.ok(is.type(object, 'object'), '"' + object + '" is an object');
  });

  var strings = ['', 'abc'];
  forEach(strings, function (string) {
    t.ok(is.type(string, 'string'), '"' + string + '" is a string');
  });

  t.ok(is.type(undefined, 'undefined'), 'undefined is undefined');

  t.end();
});

test('is.undef', function (t) {
  t.ok(is.undef(), 'absent undefined is undefined');
  t.ok(is.undef(undefined), 'literal undefined is undefined');
  t.notOk(is.undef(null), 'null is not undefined');
  t.notOk(is.undef({}), 'object is not undefined');
  t.end();
});

test('is.defined', function (t) {
  t.notOk(is.defined(), 'undefined is not defined');
  t.ok(is.defined(null), 'null is defined');
  t.ok(is.defined({}), 'object is defined');
  t.end();
});

test('is.empty', function (t) {
  t.ok(is.empty(''), 'empty string is empty');
  t.ok(is.empty(Object('')), 'empty String object is empty');
  t.ok(is.empty([]), 'empty array is empty');
  t.ok(is.empty({}), 'empty object is empty');
  t.ok(is.empty(null), 'null is empty');
  t.ok(is.empty(), 'undefined is empty');
  t.ok(is.empty(undefined), 'undefined is empty');
  t.ok(is.empty(false), 'false is empty');
  t.ok(is.empty(0), '0 is empty');
  t.ok(is.empty(NaN), 'nan is empty');
  (function () {
    t.ok(is.empty(arguments), 'empty arguments is empty');
  }());
  t.notOk(is.empty({ a: 1 }), 'nonempty object is not empty');
  t.notOk(is.empty(true), 'true is not empty');
  t.notOk(is.empty(/a/g), 'regex is not empty');
  t.notOk(is.empty(new Date()), 'date is not empty');
  t.end();
});

test('is.equal', function (t) {
  t.test('primitives', function (pt) {
    var primitives = [true, false, undefined, null, '', 'foo', 0, Infinity, -Infinity];
    pt.plan(primitives.length);
    for (var i = 0; i < primitives.length; ++i) {
      pt.ok(is.equal(primitives[i], primitives[i]), 'primitives are equal to themselves: ' + primitives[i]);
    }
    pt.end();
  });

  t.test('arrays', function (at) {
    at.ok(is.equal([1, 2, 3], [1, 2, 3]), 'arrays are shallowly equal');
    at.ok(is.equal([1, 2, [3, 4]], [1, 2, [3, 4]]), 'arrays are deep equal');
    at.notOk(is.equal([1, 2, 3], [5, 2, 3]), 'inequal arrays are not equal');
    at.notOk(is.equal([1, 2], [2, 3]), 'inequal arrays are not equal');
    at.notOk(is.equal([1, 2, 3], [2, 3]), 'inequal length arrays are not equal');
    at.ok(is.equal([], []), 'empty arrays are equal');

    var arr = [1, 2];
    at.ok(is.equal(arr, arr), 'array is equal to itself');

    at.end();
  });

  t.test('dates', function (dt) {
    dt.plan(2);
    var now = new Date();
    dt.ok(is.equal(now, new Date(now.getTime())), 'two equal date objects are equal');
    setTimeout(function () {
      dt.notOk(is.equal(now, new Date()), 'two inequal date objects are not equal');
      dt.end();
    }, 10);
  });

  t.test('plain objects', function (ot) {
    ot.ok(is.equal({ a: 1, b: 2, c: 3 }, { a: 1, b: 2, c: 3 }), 'objects are shallowly equal');
    ot.ok(is.equal({ a: { b: 1 } }, { a: { b: 1 } }), 'objects are deep equal');
    ot.notOk(is.equal({ a: 1 }, { a: 2 }), 'inequal objects are not equal');
    ot.end();
  });

  t.test('object instances', function (ot) {
    var F = function F() {
      this.foo = 'bar';
    };
    F.prototype = {};
    var G = function G() {
      this.foo = 'bar';
    };
    var f = new F();
    var g = new G();

    ot.ok(is.equal(f, f), 'the same object instances are equal');
    ot.ok(is.equal(f, new F()), 'two object instances are equal when the prototype and props are the same');
    ot.ok(is.equal(f, new G()), 'two object instances are equal when the prototype is not the same, but props are');

    g.bar = 'baz';
    ot.notOk(is.equal(f, g), 'object instances are not equal when the prototype and props are not the same');
    ot.notOk(is.equal(g, f), 'object instances are not equal when the prototype and props are not the same');
    ot.end();
  });

  t.test('functions', function (ft) {
    var F = function () {};
    F.prototype = {};
    var G = function () {};
    G.prototype = new Date();

    ft.notEqual(F.prototype, G.prototype, 'F and G have different prototypes');
    ft.notOk(is.equal(F, G), 'two functions are not equal when the prototype is not the same');

    var H = function () {};
    H.prototype = F.prototype;

    ft.equal(F.prototype, H.prototype, 'F and H have the same prototype');
    ft.ok(is.equal(F, H), 'two functions are equal when the prototype is the same');
    ft.end();
  });

  t.end();
});

test('is.hosted', function (t) {
  t.ok(is.hosted('a', { a: {} }), 'object is hosted');
  t.ok(is.hosted('a', { a: [] }), 'array is hosted');
  t.ok(is.hosted('a', { a: function () {} }), 'function is hosted');
  t.notOk(is.hosted('a', { a: true }), 'boolean value is not hosted');
  t.notOk(is.hosted('a', { a: false }), 'boolean value is not hosted');
  t.notOk(is.hosted('a', { a: 3 }), 'number value is not hosted');
  t.notOk(is.hosted('a', { a: undefined }), 'undefined value is not hosted');
  t.notOk(is.hosted('a', { a: 'abc' }), 'string value is not hosted');
  t.notOk(is.hosted('a', { a: null }), 'null value is not hosted');
  t.end();
});

test('is.instance', function (t) {
  t.ok(is.instance(new Date(), Date), 'new Date is instanceof Date');
  var F = function () {};
  t.ok(is.instance(new F(), F), 'new constructor is instanceof constructor');
  t.end();
});

test('is.nil', function (t) {
  var isNull = is.nil;
  t.equal(isNull, is['null'], 'is.nil is the same as is.null');
  t.ok(isNull(null), 'null is null');
  t.notOk(isNull(undefined), 'undefined is not null');
  t.notOk(isNull({}), 'object is not null');
  t.end();
});

test('is.args', function (t) {
  t.notOk(is.args([]), 'array is not arguments');
  (function () {
    t.ok(is.args(arguments), 'arguments is arguments');
  }());
  (function () {
    t.notOk(is.args(Array.prototype.slice.call(arguments)), 'sliced arguments is not arguments');
  }());
  var fakeOldArguments = {
    callee: function () {},
    length: 3
  };
  t.ok(is.args(fakeOldArguments), 'old-style arguments object is arguments');
  t.end();
});

test('is.args.empty', function (t) {
  t.notOk(is.args.empty([]), 'empty array is not empty arguments');
  (function () {
    t.ok(is.args.empty(arguments), 'empty arguments is empty arguments');
  }());
  (function () {
    t.notOk(is.args.empty(Array.prototype.slice.call(arguments)), 'empty sliced arguments is not empty arguments');
  }());
  t.end();
});

test('is.array', function (t) {
  t.ok(is.array([]), 'array is array');
  (function () {
    t.ok(is.array(Array.prototype.slice.call(arguments)), 'sliced arguments is array');
  }());
  t.end();
});

test('is.array.empty', function (t) {
  t.ok(is.array.empty([]), 'empty array is empty array');
  (function () {
    t.notOk(is.array.empty(arguments), 'empty arguments is not empty array');
  }());
  (function () {
    t.ok(is.array.empty(Array.prototype.slice.call(arguments)), 'empty sliced arguments is empty array');
  }());
  t.end();
});

test('is.isarraylike', function (t) {
  t.notOk(is.arraylike(), 'undefined is not array-like');
  t.notOk(is.arraylike(null), 'null is not array-like');
  t.notOk(is.arraylike(false), 'false is not array-like');
  t.notOk(is.arraylike(true), 'true is not array-like');
  t.ok(is.arraylike({ length: 0 }), 'object with zero length is array-like');
  t.ok(is.arraylike({ length: 1 }), 'object with positive length is array-like');
  t.notOk(is.arraylike({ length: -1 }), 'object with negative length is not array-like');
  t.notOk(is.arraylike({ length: NaN }), 'object with NaN length is not array-like');
  t.notOk(is.arraylike({ length: 'foo' }), 'object with string length is not array-like');
  t.notOk(is.arraylike({ length: '' }), 'object with empty string length is not array-like');
  t.ok(is.arraylike([]), 'array is array-like');
  (function () {
    t.ok(is.arraylike(arguments), 'empty arguments is array-like');
  }());
  (function () {
    t.ok(is.arraylike(arguments), 'nonempty arguments is array-like');
  }(1, 2, 3));
  t.end();
});

test('is.bool', function (t) {
  t.ok(is.bool(true), 'literal true is a boolean');
  t.ok(is.bool(false), 'literal false is a boolean');
  t.ok(is.bool(Object(true)), 'object true is a boolean');
  t.ok(is.bool(Object(false)), 'object false is a boolean');
  t.notOk(is.bool(), 'undefined is not a boolean');
  t.notOk(is.bool(null), 'null is not a boolean');
  t.end();
});

test('is.false', function (t) {
  var isFalse = is['false'];
  t.ok(isFalse(false), 'false is false');
  t.ok(isFalse(Object(false)), 'object false is false');
  t.notOk(isFalse(true), 'true is not false');
  t.notOk(isFalse(), 'undefined is not false');
  t.notOk(isFalse(null), 'null is not false');
  t.notOk(isFalse(''), 'empty string is not false');
  t.end();
});

test('is.true', function (t) {
  var isTrue = is['true'];
  t.ok(isTrue(true), 'true is true');
  t.ok(isTrue(Object(true)), 'object true is true');
  t.notOk(isTrue(false), 'false is not true');
  t.notOk(isTrue(), 'undefined is not true');
  t.notOk(isTrue(null), 'null is not true');
  t.notOk(isTrue(''), 'empty string is not true');
  t.end();
});

test('is.date', function (t) {
  t.ok(is.date(new Date()), 'new Date is date');
  t.notOk(is.date(), 'undefined is not date');
  t.notOk(is.date(null), 'null is not date');
  t.notOk(is.date(''), 'empty string is not date');
  var nowTS = (new Date()).getTime();
  t.notOk(is.date(nowTS), 'timestamp is not date');
  var F = function () {};
  F.prototype = new Date();
  t.notOk(is.date(new F()), 'Date subtype is not date');
  t.end();
});

test('is.date.valid', function (t) {
  t.ok(is.date.valid(new Date()), 'new Date() is a valid date');
  t.notOk(is.date.valid(new Date('')), 'new Date("") is not a valid date');
  t.end();
});

test('is.element', function (t) {
  t.notOk(is.element(), 'undefined is not element');

  t.test('when HTMLElement exists', { skip: typeof HTMLElement === 'undefined' }, function (st) {
    var element = document.createElement('div');
    st.ok(is.element(element), 'HTMLElement is element');
    st.notOk(is.element({ nodeType: 1 }), 'object with nodeType is not element');
    st.end();
  });

  t.end();
});

test('is.error', function (t) {
  var err = new Error('foo');
  t.ok(is.error(err), 'Error is error');
  t.notOk(is.error({}), 'object is not error');
  var objWithErrorToString = {
    toString: function () {
      return '[object Error]';
    }
  };
  t.equal(String(objWithErrorToString), toStr.call(new Error()), 'obj has Error\'s toString');
  t.notOk(is.error(objWithErrorToString), 'object with Error\'s toString is not error');
  t.end();
});

test('is.fn', function (t) {
  t.equal(is['function'], is.fn, 'alias works');
  t.ok(is.fn(function () {}), 'function is function');
  if (typeof window !== 'undefined') {
    // in IE7/8, typeof alert === 'object'
    t.ok(is.fn(window.alert), 'window.alert is function');
  }
  t.notOk(is.fn({}), 'object is not function');
  t.notOk(is.fn(null), 'null is not function');

  t.test('generator functions', { skip: !genFn }, function (st) {
    t.ok(is.fn(genFn), 'generator function is function');
    st.end();
  });

  t.end();
});

test('is.number', function (t) {
  t.ok(is.number(0), 'positive zero is number');
  t.ok(is.number(0 / -1), 'negative zero is number');
  t.ok(is.number(3), 'three is number');
  t.ok(is.number(NaN), 'NaN is number');
  t.ok(is.number(Infinity), 'infinity is number');
  t.ok(is.number(-Infinity), 'negative infinity is number');
  t.ok(is.number(Object(42)), 'object number is number');
  t.notOk(is.number(), 'undefined is not number');
  t.notOk(is.number(null), 'null is not number');
  t.notOk(is.number(true), 'true is not number');
  t.end();
});

test('is.infinite', function (t) {
  t.ok(is.infinite(Infinity), 'positive infinity is infinite');
  t.ok(is.infinite(-Infinity), 'negative infinity is infinite');
  t.notOk(is.infinite(NaN), 'NaN is not infinite');
  t.notOk(is.infinite(0), 'a number is not infinite');
  t.end();
});

test('is.decimal', function (t) {
  t.ok(is.decimal(1.1), 'decimal is decimal');
  t.notOk(is.decimal(0), 'zero is not decimal');
  t.notOk(is.decimal(1), 'integer is not decimal');
  t.notOk(is.decimal(NaN), 'NaN is not decimal');
  t.notOk(is.decimal(Infinity), 'Infinity is not decimal');
  t.end();
});

test('is.divisibleBy', function (t) {
  t.ok(is.divisibleBy(4, 2), '4 is divisible by 2');
  t.ok(is.divisibleBy(4, 2), '4 is divisible by 2');
  t.ok(is.divisibleBy(0, 1), '0 is divisible by 1');
  t.ok(is.divisibleBy(Infinity, 1), 'infinity is divisible by anything');
  t.ok(is.divisibleBy(1, Infinity), 'anything is divisible by infinity');
  t.ok(is.divisibleBy(Infinity, Infinity), 'infinity is divisible by infinity');
  t.notOk(is.divisibleBy(1, 0), '1 is not divisible by 0');
  t.notOk(is.divisibleBy(NaN, 1), 'NaN is not divisible by 1');
  t.notOk(is.divisibleBy(1, NaN), '1 is not divisible by NaN');
  t.notOk(is.divisibleBy(NaN, NaN), 'NaN is not divisible by NaN');
  t.notOk(is.divisibleBy(1, 3), '1 is not divisible by 3');
  t.end();
});

test('is.integer', function (t) {
  t.ok(is.integer(0), '0 is integer');
  t.ok(is.integer(3), '3 is integer');
  t.notOk(is.integer(1.1), '1.1 is not integer');
  t.notOk(is.integer(NaN), 'NaN is not integer');
  t.notOk(is.integer(Infinity), 'infinity is not integer');
  t.notOk(is.integer(null), 'null is not integer');
  t.notOk(is.integer(), 'undefined is not integer');
  t.end();
});

test('is.maximum', function (t) {
  t.ok(is.maximum(3, [3, 2, 1]), '3 is maximum of [3,2,1]');
  t.ok(is.maximum(3, [1, 2, 3]), '3 is maximum of [1,2,3]');
  t.ok(is.maximum(4, [1, 2, 3]), '4 is maximum of [1,2,3]');
  t.ok(is.maximum('c', ['a', 'b', 'c']), 'c is maximum of [a,b,c]');
  t.notOk(is.maximum(2, [1, 2, 3]), '2 is not maximum of [1,2,3]');

  var nanError = new TypeError('NaN is not a valid value');
  t['throws'](function () { return is.maximum(NaN); }, nanError, 'throws when first value is NaN');

  var error = new TypeError('second argument must be array-like');
  t['throws'](function () { return is.maximum(2, null); }, error, 'throws when second value is not array-like');
  t['throws'](function () { return is.maximum(2, {}); }, error, 'throws when second value is not array-like');
  t.end();
});

test('is.minimum', function (t) {
  t.ok(is.minimum(1, [1, 2, 3]), '1 is minimum of [1,2,3]');
  t.ok(is.minimum(0, [1, 2, 3]), '0 is minimum of [1,2,3]');
  t.ok(is.minimum('a', ['a', 'b', 'c']), 'a is minimum of [a,b,c]');
  t.notOk(is.minimum(2, [1, 2, 3]), '2 is not minimum of [1,2,3]');

  var nanError = new TypeError('NaN is not a valid value');
  t['throws'](function () { return is.minimum(NaN); }, nanError, 'throws when first value is NaN');

  var error = new TypeError('second argument must be array-like');
  t['throws'](function () { return is.minimum(2, null); }, error, 'throws when second value is not array-like');
  t['throws'](function () { return is.minimum(2, {}); }, error, 'throws when second value is not array-like');
  t.end();
});

test('is.nan', function (t) {
  t.ok(is.nan(NaN), 'NaN is not a number');
  t.ok(is.nan('abc'), 'string is not a number');
  t.ok(is.nan(true), 'boolean is not a number');
  t.ok(is.nan({}), 'object is not a number');
  t.ok(is.nan([]), 'array is not a number');
  t.ok(is.nan(function () {}), 'function is not a number');
  t.notOk(is.nan(0), 'zero is a number');
  t.notOk(is.nan(3), 'three is a number');
  t.notOk(is.nan(1.1), '1.1 is a number');
  t.notOk(is.nan(Infinity), 'infinity is a number');
  t.end();
});

test('is.even', function (t) {
  t.ok(is.even(0), 'zero is even');
  t.ok(is.even(2), 'two is even');
  t.ok(is.even(Infinity), 'infinity is even');
  t.notOk(is.even(1), '1 is not even');
  t.notOk(is.even(), 'undefined is not even');
  t.notOk(is.even(null), 'null is not even');
  t.notOk(is.even(NaN), 'NaN is not even');
  t.end();
});

test('is.odd', function (t) {
  t.ok(is.odd(1), 'zero is odd');
  t.ok(is.odd(3), 'two is odd');
  t.ok(is.odd(Infinity), 'infinity is odd');
  t.notOk(is.odd(0), '0 is not odd');
  t.notOk(is.odd(2), '2 is not odd');
  t.notOk(is.odd(), 'undefined is not odd');
  t.notOk(is.odd(null), 'null is not odd');
  t.notOk(is.odd(NaN), 'NaN is not odd');
  t.end();
});

test('is.ge', function (t) {
  t.ok(is.ge(3, 2), '3 is greater than 2');
  t.notOk(is.ge(2, 3), '2 is not greater than 3');
  t.ok(is.ge(3, 3), '3 is greater than or equal to 3');
  t.ok(is.ge('abc', 'a'), 'abc is greater than a');
  t.ok(is.ge('abc', 'abc'), 'abc is greater than or equal to abc');
  t.notOk(is.ge('a', 'abc'), 'a is not greater than abc');
  t.notOk(is.ge(Infinity, 0), 'infinity is not greater than anything');
  t.notOk(is.ge(0, Infinity), 'anything is not greater than infinity');
  var error = new TypeError('NaN is not a valid value');
  t['throws'](function () { return is.ge(NaN, 2); }, error, 'throws when first value is NaN');
  t['throws'](function () { return is.ge(2, NaN); }, error, 'throws when second value is NaN');
  t.end();
});

test('is.gt', function (t) {
  t.ok(is.gt(3, 2), '3 is greater than 2');
  t.notOk(is.gt(2, 3), '2 is not greater than 3');
  t.notOk(is.gt(3, 3), '3 is not greater than 3');
  t.ok(is.gt('abc', 'a'), 'abc is greater than a');
  t.notOk(is.gt('abc', 'abc'), 'abc is not greater than abc');
  t.notOk(is.gt('a', 'abc'), 'a is not greater than abc');
  t.notOk(is.gt(Infinity, 0), 'infinity is not greater than anything');
  t.notOk(is.gt(0, Infinity), 'anything is not greater than infinity');
  var error = new TypeError('NaN is not a valid value');
  t['throws'](function () { return is.gt(NaN, 2); }, error, 'throws when first value is NaN');
  t['throws'](function () { return is.gt(2, NaN); }, error, 'throws when second value is NaN');
  t.end();
});

test('is.le', function (t) {
  t.ok(is.le(2, 3), '2 is lesser than or equal to 3');
  t.notOk(is.le(3, 2), '3 is not lesser than or equal to 2');
  t.ok(is.le(3, 3), '3 is lesser than or equal to 3');
  t.ok(is.le('a', 'abc'), 'a is lesser than or equal to abc');
  t.ok(is.le('abc', 'abc'), 'abc is lesser than or equal to abc');
  t.notOk(is.le('abc', 'a'), 'abc is not lesser than or equal to a');
  t.notOk(is.le(Infinity, 0), 'infinity is not lesser than or equal to anything');
  t.notOk(is.le(0, Infinity), 'anything is not lesser than or equal to infinity');
  var error = new TypeError('NaN is not a valid value');
  t['throws'](function () { return is.le(NaN, 2); }, error, 'throws when first value is NaN');
  t['throws'](function () { return is.le(2, NaN); }, error, 'throws when second value is NaN');
  t.end();
});

test('is.lt', function (t) {
  t.ok(is.lt(2, 3), '2 is lesser than 3');
  t.notOk(is.lt(3, 2), '3 is not lesser than 2');
  t.notOk(is.lt(3, 3), '3 is not lesser than 3');
  t.ok(is.lt('a', 'abc'), 'a is lesser than abc');
  t.notOk(is.lt('abc', 'abc'), 'abc is not lesser than abc');
  t.notOk(is.lt('abc', 'a'), 'abc is not lesser than a');
  t.notOk(is.lt(Infinity, 0), 'infinity is not lesser than anything');
  t.notOk(is.lt(0, Infinity), 'anything is not lesser than infinity');
  var error = new TypeError('NaN is not a valid value');
  t['throws'](function () { return is.lt(NaN, 2); }, error, 'throws when first value is NaN');
  t['throws'](function () { return is.lt(2, NaN); }, error, 'throws when second value is NaN');
  t.end();
});

test('is.within', function (t) {
  t.test('throws on NaN', function (st) {
    var nanError = new TypeError('NaN is not a valid value');
    st['throws'](function () { return is.within(NaN, 0, 0); }, nanError, 'throws when first value is NaN');
    st['throws'](function () { return is.within(0, NaN, 0); }, nanError, 'throws when second value is NaN');
    st['throws'](function () { return is.within(0, 0, NaN); }, nanError, 'throws when third value is NaN');
    st.end();
  });

  t.test('throws on non-number', function (st) {
    var error = new TypeError('all arguments must be numbers');
    st['throws'](function () { return is.within('', 0, 0); }, error, 'throws when first value is string');
    st['throws'](function () { return is.within(0, '', 0); }, error, 'throws when second value is string');
    st['throws'](function () { return is.within(0, 0, ''); }, error, 'throws when third value is string');
    st['throws'](function () { return is.within({}, 0, 0); }, error, 'throws when first value is object');
    st['throws'](function () { return is.within(0, {}, 0); }, error, 'throws when second value is object');
    st['throws'](function () { return is.within(0, 0, {}); }, error, 'throws when third value is object');
    st['throws'](function () { return is.within(null, 0, 0); }, error, 'throws when first value is null');
    st['throws'](function () { return is.within(0, null, 0); }, error, 'throws when second value is null');
    st['throws'](function () { return is.within(0, 0, null); }, error, 'throws when third value is null');
    st['throws'](function () { return is.within(undefined, 0, 0); }, error, 'throws when first value is undefined');
    st['throws'](function () { return is.within(0, undefined, 0); }, error, 'throws when second value is undefined');
    st['throws'](function () { return is.within(0, 0, undefined); }, error, 'throws when third value is undefined');
    st.end();
  });

  t.ok(is.within(2, 1, 3), '2 is between 1 and 3');
  t.ok(is.within(0, -1, 1), '0 is between -1 and 1');
  t.ok(is.within(2, 0, Infinity), 'infinity always returns true');
  t.ok(is.within(2, Infinity, 2), 'infinity always returns true');
  t.ok(is.within(Infinity, 0, 1), 'infinity always returns true');
  t.notOk(is.within(2, -1, -1), '2 is not between -1 and 1');
  t.end();
});

test('is.object', function (t) {
  t.ok(is.object({}), 'object literal is object');
  t.notOk(is.object(), 'undefined is not an object');
  t.notOk(is.object(null), 'null is not an object');
  t.notOk(is.object(true), 'true is not an object');
  t.notOk(is.object(''), 'string is not an object');
  t.notOk(is.object(NaN), 'NaN is not an object');
  t.notOk(is.object(Object), 'object constructor is not an object');
  t.notOk(is.object(function () {}), 'function is not an object');

  t.test('Symbols', { skip: typeof Symbol !== 'function' }, function (st) {
    st.notOk(is.object(Symbol('foo')), 'symbol is not an object');
    st.end();
  });

  t.end();
});

test('is.primitive', function (t) {
  t.notOk(is.primitive({}), 'object literal is not a primitive');
  t.notOk(is.primitive([]), 'array is not a primitive');
  t.ok(is.primitive(), 'undefined is a primitive');
  t.ok(is.primitive(null), 'null is a primitive');
  t.ok(is.primitive(true), 'true is a primitive');
  t.ok(is.primitive(''), 'string is a primitive');
  t.ok(is.primitive(NaN), 'NaN is a primitive');
  t.notOk(is.primitive(Object), 'object constructor is not a primitive');
  t.notOk(is.primitive(function () {}), 'function is not a primitive');

  t.test('Symbols', { skip: typeof Symbol !== 'function' }, function (st) {
    st.ok(is.primitive(Symbol('foo')), 'symbol is a primitive');
    st.end();
  });

  t.end();
});

test('is.hash', function (t) {
  t.ok(is.hash({}), 'empty object literal is hash');
  t.ok(is.hash({ 1: 2, a: 'b' }), 'object literal is hash');
  t.notOk(is.hash(), 'undefined is not a hash');
  t.notOk(is.hash(null), 'null is not a hash');
  t.notOk(is.hash(new Date()), 'date is not a hash');
  t.notOk(is.hash(Object('')), 'string object is not a hash');
  t.notOk(is.hash(''), 'string literal is not a hash');
  t.notOk(is.hash(Object(0)), 'number object is not a hash');
  t.notOk(is.hash(1), 'number literal is not a hash');
  t.notOk(is.hash(true), 'true is not a hash');
  t.notOk(is.hash(false), 'false is not a hash');
  t.notOk(is.hash(Object(false)), 'boolean obj is not hash');
  t.notOk(is.hash(false), 'literal false is not hash');
  t.notOk(is.hash(true), 'literal true is not hash');

  t.test('commonJS environment', { skip: typeof module === 'undefined' }, function (st) {
    st.ok(is.hash(module.exports), 'module.exports is a hash');
    st.end();
  });

  t.test('browser stuff', { skip: typeof window === 'undefined' }, function (st) {
    st.notOk(is.hash(window), 'window is not a hash');
    st.notOk(is.hash(document.createElement('div')), 'element is not a hash');
    st.end();
  });

  t.test('node stuff', { skip: typeof process === 'undefined' }, function (st) {
    st.notOk(is.hash(global), 'global is not a hash');
    st.notOk(is.hash(process), 'process is not a hash');
    st.end();
  });

  t.end();
});

test('is.regexp', function (t) {
  t.ok(is.regexp(/a/g), 'regex literal is regex');
  t.ok(is.regexp(new RegExp('a', 'g')), 'regex object is regex');
  t.notOk(is.regexp(), 'undefined is not regex');
  t.notOk(is.regexp(function () {}), 'function is not regex');
  t.notOk(is.regexp('/a/g'), 'string regex is not regex');
  t.end();
});

test('is.string', function (t) {
  t.ok(is.string('foo'), 'string literal is string');
  t.ok(is.string(Object('foo')), 'string object is string');
  t.notOk(is.string(), 'undefined is not string');
  t.notOk(is.string(String), 'string constructor is not string');
  var F = function () {};
  F.prototype = Object('');
  t.notOk(is.string(F), 'string subtype is not string');
  t.end();
});

test('is.base64', function (t) {
  t.ok(is.base64('wxyzWXYZ/+=='), 'string is base64 encoded');
  t.ok(is.base64(''), 'zero length string is base64 encoded');
  t.notOk(is.base64('wxyzWXYZ123/+=='), 'string length not a multiple of four is not base64 encoded');
  t.notOk(is.base64('wxyzWXYZ1234|]=='), 'string with invalid characters is not base64 encoded');
  t.notOk(is.base64('wxyzWXYZ1234==/+'), 'string with = not at end is not base64 encoded');
  t.notOk(is.base64('wxyzWXYZ1234/==='), 'string ending with === is not base64 encoded');
  t.end();
});

test('is.hex', function (t) {
  t.ok(is.hex('abcdABCD1234'), 'string is hex encoded');
  t.ok(is.hex(''), 'zero length string is hex encoded');
  t.notOk(is.hex('wxyzWXYZ1234/+=='), 'string with invalid characters is not hex encoded');
  t.end();
});

test('is.symbol', function (t) {
  t.test('not symbols', function (st) {
    var notSymbols = [true, false, null, undefined, {}, [], function () {}, 42, NaN, Infinity, /a/g, '', 0, -0, new Error('error')];
    forEach(notSymbols, function (notSymbol) {
      st.notOk(is.symbol(notSymbol), notSymbol + ' is not symbol');
    });

    st.end();
  });

  t.test('symbols', { skip: typeof Symbol !== 'function' }, function (st) {
    st.ok(is.symbol(Symbol('foo')), 'Symbol("foo") is symbol');

    var notKnownSymbols = ['length', 'name', 'arguments', 'caller', 'prototype', 'for', 'keyFor'];
    var symbolKeys = Object.getOwnPropertyNames(Symbol).filter(function (name) {
      return notKnownSymbols.indexOf(name) < 0;
    });
    forEach(symbolKeys, function (symbolKey) {
      st.ok(is.symbol(Symbol[symbolKey]), symbolKey + ' is symbol');
    });

    st.end();
  });

  t.end();
});

test('is.bigint', function (t) {
  t.test('not bigints', function (st) {
    var notBigints = [true, false, null, undefined, {}, [], function () {}, 42, NaN, Infinity, /a/g, '', 0, -0, new Error('error')];
    forEach(notBigints, function (notBigint) {
      st.notOk(is.bigint(notBigint), notBigint + ' is not bigint');
    });

    st.end();
  });

  t.test('bigints', { skip: typeof BigInt !== 'function' }, function (st) {
    var bigInts = [
      Function('return 42n')(), // eslint-disable-line no-new-func
      BigInt(42)
    ];
    forEach(bigInts, function (bigInt) {
      st.ok(is.bigint(bigInt), bigInt + ' is bigint');
    });

    st.end();
  });

  t.end();
});
