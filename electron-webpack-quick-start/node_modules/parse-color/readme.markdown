# parse-color

parse a [css color string](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value)
plus `hsv()` and `cmyk()` strings

[![testling badge](https://ci.testling.com/substack/parse-color.png)](https://ci.testling.com/substack/parse-color)

[![build status](https://secure.travis-ci.org/substack/parse-color.png)](http://travis-ci.org/substack/parse-color)

# example

``` js
var parse = require('parse-color');
console.log(parse(process.argv[2]));
```

output:

```
$ node example/parse.js '#ffa500'
{ rgb: [ 255, 165, 0 ],
  hsl: [ 39, 100, 50 ],
  hsv: [ 39, 100, 100 ],
  cmyk: [ 0, 35, 100, 0 ],
  keyword: 'orange',
  hex: '#ffa500',
  rgba: [ 255, 165, 0, 1 ],
  hsla: [ 39, 100, 50, 1 ],
  hsva: [ 39, 100, 100, 1 ],
  cmyka: [ 0, 35, 100, 0, 1 ] }
```

```
$ node example/parse.js lime
{ rgb: [ 0, 255, 0 ],
  hsl: [ 120, 100, 50 ],
  hsv: [ 120, 100, 100 ],
  cmyk: [ 100, 0, 100, 0 ],
  keyword: 'lime',
  hex: '#00ff00',
  rgba: [ 0, 255, 0, 1 ],
  hsla: [ 120, 100, 50, 1 ],
  hsva: [ 120, 100, 100, 1 ],
  cmyka: [ 100, 0, 100, 0, 1 ] }
```

```
$ node example/parse.js 'hsl(210,50,50)'
{ rgb: [ 64, 127, 191 ],
  hsl: [ 210, 50, 50 ],
  hsv: [ 210, 67, 75 ],
  cmyk: [ 67, 33, 0, 25 ],
  keyword: undefined,
  hex: '#407fbf',
  rgba: [ 64, 127, 191, 1 ],
  hsla: [ 210, 50, 50, 1 ],
  hsva: [ 210, 67, 75, 1 ],
  cmyka: [ 67, 33, 0, 25, 1 ] }
```

```
$ node example/parse.js 'rgba(153,50,204,60%)'
{ rgb: [ 153, 50, 204 ],
  hsl: [ 280, 61, 50 ],
  hsv: [ 280, 75, 80 ],
  cmyk: [ 25, 75, 0, 20 ],
  keyword: 'darkorchid',
  hex: '#9932cc',
  rgba: [ 153, 50, 204, 0.6 ],
  hsla: [ 280, 61, 50, 0.6 ],
  hsva: [ 280, 75, 80, 0.6 ],
  cmyka: [ 25, 75, 0, 20, 0.6 ] }
```

# methods

``` js
var parse = require('parse-color')
```

## var color = parse(colorString)

Return a `color` object from the
[css colorString](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value).

`color` has these attributes:

* rgb - an array of `[ red, green, blue ]`
* hsl - an array of `[ hue, saturation, luminosity ]`
* hsv - an array of `[ hue, saturation, value ]`
* cmyk - an array of `[ cyan, magenta, yellow, blac(k) ]`
* keyword - the name of the color, if known
* hex - the hex rgb string `#rrggbb`
* rgba - rgb plus an alpha value from 0 to 1, inclusive
* hsla - hsl plus an alpha value from 0 to 1, inclusive
* hsva - hsv plus an alpha value from 0 to 1, inclusive
* cmyka - cmyk plus an alpha value from 0 to 1, inclusive

When a color can't be parsed or is unknown, the attributes will be undefined:

```
$ node example/parse.js 'x'
{ rgb: undefined,
  hsl: undefined,
  hsv: undefined,
  cmyk: undefined,
  keyword: 'x',
  hex: undefined }
```

# install

With [npm](https://npmjs.org) do:

```
npm install parse-color
```

# license

MIT
