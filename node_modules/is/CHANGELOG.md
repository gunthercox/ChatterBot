3.3.0 / 2018-12-14
==================
  * [New] add `is.bigint` (#36)
  * [Docs] change jsdoc comments "Mixed" to wildcards (#34)
  * [Tests] up to `node` `v11.4`, `v10.14`, `v9.11`, `v8.14`, `v7.10`, `v6.15`, `v4.9`; use `nvm install-latest-npm`
  * [Dev Deps] update `eslint`, `@ljharb/eslint-config`, `safe-publish-latest`, `tape`

3.2.1 / 2017-02-27
==================
  * [Fix] `is.fn`: recognize generator and async functions too (#28)
  * [Tests] up to `node` `v7.5`, `v4.7`; improve test matrix
  * [Dev Deps] update `@ljharb/eslint-config`, `eslint`, `tape`
  * [Docs] improve readme formatting (#27)

3.2.0 / 2016-10-24
==================
  * [Fix] fix infinite loop when comparing two empty arrays + fix skipping first element (#24, #25)
  * [New] add `is.primitive`
  * [New] Add `is.date.valid` function and tests (#19)
  * [Tests] use `pretest` for `npm run lint`; add `npm run tests-only`
  * [Tests] up to `node` `v4.6`, `v5.12`, `v6.9`; improve test matrix
  * [Tests] fix description (#18)
  * [Dev Deps] update `tape`, `jscs`, `eslint`, `@ljharb/eslint-config`

3.1.0 / 2015-09-20
==================
  * [Enhancement]: `is.array`: Prefer `Array.isArray` when present
  * [Fix] Deprecate `is.boolean`/`is.int` (ES3 syntax errors)
  * [Docs] Switch from vb.teelaun.ch to versionbadg.es for the npm version badge SVG
  * [Refactor] Don't use yoda conditions
  * [Refactor] `is.equal` can return earlier in some cases (#16)
  * [Tests] Quote "throws" (ES3 syntax error)
  * [Tests] up to `io.js` `v3.3`, up to `node` `v4.1`
  * [Dev Deps] add `npm run eslint`
  * [Dev Deps] update `tape`, `covert`, `jscs`

3.0.1 / 2015-02-22
==================
  * Version bump to resolve npm bug with v3.0.0

3.0.0 / 2015-02-21
==================
  * is.empty should return true for falsy values ([#13](https://github.com/enricomarino/is/issues/13), [#14](https://github.com/enricomarino/is/issues/14))
  * All grade A-supported `node`/`iojs` versions now ship with an `npm` that understands `^`.
  * Test on `iojs` `v1.2` and `v1.3`, `node` `v0.12`; speed up builds; allow failures on all but two latest minor versions.
  * Update `jscs`

2.2.1 / 2015-02-06
==================
  * Update `tape`, `jscs`
  * `toString` breaks in some browsers; using `toStr` instead.

2.2.0 / 2014-11-29
==================
  * Update `tape`, `jscs`
  * Add `is.symbol`

2.1.0 / 2014-10-21
==================
  * Add `CHANGELOG.md`
  * Add `is.hex` and `is.base64` [#12](https://github.com/enricomarino/is/issues/12)
  * Update `tape`, `jscs`
  * Lock `covert` to v1.0.0 [substack/covert#9](https://github.com/substack/covert/issues/9)

2.0.2 / 2014-10-05
==================
  * `undefined` can be redefined in ES3 browsers.
  * Update `jscs.json` and make style consistent
  * Update `foreach`, `jscs`, `tape`
  * Naming URLs in README

2.0.1 / 2014-09-02
==================
  * Add the license to package.json
  * Add license and downloads badges
  * Update `jscs`

2.0.0 / 2014-08-25
==================
  * Add `make release`
  * Update copyright notice.
  * Fix is.empty(new String())

1.1.0 / 2014-08-22
==================
  * Removing redundant license
  * Add a non-deprecated method for is.null
  * Use a more reliable valueOf coercion for is.false/is.true
  * Clean up `README.md`
  * Running `npm run lint` as part of tests.
  * Fixing lint errors.
  * Adding `npm run lint`
  * Updating `covert`

1.0.0 / 2014-08-07
==================
  * Update `tape`, `covert`
  * Increase code coverage
  * Update `LICENSE.md`, `README.md`

0.3.0 / 2014-03-02
==================
  * Update `tape`, `covert`
  * Adding `npm run coverage`
  * is.arguments -> is.args, because reserved words.
  * "undefined" is a reserved word in ES3 browsers.
  * Optimizing is.equal to return early if value and other are strictly equal.
  * Fixing is.equal for objects.
  * Test improvements

0.2.7 / 2013-12-26
==================
  * Update `tape`, `foreach`
  * is.decimal(Infinity) shouldn't be true [#11](https://github.com/enricomarino/is/issues/11)

0.2.6 / 2013-05-06
==================
  * Fix lots of tests [#9](https://github.com/enricomarino/is/issues/9)
  * Update tape [#8](https://github.com/enricomarino/is/issues/8)

0.2.5 / 2013-04-24
==================
  * Use `tap` instead of `tape` [#7](https://github.com/enricomarino/is/issues/7)

