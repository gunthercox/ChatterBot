'use strict';

((context, factory) => {
  if (
    typeof require === 'function' &&
    typeof exports === 'object' &&
    typeof module === 'object'
  ) {
    // Node.js
    module.exports = factory(require('immutable'));
  } else {
    // Other environments (usually <script> tag)
    context.chai.use(factory(context.Immutable));
  }
})(this, Immutable => (chai, utils) => {
  function isImmutable(value) {
    if (typeof Immutable.isImmutable === 'undefined') {
      return Immutable.Iterable.isIterable(value);
    } else {
      return Immutable.isImmutable(value);
    }
  }

  const { Assertion } = chai;

  function assertIsIterable(obj) {
    new Assertion(obj).assert(
      Immutable.Iterable.isIterable(obj),
      'expected #{this} to be an Iterable'
    );
  }

  /**
   * ## BDD API Reference
   */

  /**
   * ### .empty
   *
   * Asserts that the immutable collection is empty.
   *
   * ```js
   * expect(List()).to.be.empty;
   * expect(List.of(1, 2, 3)).to.not.be.empty;
   * ```
   *
   * @name empty
   * @namespace BDD
   * @api public
   */

  Assertion.overwriteProperty(
    'empty',
    _super =>
      function() {
        const obj = this._obj;

        if (Immutable.Iterable.isIterable(obj)) {
          const { size } = obj;
          new Assertion(size).a('number');

          this.assert(
            size === 0,
            'expected #{this} to be empty but got size #{act}',
            'expected #{this} to not be empty'
          );
        } else {
          _super.apply(this, arguments);
        }
      }
  );

  /**
   * ### .equal(collection)
   *
   * Asserts that the values of the target are equivalent to the values of
   * `collection`. Aliases of Chai's original `equal` method are also supported.
   *
   * ```js
   * const a = List.of(1, 2, 3);
   * const b = List.of(1, 2, 3);
   * expect(a).to.equal(b);
   * ```
   *
   * Immutable data structures should only contain other immutable data
   * structures (unlike `Array`s and `Object`s) to be considered immutable and
   * properly work against `.equal()`. See
   * [issue #24](https://github.com/astorije/chai-immutable/issues/24) for more
   * information.
   *
   * Also, note that `deep.equal` and `eql` are synonyms of `equal` when
   * tested against immutable data structures, therefore they are aliases to
   * `equal`.
   *
   * @name equal
   * @alias equals
   * @alias eq
   * @alias eql
   * @alias eqls
   * @alias deep.equal
   * @param {Collection} value
   * @namespace BDD
   * @api public
   */

  function assertImmutableEqual(_super) {
    return function(collection) {
      const obj = this._obj;

      if (isImmutable(obj)) {
        this.assert(
          Immutable.is(obj, collection),
          'expected #{act} to equal #{exp}',
          'expected #{act} to not equal #{exp}',
          collection.toJS(),
          obj.toJS(),
          true
        );
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  Assertion.overwriteMethod('equal', assertImmutableEqual);
  Assertion.overwriteMethod('equals', assertImmutableEqual);
  Assertion.overwriteMethod('eq', assertImmutableEqual);
  Assertion.overwriteMethod('eql', assertImmutableEqual);
  Assertion.overwriteMethod('eqls', assertImmutableEqual);

  /**
   * ### .referenceEqual(value)
   *
   * Asserts that the reference of the target is equivalent to the reference of
   * `collection`. This method preserves the original behavior of Chai's `equal`.
   *
   * See [issue #210](https://github.com/astorije/chai-immutable/issues/210) for
   * more details.
   *
   * ```js
   * const a = List.of(1, 2, 3);
   * const b = a;
   * const c = List.of(1, 2, 3);
   * expect(a).to.referenceEqual(b);
   * expect(a).to.not.referenceEqual(c);
   * ```
   *
   * @name referenceEqual
   * @param {Collection} value
   * @namespace BDD
   * @api public
   */

  function assertCollectionReferenceEqual() {
    return function(collection) {
      const obj = this._obj;

      this.assert(
        obj === collection,
        'expected #{act} reference to equal #{exp}',
        'expected #{act} reference to not equal #{exp}',
        collection.toJS(),
        obj.toJS(),
        true
      );
    };
  }

  Assertion.addMethod('referenceEqual', assertCollectionReferenceEqual);

  /**
   * ### .include(value)
   *
   * The `include` and `contain` assertions can be used as either property
   * based language chains or as methods to assert the inclusion of a value or subset
   * in an immutable collection. When used as language chains, they toggle the
   * `contains` flag for the `keys` assertion.
   *
   * Note that `deep.include` behaves exactly like `include` in the context of
   * immutable data structures.
   *
   * ```js
   * expect(new List([1, 2, 3])).to.include(2);
   * expect(new List([1, 2, 3])).to.deep.include(2);
   * expect(new Map({ foo: 'bar', hello: 'world' })).to.include('bar');
   * expect(new Map({ a: 1, b: 2, c: 3 })).to.include(new Map({ a: 1, b: 2 }));
   * expect(new Map({ foo: 'bar', hello: 'world' })).to.include.keys('foo');
   * ```
   *
   * @name include
   * @alias contain
   * @alias includes
   * @alias contains
   * @param {Mixed} val
   * @namespace BDD
   * @api public
   */

  function assertCollectionInclude(_super) {
    return function(val) {
      const obj = this._obj;

      if (Immutable.Iterable.isIterable(obj)) {
        const isIncluded =
          obj.includes(val) ||
          (Immutable.Iterable.isIterable(val) && obj.isSuperset(val));
        this.assert(
          isIncluded,
          'expected #{act} to include #{exp}',
          'expected #{act} to not include #{exp}',
          val,
          obj.toString()
        );
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  function chainCollectionInclude(_super) {
    return function() {
      _super.apply(this, arguments);
    };
  }

  ['include', 'contain', 'contains', 'includes'].forEach(keyword => {
    Assertion.overwriteChainableMethod(
      keyword,
      assertCollectionInclude,
      chainCollectionInclude
    );
  });

  /**
   * ### .keys(key1[, key2[, ...]])
   *
   * Asserts that the target collection has the given keys.
   *
   * When the target is an object or array, keys can be provided as one or more
   * string arguments, a single array argument, a single object argument, or an
   * immutable collection. In the last 2 cases, only the keys in the given
   * object/collection matter; the values are ignored.
   *
   * ```js
   * expect(new Map({ foo: 1, bar: 2 })).to.have.all.keys('foo', 'bar');
   * expect(new Map({ foo: 1, bar: 2 })).to.have.all.keys(new List(['bar', 'foo']));
   * expect(new Map({ foo: 1, bar: 2 })).to.have.all.keys(new Set(['bar', 'foo']));
   * expect(new Map({ foo: 1, bar: 2 })).to.have.all.keys(new Stack(['bar', 'foo']));
   * expect(new List(['x', 'y'])).to.have.all.keys(0, 1);
   *
   * expect(new Map({ foo: 1, bar: 2 })).to.have.all.keys(['foo', 'bar']);
   * expect(new List(['x', 'y'])).to.have.all.keys([0, 1]);
   *
   * // Values in the passed object are ignored:
   * expect(new Map({ foo: 1, bar: 2 })).to.have.all.keys({ 'bar': 6, 'foo': 7 });
   * expect(new Map({ foo: 1, bar: 2 })).to.have.all.keys(new Map({ 'bar': 6, 'foo': 7 }));
   * expect(new List(['x', 'y'])).to.have.all.keys({0: 4, 1: 5});
   * ```
   *
   * Note that `deep.property` behaves exactly like `property` in the context of
   * immutable data structures.
   *
   * By default, the target must have all of the given keys and no more. Add
   * `.any` earlier in the chain to only require that the target have at least
   * one of the given keys. Also, add `.not` earlier in the chain to negate
   * `.keys`. It's often best to add `.any` when negating `.keys`, and to use
   * `.all` when asserting `.keys` without negation.
   *
   * When negating `.keys`, `.any` is preferred because `.not.any.keys` asserts
   * exactly what's expected of the output, whereas `.not.all.keys` creates
   * uncertain expectations.
   *
   * ```js
   * // Recommended; asserts that target doesn't have any of the given keys
   * expect(new Map({a: 1, b: 2})).to.not.have.any.keys('c', 'd');
   *
   * // Not recommended; asserts that target doesn't have all of the given
   * // keys but may or may not have some of them
   * expect(new Map({a: 1, b: 2})).to.not.have.all.keys('c', 'd');
   * ```
   *
   * When asserting `.keys` without negation, `.all` is preferred because
   * `.all.keys` asserts exactly what's expected of the output, whereas
   * `.any.keys` creates uncertain expectations.
   *
   * ```js
   * // Recommended; asserts that target has all the given keys
   * expect(new Map({a: 1, b: 2})).to.have.all.keys('a', 'b');
   *
   * // Not recommended; asserts that target has at least one of the given
   * // keys but may or may not have more of them
   * expect(new Map({a: 1, b: 2})).to.have.any.keys('a', 'b');
   * ```
   *
   * Note that `.all` is used by default when neither `.all` nor `.any` appear
   * earlier in the chain. However, it's often best to add `.all` anyway because
   * it improves readability.
   *
   * ```js
   * // Both assertions are identical
   * expect(new Map({a: 1, b: 2})).to.have.all.keys('a', 'b'); // Recommended
   * expect(new Map({a: 1, b: 2})).to.have.keys('a', 'b'); // Not recommended
   * ```
   *
   * Add `.include` earlier in the chain to require that the target's keys be a
   * superset of the expected keys, rather than identical sets.
   *
   * ```js
   * // Target object's keys are a superset of ['a', 'b'] but not identical
   * expect(new Map({a: 1, b: 2, c: 3})).to.include.all.keys('a', 'b');
   * expect(new Map({a: 1, b: 2, c: 3})).to.not.have.all.keys('a', 'b');
   * ```
   *
   * However, if `.any` and `.include` are combined, only the `.any` takes
   * effect. The `.include` is ignored in this case.
   *
   * ```js
   * // Both assertions are identical
   * expect(new Map({a: 1})).to.have.any.keys('a', 'b');
   * expect(new Map({a: 1})).to.include.any.keys('a', 'b');
   * ```
   *
   * The alias `.key` can be used interchangeably with `.keys`.
   *
   * ```js
   * expect(new Map({ foo: 1 })).to.have.key('foo');
   * ```
   *
   * @name keys
   * @alias key
   * @alias deep.key
   * @param {...String|Array|Object|Collection} keys
   * @namespace BDD
   * @api public
   */

  function assertKeyedCollectionKeys(_super) {
    return function(keys) {
      const obj = this._obj;

      if (Immutable.Iterable.isIterable(obj)) {
        const ssfi = utils.flag(this, 'ssfi');

        switch (utils.type(keys)) {
          case 'Object':
            if (Immutable.Iterable.isIndexed(keys)) {
              keys = keys.toJS();
            } else if (Immutable.Iterable.isIterable(keys)) {
              keys = keys.keySeq().toJS();
            } else {
              keys = Object.keys(keys);
            }
          // `keys` is now an array so this statement safely falls through
          case 'Array':
            if (arguments.length > 1) {
              throw new chai.AssertionError(
                'when testing keys against an immutable collection, you must ' +
                  'give a single Array|Object|String|Collection argument or ' +
                  'multiple String arguments',
                null,
                ssfi
              );
            }
            break;
          default:
            keys = Array.prototype.slice.call(arguments);
            break;
        }

        // Only stringify non-Symbols because Symbols would become "Symbol()"
        keys = keys.map(val => (typeof val === 'symbol' ? val : String(val)));

        if (!keys.length) {
          throw new chai.AssertionError('keys required', null, ssfi);
        }

        let all = utils.flag(this, 'all');
        const any = utils.flag(this, 'any');
        const contains = utils.flag(this, 'contains');
        let ok;
        let str = contains ? 'contain ' : 'have ';

        if (!any && !all) {
          all = true;
        }

        if (any) {
          ok = keys.some(key => obj.has(key));
        } else {
          ok = keys.every(key => obj.has(key));

          if (!contains) {
            ok = ok && keys.length === obj.count();
          }
        }

        if (keys.length > 1) {
          keys = keys.map(utils.inspect);
          const last = keys.pop();
          const conjunction = any ? 'or' : 'and';
          str += `keys ${keys.join(', ')}, ${conjunction} ${last}`;
        } else {
          str += `key ${utils.inspect(keys[0])}`;
        }

        this.assert(
          ok,
          `expected #{act} to ${str}`,
          `expected #{act} to not ${str}`,
          keys.slice(0).sort(utils.compareByInspect),
          obj.toString(),
          true
        );
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  Assertion.overwriteMethod('keys', assertKeyedCollectionKeys);
  Assertion.overwriteMethod('key', assertKeyedCollectionKeys);

  /**
   * ## parsePath(path)
   *
   * Helper function used to parse string paths into arrays of keys and
   * indices.
   *
   * ```js
   * const parsed = parsePath('myobject.key.subkey');
   * ```
   *
   * ### Paths:
   *
   * - Can be as near infinitely deep and nested
   * - Arrays are also valid using the formal `myobject.document[3].key`.
   * - Literal dots and brackets (not delimiter) must be backslash-escaped.
   *
   * This function is inspired from Chai's original `parsePath` function:
   * https://github.com/chaijs/chai/blob/d664ef4/lib/chai/utils/getPathInfo.js#L46-L74
   *
   * @param {String} path
   * @returns {Array} parsed
   * @api private
   */
  function parsePath(path) {
    // Given the following path: 'a.b[1]'
    // Separates keys followed by indices with a dot: 'a.b.[1]'
    const str = path.replace(/([^\\])\[/g, '$1.[');
    // Extracts all indices and keys into an array: ['a', 'b', '[1]']
    const parts = str.match(/(\\\.|[^.]+?)+/g);

    // Removes brackets and escaping backslashes, and extracts digits from
    // each value in the array: ['a', 'b', 1]
    return parts.map(value => {
      // Extracts indices wrapped in brackets
      const re = /^\[(\d+)\]$/;
      // Builds ['[<index>]', '<index>'] if value is a digit, null otherwise
      const mArr = re.exec(value);

      // If the value was of form '[<index>]', returns <index>
      // Otherwise, returns the key without the escaping backslashes
      if (mArr) {
        return parseFloat(mArr[1]);
      } else {
        return value.replace(/\\([.[\]])/g, '$1');
      }
    });
  }

  /**
   * ### .property(path[, val])
   *
   * Asserts that the target has a property with the given `path`.
   *
   * ```js
   * expect(new Map({a: 1})).to.have.property('a');
   * ```
   *
   * When `val` is provided, `.property` also asserts that the property's value
   * is equal to the given `val`. `val` can be an immutable collection.
   *
   * ```js
   * expect(new Map({a: 1})).to.have.property('a', 1);
   * ```
   *
   * Note that `deep.property` behaves exactly like `property` in the context of
   * immutable data structures.
   *
   * Add `.nested` earlier in the chain to enable dot- and bracket-notation when
   * referencing nested properties. An immutable `List` can also be used as the
   * starting point of a `nested.property`.
   *
   * ```js
   * expect(Immutable.fromJS({a: {b: ['x', 'y']}})).to.have.nested.property('a.b[1]');
   * expect(Immutable.fromJS({a: {b: ['x', 'y']}})).to.have.nested.property('a.b[1]', 'y');
   * expect(Immutable.fromJS({a: {b: ['x', 'y']}})).to.have.nested.property(['a', 'b', 1], 'y');
   * expect(Immutable.fromJS({a: {b: ['x', 'y']}})).to.have.nested.property(new List(['a', 'b', 1]), 'y');
   * ```
   *
   * If `.` or `[]` are part of an actual property name, they can be escaped by
   * adding two backslashes before them.
   *
   * ```js
   * expect(Immutable.fromJS({'.a': {'[b]': 'x'}})).to.have.nested.property('\\.a.\\[b\\]');
   * ```
   *
   * Add `.not` earlier in the chain to negate `.property`.
   *
   * ```js
   * expect(new Map({a: 1})).to.not.have.property('b');
   * ```
   *
   * However, it's dangerous to negate `.property` when providing `val`. The
   * problem is that it creates uncertain expectations by asserting that the
   * target either doesn't have a property at the given `path`, or that it
   * does have a property at the given key `path` but its value isn't equal to
   * the given `val`. It's often best to identify the exact output that's
   * expected, and then write an assertion that only accepts that exact output.
   *
   * When the target isn't expected to have a property at the given
   * `path`, it's often best to assert exactly that.
   *
   * ```js
   * expect(new Map({b: 2})).to.not.have.property('a'); // Recommended
   * expect(new Map({b: 2})).to.not.have.property('a', 1); // Not recommended
   * ```
   *
   * When the target is expected to have a property at the given key `path`,
   * it's often best to assert that the property has its expected value, rather
   * than asserting that it doesn't have one of many unexpected values.
   *
   * ```js
   * expect(new Map({a: 3})).to.have.property('a', 3); // Recommended
   * expect(new Map({a: 3})).to.not.have.property('a', 1); // Not recommended
   * ```
   *
   * `.property` changes the target of any assertions that follow in the chain
   * to be the value of the property from the original target object.
   *
   * ```js
   * expect(new Map({a: 1})).to.have.property('a').that.is.a('number');
   * ```
   *
   * @name property
   * @alias deep.equal
   * @param {String|Array|Iterable} path
   * @param {Mixed} val (optional)
   * @returns value of property for chaining
   * @namespace BDD
   * @api public
   */

  function assertProperty(_super) {
    return function(path, val) {
      const obj = this._obj;

      if (Immutable.Iterable.isIterable(obj)) {
        const isNested = utils.flag(this, 'nested');
        const negate = utils.flag(this, 'negate');

        let descriptor;
        let hasProperty;
        let value;

        if (isNested) {
          descriptor = 'nested ';
          if (typeof path === 'string') {
            path = parsePath(path);
          }
          value = obj.getIn(path);
          hasProperty = obj.hasIn(path);
        } else {
          value = obj.get(path);
          hasProperty = obj.has(path);
        }

        // When performing a negated assertion for both name and val, merely
        // having a property with the given name isn't enough to cause the
        // assertion to fail. It must both have a property with the given name,
        // and the value of that property must equal the given val. Therefore,
        // skip this assertion in favor of the next.
        if (!negate || arguments.length === 1) {
          this.assert(
            hasProperty,
            `expected #{this} to have ${descriptor}property ` +
              `${utils.inspect(path)}`,
            `expected #{this} to not have ${descriptor}property ` +
              `${utils.inspect(path)}`
          );
        }

        if (arguments.length > 1) {
          let isEqual;
          if (Immutable.Iterable.isIterable(val)) {
            isEqual = Immutable.is(val, value);
          } else {
            isEqual = val === value;
          }

          this.assert(
            hasProperty && isEqual,
            `expected #{this} to have ${descriptor}property ` +
              `${utils.inspect(path)} of #{exp}, but got #{act}`,
            `expected #{this} to not have ${descriptor}property ` +
              `${utils.inspect(path)} of #{act}`,
            val,
            value
          );
        }

        utils.flag(this, 'object', value);
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  Assertion.overwriteMethod('property', assertProperty);

  /**
   * ### .size(value)
   *
   * Asserts that the immutable collection has the expected size.
   *
   * ```js
   * expect(List.of(1, 2, 3)).to.have.size(3);
   * ```
   *
   * It can also be used as a chain precursor to a value comparison for the
   * `size` property.
   *
   * ```js
   * expect(List.of(1, 2, 3)).to.have.size.least(3);
   * expect(List.of(1, 2, 3)).to.have.size.most(3);
   * expect(List.of(1, 2, 3)).to.have.size.above(2);
   * expect(List.of(1, 2, 3)).to.have.size.below(4);
   * expect(List.of(1, 2, 3)).to.have.size.within(2,4);
   * ```
   *
   * Similarly to `length`/`lengthOf`, `sizeOf` is an alias of `size`:
   *
   * ```js
   * expect(List.of(1, 2, 3)).to.have.sizeOf(3);
   * ```
   *
   * @name size
   * @alias sizeOf
   * @param {Number} size
   * @namespace BDD
   * @api public
   */

  function assertCollectionSize(n) {
    assertIsIterable(this._obj);

    const { size } = this._obj;
    new Assertion(size).a('number');

    this.assert(
      size === n,
      'expected #{this} to have size #{exp} but got #{act}',
      'expected #{this} to not have size #{act}',
      n,
      size
    );
  }

  function chainCollectionSize() {
    utils.flag(this, 'immutable.collection.size', true);
  }

  Assertion.addChainableMethod(
    'size',
    assertCollectionSize,
    chainCollectionSize
  );
  Assertion.addMethod('sizeOf', assertCollectionSize);

  // Numerical comparator overwrites

  function assertCollectionSizeLeast(_super) {
    return function(n) {
      if (utils.flag(this, 'immutable.collection.size')) {
        assertIsIterable(this._obj);

        const { size } = this._obj;
        new Assertion(size).a('number');

        this.assert(
          size >= n,
          'expected #{this} to have a size of at least #{exp} but got #{act}',
          'expected #{this} to not have a size of at least #{exp} but got ' +
            '#{act}',
          n,
          size
        );
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  function assertCollectionSizeMost(_super) {
    return function(n) {
      if (utils.flag(this, 'immutable.collection.size')) {
        assertIsIterable(this._obj);

        const { size } = this._obj;
        new Assertion(size).a('number');

        this.assert(
          size <= n,
          'expected #{this} to have a size of at most #{exp} but got #{act}',
          'expected #{this} to not have a size of at most #{exp} but got ' +
            '#{act}',
          n,
          size
        );
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  function assertCollectionSizeAbove(_super) {
    return function(n) {
      if (utils.flag(this, 'immutable.collection.size')) {
        assertIsIterable(this._obj);

        const { size } = this._obj;
        new Assertion(size).a('number');

        this.assert(
          size > n,
          'expected #{this} to have a size above #{exp} but got #{act}',
          'expected #{this} to not have a size above #{exp} but got #{act}',
          n,
          size
        );
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  function assertCollectionSizeBelow(_super) {
    return function(n) {
      if (utils.flag(this, 'immutable.collection.size')) {
        assertIsIterable(this._obj);

        const { size } = this._obj;
        new Assertion(size).a('number');

        this.assert(
          size < n,
          'expected #{this} to have a size below #{exp} but got #{act}',
          'expected #{this} to not have a size below #{exp} but got #{act}',
          n,
          size
        );
      } else {
        _super.apply(this, arguments);
      }
    };
  }

  Assertion.overwriteMethod('least', assertCollectionSizeLeast);
  Assertion.overwriteMethod('gte', assertCollectionSizeLeast);

  Assertion.overwriteMethod('most', assertCollectionSizeMost);
  Assertion.overwriteMethod('lte', assertCollectionSizeMost);

  Assertion.overwriteMethod('above', assertCollectionSizeAbove);
  Assertion.overwriteMethod('gt', assertCollectionSizeAbove);
  Assertion.overwriteMethod('greaterThan', assertCollectionSizeAbove);

  Assertion.overwriteMethod('below', assertCollectionSizeBelow);
  Assertion.overwriteMethod('lt', assertCollectionSizeBelow);
  Assertion.overwriteMethod('lessThan', assertCollectionSizeBelow);

  Assertion.overwriteMethod(
    'within',
    _super =>
      function(min, max) {
        if (utils.flag(this, 'immutable.collection.size')) {
          assertIsIterable(this._obj);

          const { size } = this._obj;
          new Assertion(size).a('number');

          this.assert(
            min <= size && size <= max,
            'expected #{this} to have a size within #{exp} but got #{act}',
            'expected #{this} to not have a size within #{exp} but got #{act}',
            `${min}..${max}`,
            size
          );
        } else {
          _super.apply(this, arguments);
        }
      }
  );

  /**
   * ## TDD API Reference
   */

  const { assert } = chai;
  const originalEqual = assert.equal;
  const originalNotEqual = assert.notEqual;

  /**
   * ### .equal(actual, expected)
   *
   * Asserts that the values of `actual` are equivalent to the values of
   * `expected`. Note that `.strictEqual()` and `.deepEqual()` assert
   * exactly like `.equal()` in the context of Immutable data structures.
   *
   * ```js
   * const a = List.of(1, 2, 3);
   * const b = List.of(1, 2, 3);
   * assert.equal(a, b);
   * ```
   *
   * Immutable data structures should only contain other immutable data
   * structures (unlike `Array`s and `Object`s) to be considered immutable and
   * properly work against `.equal()`, `.strictEqual()` or `.deepEqual()`. See
   * [issue #24](https://github.com/astorije/chai-immutable/issues/24) for more
   * information.
   *
   * @name equal
   * @param {Collection} actual
   * @param {Collection} expected
   * @namespace Assert
   * @api public
   */

  assert.equal = (actual, expected) => {
    // It seems like we shouldn't actually need this check, however,
    // `assert.equal` actually behaves differently than its BDD counterpart!
    // Namely, the BDD version is strict while the "assert" one isn't.
    if (Immutable.Iterable.isIterable(actual)) {
      return new Assertion(actual).equal(expected);
    } else {
      return originalEqual(actual, expected);
    }
  };

  /**
   * ### .referenceEqual(actual, expected)
   *
   * Asserts that the reference of `actual` is equivalent to the reference of
   * `expected`. This method preserves the original behavior of Chai's `equal`.
   *
   * See [issue #210](https://github.com/astorije/chai-immutable/issues/210) for
   * more details.
   *
   * ```js
   * const a = List.of(1, 2, 3);
   * const b = a;
   * const c = List.of(1, 2, 3);
   * assert.referenceEqual(a, b);
   * assert.throws(() => assert.referenceEqual(a, c));
   * ```
   *
   * @name referenceEqual
   * @param {Collection} actual
   * @param {Collection} expected
   * @namespace Assert
   * @api public
   */

  assert.referenceEqual = originalEqual;

  /**
   * ### .notEqual(actual, expected)
   *
   * Asserts that the values of `actual` are not equivalent to the values of
   * `expected`. Note that `.notStrictEqual()` and `.notDeepEqual()` assert
   * exactly like `.notEqual()` in the context of Immutable data structures.
   *
   * ```js
   * const a = List.of(1, 2, 3);
   * const b = List.of(4, 5, 6);
   * assert.notEqual(a, b);
   * ```
   *
   * @name notEqual
   * @param {Collection} actual
   * @param {Collection} expected
   * @namespace Assert
   * @api public
   */

  assert.notEqual = (actual, expected) => {
    if (Immutable.Iterable.isIterable(actual)) {
      return new Assertion(actual).not.equal(expected);
    } else {
      return originalNotEqual(actual, expected);
    }
  };

  /**
   * ### .notReferenceEqual(actual, expected)
   *
   * Asserts that the reference of `actual` is not equivalent to the reference of
   * `expected`. This method preserves the original behavior of Chai's `notEqual`.
   *
   * See [issue #210](https://github.com/astorije/chai-immutable/issues/210) for
   * more details.
   *
   * ```js
   * const a = List.of(1, 2, 3);
   * const b = a;
   * const c = List.of(1, 2, 3);
   * assert.throws(() => assert.notReferenceEqual(a, b));
   * assert.notReferenceEqual(a, c);
   * ```
   *
   * @name notReferenceEqual
   * @param {Collection} actual
   * @param {Collection} expected
   * @namespace Assert
   * @api public
   */

  assert.notReferenceEqual = originalNotEqual;

  /**
   * ### .sizeOf(collection, length)
   *
   * Asserts that the immutable collection has the expected size.
   *
   * ```js
   * assert.sizeOf(List.of(1, 2, 3), 3);
   * assert.sizeOf(new List(), 0);
   * ```
   *
   * @name sizeOf
   * @param {Collection} collection
   * @param {Number} size
   * @namespace Assert
   * @api public
   */

  assert.sizeOf = (collection, expected) => {
    new Assertion(collection).size(expected);
  };
});
