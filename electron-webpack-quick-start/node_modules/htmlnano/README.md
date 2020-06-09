# htmlnano
[![npm version](https://badge.fury.io/js/htmlnano.svg)](http://badge.fury.io/js/htmlnano)
[![Build Status](https://travis-ci.org/posthtml/htmlnano.svg?branch=master)](https://travis-ci.org/posthtml/htmlnano)

Modular HTML minifier, built on top of the [PostHTML](https://github.com/posthtml/posthtml). Inspired by [cssnano](http://cssnano.co/).

## [Benchmark](https://github.com/maltsev/html-minifiers-benchmark/blob/master/README.md)
[html-minifier]: https://www.npmjs.com/package/html-minifier
[htmlnano]: https://www.npmjs.com/package/htmlnano

| Website | Source (KB) | [html-minifier] | [htmlnano] |
|---------|------------:|----------------:|-----------:|
| [stackoverflow.com](http://stackoverflow.com/) | 250 | 199 | 208 |
| [github.com](http://github.com/) | 51 | 43 | 45 |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Main_Page) | 71 | 64 | 68 |
| [npmjs.com](https://www.npmjs.com/features) | 26 | 20 | 21 |
| **Avg. minify rate** | 0% | **18%** | **14%** |

## Usage

### Gulp

```bash
npm install --save-dev gulp-htmlnano
```

```js
var gulp = require('gulp');
var htmlnano = require('gulp-htmlnano');
var options = {
    removeComments: false
};

gulp.task('default', function() {
    return gulp
        .src('./index.html')
        .pipe(htmlnano(options))
        .pipe(gulp.dest('./build'));
});
```

### Javascript

```js
var htmlnano = require('htmlnano');
var options = {
    removeEmptyAttributes: false, // Disable the module "removeEmptyAttributes"
    collapseWhitespace: 'conservative' // Pass options to the module "collapseWhitespace"
};

htmlnano
    .process(html, options)
    .then(function (result) {
        // result.html is minified
    })
    .catch(function (err) {
        console.error(err);
    });
```

### PostHTML

Just add `htmlnano` as the last plugin:

```js
var posthtml = require('posthtml');
var options = {
    removeComments: false, // Disable the module "removeComments"
    collapseWhitespace: 'conservative' // Pass options to the module "collapseWhitespace"
};
var posthtmlPlugins = [
    /* other PostHTML plugins */

    require('htmlnano')(options)
];

posthtml(posthtmlPlugins)
    .process(html)
    .then(function (result) {
        // result.html is minified
    })
    .catch(function (err) {
        console.error(err);
    });

// You can also use htmlnano modules separately:
posthtml([
    require('htmlnano/lib/modules/mergeStyles').default
]).process(html);
```

## Modules

By default the modules should only perform safe transforms, see the module documentation below for details.
You can disable modules by passing `false` as option, and enable them by passing `true`.

### collapseWhitespace

Collapses redundant white spaces (including new lines). It doesn’t affect white spaces in the elements `<style>`, `<textarea>`, `<script>` and `<pre>`.

##### Options

- `conservative` — collapses all redundant white spaces to 1 space (default)
- `all` — collapses all redundant white spaces

##### Side effects

`<i>hello</i> <i>world</i>` after minification will be rendered as `helloworld`.
To prevent that use `conservative` option (this is the default option).

##### Example

Source:

```html
<div>
    hello  world!
    <style>div  { color: red; }  </style>
</div>
```

Minified (with `all`):

```html
<div>hello world!<style>div  { color: red; }  </style></div>
```

Minified (with `conservative`):

```html
<div> hello world! <style>div  { color: red; }  </style> </div>
```

### removeComments

##### Options

- `safe` – removes all HTML comments except the conditional comments and  [`<!--noindex--><!--/noindex-->`](https://yandex.com/support/webmaster/controlling-robot/html.xml) (default)
- `all` — removes all HTML comments

##### Example

Source:

```html
<div><!-- test --></div>
```

Minified:

```html
<div></div>
```

### removeEmptyAttributes

Removes empty [safe-to-remove](https://github.com/posthtml/htmlnano/blob/master/lib/modules/removeEmptyAttributes.es6) attributes.

##### Side effects

This module could break your styles or JS if you use selectors with attributes:

```CSS
img[style=""] {
    margin: 10px;
}
```

##### Example

Source:

```html
<img src="foo.jpg" alt="" style="">
```

Minified:

```html
<img src="foo.jpg" alt="">
```

### minifyCss

Minifies CSS with [cssnano](http://cssnano.co/) inside `<style>` tags and `style` attributes.

##### Options

Css transforms are set to the `safe` option as a default (this should have very little side-effects):

```Json
"minifyCss": {
    "safe": true
}
```

See [the documentation of cssnano](http://cssnano.co/optimisations/).
For example you can [keep outdated vendor prefixes](http://cssnano.co/optimisations/#discard-outdated-vendor-prefixes):

```js
htmlnano.process(html, {
    minifyCss: {
        autoprefixer: false
    }
});
```

##### Example

Source:

```html
<div>
    <style>
        h1 {
            margin: 10px 10px 10px 10px;
            color: #ff0000;
        }
    </style>
</div>
```

Minified:

```html
<div>
    <style>h1{margin:10px;color:red}</style>
</div>
```

### minifyJs

Minifies JS with [Terser](https://github.com/fabiosantoscode/terser) inside `<script>` tags.

##### Options

See [the API documentation of Terser](https://github.com/fabiosantoscode/terser#api-reference)

##### Example

Source:

```html
<div>
    <script>
        /* comment */
        var foo = function () {

        };
    </script>
</div>
```

Minified:

```html
<div>
    <script>var foo=function(){};</script>
</div>
```

### minifyJson

Minifies JSON inside `<script type="application/json"></script>`.

##### Example

Source:

```html
<script type="application/json">
{
    "user": "me"
}
</script>
```

Minified:

```html
<script type="application/json">{"user":"me"}</script>
```

### minifySvg

Minifies SVG inside `<svg>` tags with [SVGO](https://github.com/svg/svgo/).

##### Options

See [the documentation of SVGO](https://github.com/svg/svgo/blob/master/README.md)

##### Example

Source:

```html
<svg version="1.1" baseProfile="full" width="300" height="200" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="red" />

    <circle cx="150" cy="100" r="80" fill="green" />

    <text x="150" y="125" font-size="60" text-anchor="middle" fill="white">SVG</text>
</svg>`
```

Minified:

```html
<svg baseProfile="full" width="300" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="red"/><circle cx="150" cy="100" r="80" fill="green"/><text x="150" y="125" font-size="60" text-anchor="middle" fill="#fff">SVG</text></svg>
```

### removeRedundantAttributes

Removes redundant attributes from tags if they contain default values:

- `method="get"` from `<form>`
- `type="text"` from `<input>`
- `type="submit"` from `<button>`
- `language="javascript"` and `type="text/javascript"` from `<script>`
- `charset` from `<script>` if it's an external script
- `media="all"` from `<style>` and `<link>`

##### Options

This module is disabled by default, change option to true to enable this module.

##### Side effects

This module could break your styles or JS if you use selectors with attributes:

```CSS
form[method="get"] {
    color: red;
}
```

##### Example

Source:

```html
<form method="get">
    <input type="text">
</form>
```

Minified:

```html
<form>
    <input>
</form>
```

### collapseBooleanAttributes

Collapses boolean attributes (like `disabled`) to the minimized form.

##### Side effects

This module could break your styles or JS if you use selectors with attributes:

```CSS
button[disabled="disabled"] {
    color: red;
}
```

##### Example

Source:

```html
<button disabled="disabled">click</button>
<script defer=""></script>
```

Minified:

```html
<button disabled>click</button>
<script defer></script>
```

### mergeStyles

Merges multiple `<style>` with the same `media` and `type` into one tag.
`<style scoped>...</style>` are skipped.

##### Example

Source:

```html
<style>h1 { color: red }</style>
<style media="print">div { color: blue }</style>

<style type="text/css" media="print">a {}</style>
<style>div { font-size: 20px }</style>
```

Minified:

```html
<style>h1 { color: red } div { font-size: 20px }</style>
<style media="print">div { color: blue } a {}</style>
```

### mergeScripts

Merge multiple `<script>` with the same attributes (`id, class, type, async, defer`) into one (last) tag.

##### Side effects

It could break your code if the tags with different attributes share the same variable scope.
See the example below.

##### Example

Source:

```html
<script>var foo = 'A:1';</script>
<script class="test">foo = 'B:1';</script>
<script type="text/javascript">foo = 'A:2';</script>
<script defer>foo = 'C:1';</script>
<script>foo = 'A:3';</script>
<script defer="defer">foo = 'C:2';</script>
<script class="test" type="text/javascript">foo = 'B:2';</script>
```

Minified:

```html
<script>var foo = 'A:1'; foo = 'A:2'; foo = 'A:3';</script>
<script defer="defer">foo = 'C:1'; foo = 'C:2';</script>
<script class="test" type="text/javascript">foo = 'B:1'; foo = 'B:2';</script>
```

### custom

It's also possible to pass custom modules in the minifier.

As a function:

```js
var options = {
    custom: function (tree, options) {
        // Some minification
        return tree;
    }
};
```

Or as a list of functions:

```js
var options = {
    custom: [
        function (tree, options) {
            // Some minification
            return tree;
        },

        function (tree, options) {
            // Some other minification
            return tree;
        }
    ]
};
```

`options` is an object with all options that were passed to the plugin.

## Contribute

Since the minifier is modular, it's very easy to add new modules:

1. Create a ES6-file inside `lib/modules/` with a function that does some minification. For example you can check [`lib/modules/example.es6`](https://github.com/posthtml/htmlnano/blob/master/lib/modules/example.es6).

2. Add the module in [the modules array](https://github.com/posthtml/htmlnano/blob/master/lib/htmlnano.es6#L5). The modules are applied from top to bottom. So you can choose the order for your module.

3. Create a JS-file inside `test/modules/` with some unit-tests.

4. Describe your module in the section "[Modules](https://github.com/posthtml/htmlnano/blob/master/README.md#modules)".

5. Send me a pull request.

Other types of contribution (bug fixes, documentation improves, etc) are also welcome!
Would like to contribute, but don't have any ideas what to do? Check out [our issues](https://github.com/posthtml/htmlnano/labels/help%20wanted).
