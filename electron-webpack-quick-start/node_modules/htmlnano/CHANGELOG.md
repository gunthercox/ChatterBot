# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [0.1.10] - 2018-08-03
### Fixed
- Merging `<script>` tags without leading `;` [#55].


## [0.1.9] - 2018-04-29
### Fixed
- Default minification options safety [#50].


## [0.1.8] - 2018-04-17
### Fixed
- ES6+ minification [#48].



## [0.1.7] - 2018-03-13
### Fixed
- Update dependencies which also fixes the SVG minification bug [#47].



## [0.1.6] - 2017-06-27
### Fixed
- "Not a function" error [#42].



## [0.1.5] - 2016-04-24
### Added
- Minify SVG [#28].
- Merge `<script>` [#19].

### Changed
- Remove redundant `type="submit"` from `<button>` [#31].

### Fixed
- Windows build [#30].


## [0.1.4] - 2016-02-16
### Added
- Minify JSON.
- Merge multiple `<style>` into one.
- Collapse boolean attributes.
- Remove redundant attributes.
- HTML minifiers benchmark [#22].

### Changed
- Expand list of JSON-like mime types [#20].


## [0.1.3] - 2016-02-09
### Fixed
- Don't alter HTML comments inside not relevant modules [#17].


## [0.1.2] - 2016-02-07
### Fixed
- Don't remove conditional comments in safe mode [#13].
- Downgrade: `String.startsWith -> String.search`.


## [0.1.1] - 2016-01-31
### Added
- Minify CSS inside `<style>` tags and `style` attributes.
- Minify JS inside `<script>` tags and `on*` attributes.

### Changed
- Remove attributes that contains only white spaces.



[0.1.10]: https://github.com/posthtml/htmlnano/compare/0.1.9...0.1.10
[0.1.9]: https://github.com/posthtml/htmlnano/compare/0.1.8...0.1.9
[0.1.8]: https://github.com/posthtml/htmlnano/compare/0.1.7...0.1.8
[0.1.7]: https://github.com/posthtml/htmlnano/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/posthtml/htmlnano/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/posthtml/htmlnano/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/posthtml/htmlnano/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/posthtml/htmlnano/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/posthtml/htmlnano/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/posthtml/htmlnano/compare/0.1.0...0.1.1


[#55]: https://github.com/posthtml/htmlnano/issues/55
[#50]: https://github.com/posthtml/htmlnano/issues/50
[#48]: https://github.com/posthtml/htmlnano/issues/48
[#47]: https://github.com/posthtml/htmlnano/issues/47
[#42]: https://github.com/posthtml/htmlnano/issues/42
[#31]: https://github.com/posthtml/htmlnano/issues/31
[#30]: https://github.com/posthtml/htmlnano/issues/30
[#28]: https://github.com/posthtml/htmlnano/issues/28
[#22]: https://github.com/posthtml/htmlnano/issues/22
[#20]: https://github.com/posthtml/htmlnano/issues/20
[#19]: https://github.com/posthtml/htmlnano/issues/19
[#17]: https://github.com/posthtml/htmlnano/issues/17
[#13]: https://github.com/posthtml/htmlnano/issues/13
