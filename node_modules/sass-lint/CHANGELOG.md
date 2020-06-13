# Sass Lint Changelog

## v1.13.1

**Fixes**
* Same as v1.12.1 - 1.13.0 was released by accident and contains many breaking changes - npm unpublishing failed so this unfortnately bumps our version a few spots - 


## v1.13.0

**IGNORE ME - SORRY**

## v1.12.1

**October 17th, 2017**

**Fixes**
* Temporarily move to our gonzales-pe-sl fork to publish fixes that currently don't exist on the gonzales-pe published version

## v1.12.0

**October 3rd, 2017**

**Fixes**
* Fixed an issue with custom properties being flagged in the misspelled-properties rule [#1122](https://github.com/sasstools/sass-lint/pull/1122)
* Fixed an issue where custom properties with colors in their name would be flagged as invalid by no-color-keywords [#1124](https://github.com/sasstools/sass-lint/pull/1124)
* Fixed a crash in empty-line-between-blocks where acessing the content of a parent node of type string would throw an error [#1125](https://github.com/sasstools/sass-lint/pull/1125)
* Functions and custom properties were being incorrectly flagged as invalid within rgba functions for no-color-literals [#1127](https://github.com/sasstools/sass-lint/pull/1127)
* Fixed an incorrect warning in space-after-colon when using `@at-root` [#1129](https://github.com/sasstools/sass-lint/pull/1129)
* Fixed an issue where interpolation was incorrectly flagging within the class-name-format rule [#1131](https://github.com/sasstools/sass-lint/pull/1131)


**New Features**
* Rollup.js integration added to integration list
* Added an npmignore to remove unnecessary dev files from a sass-lint install / release [#1132](https://github.com/sasstools/sass-lint/pull/1132)
* Added basic support for a `.sasslintrc` json config file [#1135](https://github.com/sasstools/sass-lint/pull/1135)
* Added two new options to the variable-for-property rule - [allow-map-get](https://github.com/sasstools/sass-lint/blob/master/docs/rules/variable-for-property.md#allow-map-get-true) & [allowed-functions](https://github.com/sasstools/sass-lint/blob/master/docs/rules/variable-for-property.md#allowed-functions-) - [#1128](https://github.com/sasstools/sass-lint/pull/1128)

## v1.11.1

**August 28th, 2017**

**Fixes**
* Fixed an issue with the `misspelled-properties` rule incorrectly reporting nested properties [#1113](https://github.com/sasstools/sass-lint/pull/1113)

## v1.11.0

**August 27th, 2017**

**New Features**
* The `trailing-semicolon` rule now checks for double semicolons [#1107](https://github.com/sasstools/sass-lint/pull/1107)

**Changes**
* Updated `gonzales-pe` parser to use version 4.1.1
* The `no-empty-rulesets` rule now flags rulesets that contain only comments [#998](https://github.com/sasstools/sass-lint/pull/998)
* The `misspelled-properties` rule now uses the [known-css-properties](https://www.npmjs.com/package/known-css-properties) to validate properties.
* The `zero-unit` rule now considers the `%` unit [#1103](https://github.com/sasstools/sass-lint/pull/1103)

**Fixes**
* Fixed a fatal error with the `space-after-bang` rule [#1108](https://github.com/sasstools/sass-lint/pull/1108)
* Fixed an issue where line numbers were incorrect when using `front-matter` [#1060](https://github.com/sasstools/sass-lint/pull/1060)
* Fixed an issue with the `misspelled-properties` rule incorrectly reporting multiline properties [#1106](https://github.com/sasstools/sass-lint/pull/1106)

## v1.10.2

**November 9th, 2016**

**Changes**
* Reverted back to ESlint v2.x to prevent a breaking change in Node < v4

**Fixes**
* Fixed an exception for partial idents in `space-around-operator` [#940](https://github.com/sasstools/sass-lint/pull/940)
* Fixed an issue with negative numbers in `space-around-operator` [#945](https://github.com/sasstools/sass-lint/pull/945)

## v1.10.1

**November 7th, 2016**

**Fixes**

* Fixed an issue with the `--no-exit` `-q` flag not being respected and unhandled errors/exceptions being thrown by the CLI
* Fixed an issue with variable declarations showing as properties in the `no-duplicate-properties` rule [#937](https://github.com/sasstools/sass-lint/pull/936)
* Fixed an issue with variable declarations showing as properties in the `declarations-before-nesting` rule [#937](https://github.com/sasstools/sass-lint/pull/936)

## v1.10.0

**November 6th, 2016**

The 'you can ignore those bad habits again' update

** :tada: DISABLE LINTERS :tada: **
The ability to enable and disable linters on the fly has finally(!) been added [#677](https://github.com/sasstools/sass-lint/pull/677) [docs](https://github.com/sasstools/sass-lint/blob/master/docs/toggle-rules-in-src.md)

A massive thank you to everyone who commented/contributed/reported and tested this feature this was very much a community effort here. An extra special thank you to
* [@donabrams](https://github.com/donabrams)

For his initial hard work in getting this off the ground. There were lots of others who have fixed everything from test issues to AST issues to make this possible afterwards, so thanks to you too!

**New Features**
* `max-warnings` which is available with the sass-lint CLI is now available as an option in your config file too [#857](https://github.com/sasstools/sass-lint/pull/857)
* **New Rule** `no-url-domains` rule [#846](https://github.com/sasstools/sass-lint/pull/846) [docs](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-url-domains.md)
* **New Rule** `max-line-length` rule was added [#840](https://github.com/sasstools/sass-lint/pull/840) [docs](https://github.com/sasstools/sass-lint/blob/master/docs/rules/max-line-length.md)
* **New Rule** `max-file-line-count` rule was added [#842](https://github.com/sasstools/sass-lint/pull/842) [docs](https://github.com/sasstools/sass-lint/blob/master/docs/rules/max-file-line-count.md)
* **New Rule** `declarations-before-nesting` rule was added [#866](https://github.com/sasstools/sass-lint/pull/866) [docs](https://github.com/sasstools/sass-lint/blob/master/docs/rules/declarations-before-nesting.md)

**Fixes**
* Fixed an issue with an un handled error being thrown in certain circumstances for the `space-before-colon` rule [#894](https://github.com/sasstools/sass-lint/pull/894)
* Operators in variable names are now handled correctly for the `variable-name-format` rule [#903](https://github.com/sasstools/sass-lint/pull/903)
* Fixed an issue with string values in the `shorthand-values` rule [#848](https://github.com/sasstools/sass-lint/pull/848)
* Fixed an issue with valid strict BEM producing an error in the `*-name-format` rules [#892](https://github.com/sasstools/sass-lint/pull/892)
* Fixed an issue with non-string user conventions in the `border-zero` rule [#913](https://github.com/sasstools/sass-lint/pull/913)
* Fixed an issue where BOM markers in files were causing parse errors or random errors/warnings [#893](https://github.com/sasstools/sass-lint/pull/893)
* Fixed an issue with interpolates properties in the `no-duplicate-properties` rule [#915](https://github.com/sasstools/sass-lint/pull/915)
* Fixed a possible error with invalid user conventions in the `border-zero` rule [#926](https://github.com/sasstools/sass-lint/pull/926)

**Changes**
* Node 0.10 and 0.12 are no longer officially supported by sass-lint. We've not deliberately broken these builds but we will no longer be testing against them either [#896](https://github.com/sasstools/sass-lint/issues/896) & [#924](https://github.com/sasstools/sass-lint/pull/924)
* In future the `no-url-protocols` rule will not lint domains in URL's for now a new flag is added to mimic this behaviour. The new `no-url-domains` rule can be used instead [#813](https://github.com/sasstools/sass-lint/issues/813)
* Front matter such as those present in Jekyll templates will now be ignored in all files before passing to the AST / Linting [897](https://github.com/sasstools/sass-lint/pull/897)
* Running the tests no longer required sass-lint development to be `npm-link`ed or globally installed. [#911](https://github.com/sasstools/sass-lint/pull/911)
* The concentric property list in `property-sort-order` was updated to reflect the latest release [#922](https://github.com/sasstools/sass-lint/pull/922)

**Updates**
* AST fixes have arrived with version 3.4.7 of gonzales-pe [#906](https://github.com/sasstools/sass-lint/pull/906)
* Updated to the latest versions of many other packages

**Documentation**
* The documentation around configuring a rule was tidied up and made clearer [#910](https://github.com/sasstools/sass-lint/pull/910)

**Special thanks to**

* [bgriffith](https://github.com/bgriffith)
* [donabrams](https://github.com/donabrams)
* [danpurdy](https://github.com/DanPurdy)
* [danwaz](https://github.com/danwaz)
* [lucasjahn](https://github.com/lucasjahn)
* [mrjamesriley](https://github.com/mrjamesriley)
* [notrobin](https://github.com/nottrobin)
* [onishiweb](https://github.com/onishiweb)
* [richarddewit](https://github.com/richarddewit)

## v1.9.1

**August 25, 2016**

**Fixes**
* Fixed an issue with nth selectors in the `no-mergeable-selectors` rule [#834](https://github.com/sasstools/sass-lint/issues/834)
* Fixed an issue with atrule arguments containing functions in the `no-mergeable-selectors` rule [#826](https://github.com/sasstools/sass-lint/issues/826)
* Fixed an issue with hex colors being ignored in the `shorthand-values` rule [#836](https://github.com/sasstools/sass-lint/pull/836)

## v1.9.0

**August 18, 2016**

**Fixes**
* Fixed an issue with the indentation rule when it encountered at-rules with no block immediately preceding a map [#779](https://github.com/sasstools/sass-lint/issues/779) [#783](https://github.com/sasstools/sass-lint/issues/783)
* Fixed an issue in `single-lint-per-selector` where inline comments were seen as selectors [#789](https://github.com/sasstools/sass-lint/issues/789)
* Fixed an issue with interpolation in placeholders within the `bem-depth` rule [#782](https://github.com/sasstools/sass-lint/issues/782)
* Removed duplicated code from `no-mergeable-selectors` to helper methods

**Documentation**
* Fixed typos in no-vendor-prefixes rule documentation [#787](https://github.com/sasstools/sass-lint/issues/787)
* Added link to Visual Studio extension [#815](https://github.com/sasstools/sass-lint/pull/815)

**New Rules**
* Added the `no-color-hex` rule to disallow all hexadecimal colour definitions [#754](https://github.com/sasstools/sass-lint/issues/754)

**Updates**
* Gonzales-pe updated to version 3.4.4 which fixes a lot of longstanding issues see the [Changelog](https://github.com/tonyganch/gonzales-pe/blob/dev/CHANGELOG.md)

## v1.8.2

**June 23, 2016**

Unfortunately it seems a reversion snuck into gonzales-pe's latest version so we're pinning it back where it was until it's fixed. Sorry..

## v1.8.1

**June 23, 2016**

Parser patching

Gonzales-pe had a few important updates so we chose to do a patch release to make sure everyone gets to benefit from less parse errors as soon as possible!

**Fixes**
* Fixed an issue in `shorthand-values` where values within parenthesis would be ignored [#748](https://github.com/sasstools/sass-lint/issues/748)
* Corrected the documentation for `property-units` [#740](https://github.com/sasstools/sass-lint/issues/740)
* Fixed an issue where config files were not being recursively searched for [#756](https://github.com/sasstools/sass-lint/issues/756)

**Updates**
* Gonzales-pe updated to version 3.3.5 [see changelog](https://github.com/tonyganch/gonzales-pe/blob/v3.3.5/CHANGELOG.md#21062016-version-335) [#746](https://github.com/sasstools/sass-lint/pull/746)

## v1.8.0

**June 17, 2016**

We're gonna need a bigger boat

**Indentation**

A lot of work on the indentation rule is present in 1.8 including the following:

* Tabs are now supported and can be used as a valid option in your config [#592](https://github.com/sasstools/sass-lint/issues/592)
* LF and CRLF are now supported for both spaces and tabs.
* `.sass` support is now included (Could be a little buggy due to some discrepancies in the AST) [#611](https://github.com/sasstools/sass-lint/issues/611)
* Mixed spaces and tabs warnings are now correctly informing you if you've specified that you'll use spaces and it detects tabs. [#382](https://github.com/sasstools/sass-lint/issues/382)
* Indenting of multiline properties in media queries etc is now supported [#426](https://github.com/sasstools/sass-lint/issues/426)

**Fixes**
* Fixed an issue with interpolated properties in the `shorthand-values` rule [#669](https://github.com/sasstools/sass-lint/issues/669)
* Corrected the name of the `pseudo-element` rule [#682](https://github.com/sasstools/sass-lint/pull/682)
* Corrected the name of the `no-empty-rulesets` rule [#684](https://github.com/sasstools/sass-lint/issues/684)
* Corrected the name of the `no-trailing-zero` rule [#685](https://github.com/sasstools/sass-lint/issues/685)
* Fixed an issue where partially matching rules affected each others severity levels [#687](https://github.com/sasstools/sass-lint/issues/687)
* Fixed an issue with nested properties in the `no-misspelled-properties` [#352](https://github.com/sasstools/sass-lint/issues/352)
* Fixed an issue with interpolated properties in the `no-misspelled-properties` [#679](https://github.com/sasstools/sass-lint/issues/679)
* Fixed an issue with interpolated selectors in the `no-mergeable-selectors` [#703](https://github.com/sasstools/sass-lint/issues/703)
* Added the absolute path module to fix an issue with Node 0.10 [#706](https://github.com/sasstools/sass-lint/pull/706)
* Added a new method and updated gulp-sass-lint to fix an config files and ignored files not working correctly [#452](https://github.com/sasstools/sass-lint/issues/452)
* Fixed an issue with the `!important` flag raising a lint warning within the `variable-for-property` rule [#714](https://github.com/sasstools/sass-lint/issues/714)
* Fixed an issue where sass-lint would try to lint a directory with a .scss or .sass extension, now sass-lint will only attempt to lint files :tada: [#719](https://github.com/sasstools/sass-lint/pull/719) & [#555](https://github.com/sasstools/sass-lint/issues/555)
* Fixed an issue where Sass color functions would raise lint warnings in the `no-color-keywords` rule [#717](https://github.com/sasstools/sass-lint/issues/717)
* Fixed an unhandled error with the `pseudo-element` rule [#671](https://github.com/sasstools/sass-lint/pull/671)

**Changes**
* Added flexbox and outline properties to the recess order preset [#666](https://github.com/sasstools/sass-lint/issues/666)
* Added missing pseudo classes to our pseudo class master list [#675](https://github.com/sasstools/sass-lint/issues/675)
* Added pascal case format to all name format rules [#678](https://github.com/sasstools/sass-lint/issues/678)
* Included files in your config file can now be an array similar to the ignored files option [#668](https://github.com/sasstools/sass-lint/issues/668)
* Added PR and issue templates [#692](https://github.com/sasstools/sass-lint/pulls/692)
* Now testing on Node v6 [#699](https://github.com/sasstools/sass-lint/issues/699)
* Added the `ignore-non-standard` option to the `no-vendor-prefixes` rule. This allows you to blanket ignore the vendor prefixes on any non standard properties [#702](https://github.com/sasstools/sass-lint/issues/702)
* The `url-quotes` rule now highlights the beginning of the detect rather than the end [#712](https://github.com/sasstools/sass-lint/issues/712)
* All helper tests have been split and rearranged for ease of use when developing [#322](https://github.com/sasstools/sass-lint/pull/322)
* Moved away from our Gonzales-pe-sl fork back to gonzales-pe as we've made changes to the main AST now [#722](https://github.com/sasstools/sass-lint/pull/722)

**New Rules**
* Added `pseudo-element` rule to enforce the use of single colons in pseudo classes and double colons in pseudo elements. [#662](https://github.com/sasstools/sass-lint/issues/662)
* Added `no-universal-selectors` rule to warn against the use of universal selectors (*) [#694](https://github.com/sasstools/sass-lint/issues/694)
* Added `no-attribute-selectors` rule to warn against the use of attribute selectors [#694](https://github.com/sasstools/sass-lint/issues/694)
* Added `no-combinators` rule to warn against the use of combinators [#694](https://github.com/sasstools/sass-lint/issues/694)
* Added `attribute-quotes` rule to enforce the use of the use of quotes in attribute values [#707](https://github.com/sasstools/sass-lint/issues/707)
* Added `no-disallowed-properties` rule to warn against the use of certain properties. [#546](https://github.com/sasstools/sass-lint/issues/546)

## v1.7.0

**April 27, 2016**

You wait months for one release and then four come along in a week!

**Fixes**
* Fixed an issue with final newline not registering correctly for `.sass` syntax [#627](https://github.com/sasstools/sass-lint/issues/627) & [#630](https://github.com/sasstools/sass-lint/issues/630).
* Fixed an issue with `placeholder-name-format` generating warnings on variables used as placeholder names.
* Fixed the `empty-args` rule being wrongly labeled as `no-empty-args` in lint warnings/errors [#625](https://github.com/sasstools/sass-lint/issues/625)
* Fixed an issue with `no-color-literals` incorrectly flagging variable names and map identifiers that shared their names with color literals [#538](https://github.com/sasstools/sass-lint/issues/538)
* CLI examples corrected thanks to [alxndr](https://github.com/alxndr) - [#649](https://github.com/sasstools/sass-lint/issues/649)

**Changes**
* `no-color-literals` now includes two extra options `allow-map-identifiers` and `allow-variable-identifiers` which allow you to fine tune your use of color literals in map identifiers/variables on top of the existing functionality [see the docs](https://github.com/sasstools/sass-lint/blob/develop/docs/rules/no-color-literals.md)
* Updated to `gonzales-pe-sl` v3.2.8

## v1.6.2

**April 22, 2016**

**Fixes**
* Fix `brace-style` rule incorrectly flagging `@imports` as single-line statements [#634](https://github.com/sasstools/sass-lint/issues/634)
* Fix `brace-style` rule not allowing multiline parameters [#632](https://github.com/sasstools/sass-lint/issues/632)
* `no-misspelled-properties` now correctly ignores vendor prefixes [#606](https://github.com/sasstools/sass-lint/issues/606)
* Now correctly strips double-barreled vendor prefixes such as `-moz-osx-`

## v.1.6.1

The update that time forgot

* Issues publishing to npm

## v1.6.0

**April 21, 2016**

The long lost 1.6 update

**WARNING**
* We've moved to the latest version of gonzales-pe and then onto our own fork in which we've fixed our issues with CRLF etc. All of our tests are passing but there may be unforeseen regressions in gonzales that we will aim to fix. If you find a problem like this please report it to us and we'll investigate further. You can then decide to keep your sass-lint dependency to 1.5.1 if you so choose.

**Changes**
* Updated all rules to work with the new Gonzales-pe 3.2.x release [#495](https://github.com/sasstools/sass-lint/issues/495)
> No breaking changes in the sense that all the rules are the same and pass the same tests or more BUT many did involve a complete re write.

* Now using gonzales-pe-sl 3.2.7 fork
* Update the no-mergeable-selectors rule to ignore certain situations and work a little more reliably across codebases
* Added BEM conventions to all naming rules [#614](https://github.com/sasstools/sass-lint/pull/614)
* Added Appveyor CI for testing against CRLF line endings on Windows


**CLI**
* Add max warnings option to the CLI --max-warnings [#568](https://github.com/sasstools/sass-lint/pull/568)

**New Rules**
* `no-trailing-whitespace` rule added [#605](https://github.com/sasstools/sass-lint/pull/605)

**Fixes**
* Fixed parsing error when using interpolated values [#44](https://github.com/sasstools/sass-lint/issues/44), [#184](https://github.com/sasstools/sass-lint/issues/184), [#210](https://github.com/sasstools/sass-lint/issues/210), [#222](https://github.com/sasstools/sass-lint/issues/222),
[#321](https://github.com/sasstools/sass-lint/issues/321),
[#486](https://github.com/sasstools/sass-lint/issues/486),
* Fixed parsing error when using the `!global` flag [#56](https://github.com/sasstools/sass-lint/issues/56)
* Having `-` within a class name will no longer return a parse error [#229](https://github.com/sasstools/sass-lint/issues/229)
* Fixed parsing error when using extrapolated variable as extend name [#313](https://github.com/sasstools/sass-lint/issues/313)
* Fixed an un-handled error thrown from the indentation rule [#389](https://github.com/sasstools/sass-lint/issues/389)
* Fixed an issue with final newline rule for sass [#445](https://github.com/sasstools/sass-lint/issues/445)
* Updated indentation rule to work with CRLF (indentation is mainly scss for the moment) [#524](https://github.com/sasstools/sass-lint/pull/524)
* Fixed parsing error when using nested maps [#531](https://github.com/sasstools/sass-lint/issues/531)
* Fixed parsing error when using variables for placeholder name [#532](https://github.com/sasstools/sass-lint/issues/532)
* Fixed issue with dots in filenames [#541](https://github.com/sasstools/sass-lint/pull/541)
* Fixed use of modulo operator in SCSS syntax [#565](https://github.com/sasstools/sass-lint/issues/565)
* Fixed an issue with space-around-operator and unicode [#620](https://github.com/sasstools/sass-lint/pull/620)
* Fixed an issue with CRLF line endings in the no-trailing-whitespace rule [#623](https://github.com/sasstools/sass-lint/pull/623)

**A big thank you to everyone who reported issues or contributed to the discussion around issues and also for everyone bearing with us while we go this monster update ready for you.**

## v1.5.1
**February 26, 2016**

Hotfix

**Fixes**
* Fix lodash dependancy issue [#549](https://github.com/sasstools/sass-lint/issues/549)

## v1.5.0
**January 28, 2016**

New year blues

**Changes**
* AST parse errors will now be returned to the user as `Fatal` lint errors this prevents un-handled errors breaking builds [#459](https://github.com/sasstools/sass-lint/pull/459)
* Sass-lint plugin for Brackets added to the README [#470](https://github.com/sasstools/sass-lint/issues/470)
* Sass-lint plugin for IntelliJ IDEA, RubyMine, WebStorm, PhpStorm, PyCharm, added to the README [#484](https://github.com/sasstools/sass-lint/issues/484)


**CLI**
* Updated error codes, whenever errors are present even when cli is using the `--no-exit` flag a error code of 1 will be output [#221](https://github.com/sasstools/sass-lint/issues/221)

**Fixes**
* Fixed an issue where an error of `next is undefined` would be thrown in the `space-after-colon` rule [#468](https://github.com/sasstools/sass-lint/issues/468)
* Fixed an issue with negative z-index values in the `space-around-operator` rule [#454](https://github.com/sasstools/sass-lint/issues/454)
* Fixed another minor issue with `space-around-operator` to prevent a possible crash [#483](https://github.com/sasstools/sass-lint/issues/483)

## v1.4.0
**December 10, 2015**

The long overdue update!

**Changes**
* The config file can now be cached for a small performance boost [#279](https://github.com/sasstools/sass-lint/issues/279)
* Added an `ignore-custom-properties` option to the property sort order rule, allowing you to ignore/include non standard properties in your property sort orders [#302](https://github.com/sasstools/sass-lint/issues/302)
* Streamlined the `force-pseudo-nesting`, `force-element-nesting` and `force-attribute-nesting` rules [#323](https://github.com/sasstools/sass-lint/pull/323)
* Improved the testing of our config handling [#403](https://github.com/sasstools/sass-lint/issues/403)
* Corrected the naming of the `no-misspelled-properties` tests [#405](https://github.com/sasstools/sass-lint/pull/405)
* Updated some of our dependencies to their latest versions [#428](https://github.com/sasstools/sass-lint/pull/428)
* `no-trailing-zero` now acts similar to the `no-unnecessary-mantissa` rule of scss-lint in that it warns about unnecessary decimals [#438](https://github.com/sasstools/sass-lint/issues/438)

**CLI**
* [-s --syntax] Syntax flag allows you to specify syntax of the file(s) you wish to lint [#381](https://github.com/sasstools/sass-lint/issues/381)

**New Rules**
* [space-around-operator](https://github.com/sasstools/sass-lint/blob/master/docs/rules/space-around-operator.md)
* [class-name-format](https://github.com/sasstools/sass-lint/blob/master/docs/rules/class-name-format.md)
* [id-name-format](https://github.com/sasstools/sass-lint/blob/master/docs/rules/id-name-format.md)
* [property-units](https://github.com/sasstools/sass-lint/blob/master/docs/rules/property-units.md)
* [bem-depth](https://github.com/sasstools/sass-lint/blob/master/docs/rules/bem-depth.md)

**Fixes**
* Pre emptive fix for `space-around-operator` with negative values [#394](https://github.com/sasstools/sass-lint/issues/394)
* Pre emptive fix for `space-around-operator` with percentage values [#425](https://github.com/sasstools/sass-lint/issues/425)
* `no-trailing-zero` now works as expected with 0 values after a decimal [#439](https://github.com/sasstools/sass-lint/issues/439)
* Percentage values are now correctly handled and reported in the `shorthand-values` rule [#435](https://github.com/sasstools/sass-lint/issues/435)
* `function-name-format` no longer incorrectly reports on valid default CSS & Sass functions [#442](https://github.com/sasstools/sass-lint/pull/442)
* Corrected a typo in config file documentation [#384](https://github.com/sasstools/sass-lint/pull/384)

**Brought to you by**

* [Sam Richard](https://github.com/Snugug)
* [Ben Griffith](https://github.com/bgriffith)
* [Dan Purdy](https://github.com/DanPurdy)
* [Ben Rothman](https://github.com/benthemonkey)
* [Don Abrams](https://github.com/donabrams)
* [Andrew Hays](https://github.com/Dru89)
* [Kaelig](https://github.com/kaelig)

**A big thankyou to everyone who reported issues or contributed to the discussion around issues**

## v1.3.3
**November 16, 2015**

**Changes**
* Added coveralls code coverage tool, updated relevant tests [#351](https://github.com/sasstools/sass-lint/pull/351)

**Fixes**
* Added missing `background-clip` property to the SMACCS sort order [#366](https://github.com/sasstools/sass-lint/issues/366)
* Fixed an issue with negative values in the `shorthand-values` rule [#375](https://github.com/sasstools/sass-lint/issues/375)
* Fixed an issue where `mixin-name-format` was attempting to lint extends [#396](https://github.com/sasstools/sass-lint/issues/396)

## v1.3.2
**October 28, 2015**

**Changes**
* Add tests for ignored files when using the CLI [#72](https://github.com/sasstools/sass-lint/issues/72)

**Fixes**
* Ignored files passed in using the `-i` flag are now correctly ignored [#129](https://github.com/sasstools/sass-lint/issues/129)
* Fixed an issue where the `no-url-protocols` rule would ignore the users' config [#335](https://github.com/sasstools/sass-lint/issues/335)
* The `hex-length` rule now correctly handles short hexes [#341](https://github.com/sasstools/sass-lint/issues/341)
* The `no-url-protocols` rule no longer incorrectly issues warnings for data-urls [#340](https://github.com/sasstools/sass-lint/issues/340)
* The `trailing-semicolon` rule no longer incorrectly issues warnings for nested properties [#359](https://github.com/sasstools/sass-lint/pull/359)
* The `space-before-brace` rule no longer incorrectly issues warnings for nested properties [#361](https://github.com/sasstools/sass-lint/pull/361)


## v1.3.1
**October 17, 2015**

**Changes**
* Added the missing rules `function-name-format`, `mixin-name-format`, `placeholder-name-format` and `variable-name-format` to the default config [#315](https://github.com/sasstools/sass-lint/issues/315)

**Fixes**

* Corrected an issue with the rule `brace-style` that would crash sass-lint [#301](https://github.com/sasstools/sass-lint/issues/301)
* Fixed an issue where user configs and options were being ignored or overwritten by default rules [#309](https://github.com/sasstools/sass-lint/issues/309)

## v1.3.0
**October 12, 2015**

Lint all the things!

1.3.0 introduces a whole raft of changes, fixes and new rules. Enjoy!

**Changes**

* Now testing against Node 4 [#145](https://github.com/sasstools/sass-lint/pull/145#issuecomment-138744764)
* `no-duplicate-properties` now accepts an exclusion whitelist [#156](https://github.com/sasstools/sass-lint/pull/156)
* IDE integrations added to README (Atom & Sublime Text) [#163](https://github.com/sasstools/sass-lint/pull/163)
* Output is now silenced on no errors [#141](https://github.com/sasstools/sass-lint/issues/141)
* Option `config-file` will tell Sass Lint the path to a custom config file. [#226](https://github.com/sasstools/sass-lint/issues/226)
* All rules except indentation now working correctly with `.sass` syntax [#258](https://github.com/sasstools/sass-lint/pull/258)
* `space-between-parens` rule now allows multiline arguments [#260](https://github.com/sasstools/sass-lint/issues/260)
* `empty-line-between-blocks` rule now optionally allows single line rulesets [#282](https://github.com/sasstools/sass-lint/issues/282)
* The `no-duplicate-properties` rule exclusion whitelist only works for properties directly after one another. [#280](https://github.com/sasstools/sass-lint/issues/280)


**CLI**

* [-f --format]() Format flag allows you to specify output format [#127](https://github.com/sasstools/sass-lint/issues/127)
* [-o --output]() Output flag allows you to specify a file to output to [#127](https://github.com/sasstools/sass-lint/issues/127)

**Rules**

* [brace-style](https://github.com/sasstools/sass-lint/issues/36)
* [force-attribute-nesting](https://github.com/sasstools/sass-lint/blob/master/docs/rules/force-attribute-nesting.md)
* [force-element-nesting](https://github.com/sasstools/sass-lint/blob/master/docs/rules/force-element-nesting.md)
* [force-pseudo-nesting](https://github.com/sasstools/sass-lint/blob/master/docs/rules/force-pseudo-nesting.md)
* [function-name-format](https://github.com/sasstools/sass-lint/blob/master/docs/rules/function-name-format.md)
* [mixin-name-format](https://github.com/sasstools/sass-lint/blob/master/docs/rules/mixin-name-format.md)
* [no-mergeable-selectors](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-mergeable-selectors.md)
* [no-misspelled-properties](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-misspelled-properties.md)
* [no-qualifying-elements](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-qualifying-elements.md)
* [no-trailing-zero](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-trailing-zero.md)
* [no-transition-all](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-transition-all.md)
* [no-url-protocols](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-url-protocols.md)
* [no-vendor-prefixes](https://github.com/sasstools/sass-lint/blob/master/docs/rules/no-vendor-prefixes.md)
* [placeholder-name-format](https://github.com/sasstools/sass-lint/blob/master/docs/rules/placeholder-name-format.md)
* [shorthand-values](https://github.com/sasstools/sass-lint/blob/master/docs/rules/shorthand-values.md)
* [url-quotes](https://github.com/sasstools/sass-lint/blob/master/docs/rules/url-quotes.md)
* [variable-name-format](https://github.com/sasstools/sass-lint/blob/master/docs/rules/variable-name-format.md)

**Fixes**

* Capitalised all warning messages [#137](https://github.com/sasstools/sass-lint/issues/137)
* Line endings should now be consistently working cross platform [#154](https://github.com/sasstools/sass-lint/pull/154)
* Fixed issue with non resetting test prefixes [#182](https://github.com/sasstools/sass-lint/issues/182)
* Fixed resetting of test defaults [#186](https://github.com/sasstools/sass-lint/issues/186)
* Documentation fixes [#235](https://github.com/sasstools/sass-lint/pull/235)
* Absolute config paths being converted to relative all the time [#223](https://github.com/sasstools/sass-lint/issues/223)
* Multiple fixes for `.sass` syntax [#258](https://github.com/sasstools/sass-lint/pull/258)
* Fixed an issue with the warning message for `no-qualifying-elements` [#262](https://github.com/sasstools/sass-lint/pull/262)
* Fixed a bug in `no-shorthand-values` rule [#263](https://github.com/sasstools/sass-lint/issues/263)
* `indentation` rule now works with maps and multiline arguments also fixes a few edge cases [#104](https://github.com/sasstools/sass-lint/issues/104) [260](https://github.com/sasstools/sass-lint/issues/260)


**Brought to you by..**

* [Sam Richard](https://github.com/Snugug)
* [Ben Griffith](https://github.com/bgriffith)
* [Dan Purdy](https://github.com/DanPurdy)
* [Ben Rothman](https://github.com/benthemonkey)
* [Michael Vendivel](https://github.com/mven)
* [Joshua Clanton](https://github.com/joshuacc)
* [Kenneth Skovhus](https://github.com/skovhus)
* [Nick](https://github.com/MethodGrab)
* [Anders Olsen Sandvik](https://github.com/Andersos)
* [Nicolas Fortin](https://github.com/zallek)
* [Alan Souza](https://github.com/alansouzati)

**A big thankyou to everyone who reported issues or contributed to the discussion around issues**

## v1.2.3
**October 5, 2015**

**Changes**

* Lock AST to known good version ([#245](https://github.com/sasstools/sass-lint/issues/245))

**Fixes**

* Top level mixins now don't raise an incorrect `mixins before declarations` warning
([#227](https://github.com/sasstools/sass-lint/issues/227))
* Fix an issue with `final-newline` for the `.sass` syntax ([#207](https://github.com/sasstools/sass-lint/issues/207))
* The `placeholder-in-extend` rule now works for the `.sass` syntax ([#199](https://github.com/sasstools/sass-lint/issues/199))
* The `clean-import-paths` rule now works for the `.sass` syntax ([#179](https://github.com/sasstools/sass-lint/issues/179))
* The `extends-before-mixins` rule now works for the `.sass` syntax ([#193](https://github.com/sasstools/sass-lint/issues/193))


## v1.2.2
**September 22, 2015**

**Fixes**

* CLI output formatting now works ([#213](https://github.com/sasstools/sass-lint/pull/213))


## v1.2.1
**September 19, 2015**

**Fixes**

* Extends rules now work with `.sass` syntax ([#189](https://github.com/sasstools/sass-lint/pull/189))
* Silence output if there are no errors ([#170](https://github.com/sasstools/sass-lint/pull/170))
* Single line per selector now works with `.sass` syntax ([#168](https://github.com/sasstools/sass-lint/pull/168))
* Custom options no longer overwrite defaults ([#159](https://github.com/sasstools/sass-lint/pull/159))
* Fix CLI config error ([#150](https://github.com/sasstools/sass-lint/pull/153))


## v1.2.0
**September 7, 2015**

Rockin' Rules and Fixes!

Huge thanks to [Ben Griffith](https://github.com/bgriffith) and [Dan Purdy](https://github.com/DanPurdy) for their awesome work on getting 1.2.0 out the door and welcome them as collaborators!

**Fixes**

* Color Keyword with variable names no longer fails ([#126](https://github.com/sasstools/sass-lint/issues/126))
* Space After Comma rule no longer incorrectly reports end of lines as spaces ([#125](https://github.com/sasstools/sass-lint/issues/125))
* No longer errors on empty files ([#91](https://github.com/sasstools/sass-lint/issues/91))
* Update naming of `clean-import-paths` and `no-duplicate-properties` ([#118](https://github.com/sasstools/sass-lint/issues/118))
* Fix colons in parens being not parsed for `space-before-colon` ([#98](https://github.com/sasstools/sass-lint/issues/98))
* Fix issue with `space-after-comma` and new lines ([#105](https://github.com/sasstools/sass-lint/issues/105))
* Fix for `space-after-colon` only finding some colons ([#98](https://github.com/sasstools/sass-lint/issues/98))
* Fix `clean-import-path` bug when importing CSS ([#95](https://github.com/sasstools/sass-lint/issues/95))
* Fix EOL issues on Windows ([#65](https://github.com/sasstools/sass-lint/issues/65))
* Fix issue with `mixins-before-declarations` for strange Gonzales parsing ([#80](https://github.com/sasstools/sass-lint/issues/80))
* Fix typo in `quotes` doc

**Changes**

* Clean up tests ([#123](https://github.com/sasstools/sass-lint/issues/123), [#110](https://github.com/sasstools/sass-lint/issues/111))
* Clean up ESLint testing
* Add tests for helper functions ([#116](https://github.com/sasstools/sass-lint/issues/116))

**New**

* Enhance `property-sort-order` with RECESS, SMACSS, and Concentric default sort orders ([#20](https://github.com/sasstools/sass-lint/issues/20))
* Add Sample Sass Lint config file ([#57](https://github.com/sasstools/sass-lint/issues/57))
* Add tests for CLI ([#72](https://github.com/sasstools/sass-lint/issues/72), [#108](https://github.com/sasstools/sass-lint/issues/108))
* Add ability to write output to file and change output formatting ([#48](https://github.com/sasstools/sass-lint/issues/48))
* Add ability to specify that configured rules override instead of merge with defaults ([#58](https://github.com/sasstools/sass-lint/issues/58))

**Rules**

* [no-color-keywords](https://github.com/sasstools/sass-lint/issues/101)
* [variable-for-property](https://github.com/sasstools/sass-lint/issues/33)
* [no-color-literals](https://github.com/sasstools/sass-lint/issues/27)
* [no-duplicate-properties](https://github.com/sasstools/sass-lint/issues/28)
* [border-zero](https://github.com/sasstools/sass-lint/issues/84)
* [no-css-comments](https://github.com/sasstools/sass-lint/issues/85)
* [no-invalid-hex](https://github.com/sasstools/sass-lint/issues/82)
* [empty-args](https://github.com/sasstools/sass-lint/issues/38)
* [hex-notation](https://github.com/sasstools/sass-lint/issues/77)
* [hex-length](https://github.com/sasstools/sass-lint/issues/73)
* [zero-unit](https://github.com/sasstools/sass-lint/issues/68)
* [clean-import-paths](https://github.com/sasstools/sass-lint/issues/29)


## v1.1.0
**August 31, 2015**

CLI Goodness

**New**

* Add Command Line Interface usage for Sass Lint! ([#42](https://github.com/sasstools/sass-lint/issues/42))
* Add ability to define custom config path ([#47](https://github.com/sasstools/sass-lint/issues/47))
* Add ability for config to be found recursively up the directory tree to a user's home directory

**Fixes**

* Empty line between root-level blocks ([#54](https://github.com/sasstools/sass-lint/issues/54))
* Bang whitespace include `!default` flag ([#53](https://github.com/sasstools/sass-lint/issues/53))
* One declaration per line inside arguments ([#51](https://github.com/sasstools/sass-lint/issues/51))
* Leading zero non-decimal issues ([#49](https://github.com/sasstools/sass-lint/issues/49))
* Indentation rule with parenthesis ([#46](https://github.com/sasstools/sass-lint/issues/46))


## v1.0.0
**August 29, 2015**

Initial Release!

**Rules**

* [extends-before-mixins](docs/rules/extends-before-mixins.md)
* [extends-before-declarations](docs/rules/extends-before-declarations.md)
* [placeholder-in-extend](docs/rules/placeholder-in-extend.md)
* [mixins-before-declarations](docs/rules/mixins-before-declarations.md)
* [one-declaration-per-line](docs/rules/one-declaration-per-line.md)
* [empty-line-between-blocks](docs/rules/empty-line-between-blocks.md)
* [single-line-per-selector](docs/rules/single-line-per-selector.md)
* [no-empty-rulesets](docs/rules/no-empty-rulesets.md)
* [no-extends](docs/rules/no-extends.md)
* [no-ids](docs/rules/no-ids.md)
* [no-important](docs/rules/no-important.md)
* [indentation](docs/rules/indentation.md)
* [leading-zero](docs/rules/leading-zero.md)
* [nesting-depth](docs/rules/nesting-depth.md)
* [property-sort-order](docs/rules/property-sort-order.md)
* [space-after-comma](docs/rules/space-after-comma.md)
* [space-before-colon](docs/rules/space-before-colon.md)
* [space-after-colon](docs/rules/space-after-colon.md)
* [space-before-brace](docs/rules/space-before-brace.md)
* [space-before-bang](docs/rules/space-before-bang.md)
* [space-after-bang](docs/rules/space-after-bang.md)
* [space-between-parens](docs/rules/space-between-parens.md)
* [trailing-semicolon](docs/rules/trailing-semicolon.md)
* [final-newline](docs/rules/final-newline.md)
* [no-debug](docs/rules/no-debug.md)
* [no-warn](docs/rules/no-warn.md)
* [quotes](docs/rules/quotes.md)
