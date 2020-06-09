# Changelog


## v4.1.2

 - The hotfix was hotfixed

## v4.1.1

 - Fixed a bug where toplevel scopes were being mixed up with lambda scopes

## v4.1.0

 - Internal functions were replaced by `Object.assign`, `Array.prototype.some`, `Array.prototype.find` and `Array.prototype.every`.
 - A serious issue where some ESM-native code was broken was fixed.
 - Performance improvements were made.
 - Support for BigInt was added.
 - Inline efficiency was improved. Functions are now being inlined more proactively instead of being inlined only after another Compressor pass.

## v4.0.2

(Hotfix release. Reverts unmapped segments PR [#342](https://github.com/terser-js/terser/pull/342), which will be put back on Terser when the upstream issue is resolved)

## v4.0.1

 - Collisions between the arguments of inlined functions and names in the outer scope are now being avoided while inlining
 - Unmapped segments are now preserved when compressing a file which has source maps
 - Default values of functions are now correctly converted from Mozilla AST to Terser AST
 - JSON ⊂ ECMAScript spec (if you don't know what this is you don't need to)
 - Export AST_* classes to library users
 - Fixed issue with `collapse_vars` when functions are created with the same name as a variable which already exists
 - Added `MutationObserverInit` (Object with options for initialising a mutation observer) properties to the DOM property list
 - Custom `Error` subclasses are now internally used instead of old-school Error inheritance hacks.
 - Documentation fixes
 - Performance optimizations

## v4.0.0

 - **breaking change**: The `variables` property of all scopes has become a standard JavaScript `Map` as opposed to the old bespoke `Dictionary` object.
 - Typescript definitions were fixed
 - `terser --help` was fixed
 - The public interface was cleaned up
 - Fixed optimisation of `Array` and `new Array`
 - Added the `keep_quoted=strict` mode to mangle_props, which behaves more like Google Closure Compiler by mangling all unquoted property names, instead of reserving quoted property names automatically.
 - Fixed parent functions' parameters being shadowed in some cases
 - Allowed Terser to run in a situation where there are custom functions attached to Object.prototype
 - And more bug fixes, optimisations and internal changes

## v3.17.0

 - More DOM properties added to --mangle-properties's DOM property list
 - Closed issue where if 2 functions had the same argument name, Terser would not inline them together properly
 - Fixed issue with `hasOwnProperty.call`
 - You can now list files to minify in a Terser config file
 - Started replacing `new Array(<number>)` with an array literal
 - Started using ES6 capabilities like `Set` and the `includes` method for strings and arrays

## v3.16.1

 - Fixed issue where Terser being imported with `import` would cause it not to work due to the `__esModule` property. (PR #254 was submitted, which was nice, but since it wasn't a pure commonJS approach I decided to go with my own solution)

## v3.16.0

 - No longer leaves names like Array or Object or window as a SimpleStatement (statement which is just a single expression).
 - Add support for sections sourcemaps (IndexedSourceMapConsumer)
 - Drops node.js v4 and starts using commonJS
 - Is now built with rollup

## v3.15.0

 - Inlined spread syntax (`[...[1, 2, 3], 4, 5] => [1, 2, 3, 4, 5]`) in arrays and objects.
 - Fixed typo in compressor warning
 - Fixed inline source map input bug
 - Fixed parsing of template literals with unnecessary escapes (Like `\\a`)
