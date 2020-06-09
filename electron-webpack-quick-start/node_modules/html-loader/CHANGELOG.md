# Change Log

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

<a name="1.0.0-alpha.0"></a>
# [1.0.0-alpha.0](https://github.com/webpack-contrib/html-loader/compare/v0.5.5...v1.0.0-alpha.0) (2018-02-06)


### Code Refactoring

* apply `webpack-defaults` ([#134](https://github.com/webpack-contrib/html-loader/issues/134)) ([4f28e16](https://github.com/webpack-contrib/html-loader/commit/4f28e16))


### Features

* **index:** add `<import src="./file.html">` (HTML Imports) support (`options.import`) ([b8ec2d4](https://github.com/webpack-contrib/html-loader/commit/b8ec2d4))
* **index:** add `<import>` filter support (`options.import`) ([#163](https://github.com/webpack-contrib/html-loader/issues/163)) ([6da1dce](https://github.com/webpack-contrib/html-loader/commit/6da1dce))
* **index:** add `options` validation (`schema-utils`) ([6a52f85](https://github.com/webpack-contrib/html-loader/commit/6a52f85))
* **index:** add `url` filter support (`options.url`) ([#162](https://github.com/webpack-contrib/html-loader/issues/162)) ([9e3871f](https://github.com/webpack-contrib/html-loader/commit/9e3871f))
* **index:** add asset resolving (HTML URLs) support (`options.url`) ([82e094b](https://github.com/webpack-contrib/html-loader/commit/82e094b))
* **index:** use `posthtml` for HTML processing ([ac18b3d](https://github.com/webpack-contrib/html-loader/commit/ac18b3d))


### BREAKING CHANGES

* requires `node >= v6.0.0`
* requires `webpack >= v3.0.0`



<a name="0.5.5"></a>
## [0.5.5](https://github.com/webpack-contrib/html-loader/compare/v0.5.4...v0.5.5) (2018-01-17)


### Bug Fixes

* **index:** don't prepend `./` to the URL on `interpolate=require` (`options.interpolate`) ([#165](https://github.com/webpack-contrib/html-loader/issues/165)) ([9515410](https://github.com/webpack-contrib/html-loader/commit/9515410))



<a name="0.5.4"></a>
## [0.5.4](https://github.com/webpack-contrib/html-loader/compare/v0.5.1...v0.5.4) (2018-01-05)


### Bug Fixes

* ignore attribute if `mailto:` is present ([#145](https://github.com/webpack-contrib/html-loader/issues/145)) ([4b13d4c](https://github.com/webpack-contrib/html-loader/commit/4b13d4c))
* **index:** escape double quotes correctly (`options.interpolate`) ([#154](https://github.com/webpack-contrib/html-loader/issues/154)) ([1ef5de4](https://github.com/webpack-contrib/html-loader/commit/1ef5de4))


<a name="0.5.1"></a>
## [0.5.1](https://github.com/webpack/html-loader/compare/v0.5.0...v0.5.1) (2017-08-08)


### Bug Fixes

* Support for empty tags in tag-attribute matching ([#133](https://github.com/webpack/html-loader/issues/133)) ([6efa6de](https://github.com/webpack/html-loader/commit/6efa6de)), closes [#129](https://github.com/webpack/html-loader/issues/129)



<a name="0.5.0"></a>
# [0.5.0](https://github.com/webpack/html-loader/compare/v0.4.3...v0.5.0) (2017-07-26)


### Features

* add support for empty tags in `tag:attribute` matching ([#129](https://github.com/webpack/html-loader/issues/129)) ([70370dc](https://github.com/webpack/html-loader/commit/70370dc))


<a name="0.4.5"></a>
## [0.4.5](https://github.com/webpack/html-loader/compare/v0.4.3...v0.4.5) (2017-07-26)


### Bug Fixes

* es6 default export ([fae0309](https://github.com/webpack/html-loader/commit/fae0309))
* Handle es6 default export ([e04e969](https://github.com/webpack/html-loader/commit/e04e969))
* **getOptions:** deprecation warn in loaderUtils ([#114](https://github.com/webpack/html-loader/issues/114)) ([3d47e98](https://github.com/webpack/html-loader/commit/3d47e98))


### Features

* Adds exportAsDefault ([37d40d8](https://github.com/webpack/html-loader/commit/37d40d8))
