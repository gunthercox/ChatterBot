### CSS Hot Loader

[![build status][travis-image]][travis-url]
[![Test coverage][coveralls-image]][coveralls-url]
[![NPM version][npm-image]][npm-url]
[![npm download][download-image]][download-url]

[npm-image]: http://img.shields.io/npm/v/css-hot-loader.svg?style=flat-square
[npm-url]: http://npmjs.org/package/css-hot-loader
[download-image]: https://img.shields.io/npm/dm/css-hot-loader.svg?style=flat-square
[download-url]: https://npmjs.org/package/css-hot-loader
[travis-image]: https://img.shields.io/travis/shepherdwind/css-hot-loader.svg?style=flat-square
[travis-url]: https://travis-ci.org/shepherdwind/css-hot-loader
[coveralls-image]: https://img.shields.io/coveralls/shepherdwind/css-hot-loader.svg?style=flat-square
[coveralls-url]: https://coveralls.io/r/shepherdwind/css-hot-loader?branch=master

This is a css hot loader, which support hot module replacement for an extracted css file.

### Why we need css hot loader

In most cases, we can realize css hot reload by [style-loader](https://github.com/webpack/style-loader) . But style-loader need inject style tag into document, Before js ready, the web page will have no any style. That is not good experience.

Also, a lots of people thought about that, How can realize hot reload with
extract-text-webpack-plugin. For example [#30](https://github.com/webpack-contrib/extract-text-webpack-plugin/issues/30) , [#!89](https://github.com/webpack-contrib/extract-text-webpack-plugin/pull/89).

So I wrote this loader, which supports hot module replacement for an extracted css file.

### Install

First install package from npm

```sh
$ npm install css-hot-loader --save-dev
```

Then config webpack.config.js

```javascript
module: {
  rules: [
    {
      test: /\.css/,
      use: [
        'css-hot-loader',
        MiniCssExtractPlugin.loader,
        'css-loader',
      ],
    },
  ] // end rules
},
```

There is an issue to work with webpack4 [#37](https://github.com/shepherdwind/css-hot-loader/issues/37).
Please use [mini-css-extract-plugin](https://github.com/webpack-contrib/mini-css-extract-plugin) to replace extract-text-webpack-plugin.

### Attention

This plugin require the output css file name static. If output file name depend
on css content, for example `'bundle.[name].[contenthash].css'`, HMR reload will
fail, more detail refer to [#21](https://github.com/shepherdwind/css-hot-loader/issues/21).


### webpack 1.x

Config file example should like this

```javascript
  module: {
    loaders: [{
      test: /\.less$/,
      loaders: [
        'css-hot-loader',
        'extract-text-webpack-plugin',
        'less',
        ...
       ],
      include: path.join(__dirname, 'src')
    }]
  }
```

See more examples code from https://github.com/shepherdwind/css-hot-loader/tree/v1.4.3/examples

### options

#### fileMap

Option to define you css file reload rule. Since 1.1.0 .

For example `'css-hot-loader?fileMap='../css/{fileName}'` , which mean

```
js/foo.js => css/foo.css
```

Default value is `{fileName}`.

see [#3](https://github.com/shepherdwind/css-hot-loader/issues/3).

#### reloadAll

Force reload all css file.

#### cssModule

When this option is opened, every time you modify the css file, the js file will
reload too. Default closed, this option use with css module.

see [!47](https://github.com/shepherdwind/css-hot-loader/pull/47) and [!51](https://github.com/shepherdwind/css-hot-loader/pull/51)

### How


The realization principle of this loader is very simple. There are some assumed condition:

1. css required by js , so css also be a js file
2. The name of css file, which need hot reload , is the same as js file excuted.

The secend assumption is often established. If you use extract-text-webpack-plugin , entry `foo.js` will extract css file `foo.css`. This principle will help us to locate the url of css file extracted.

Because every css file will be a js module , every css file change can affect a module change. CSS hot loader will accept this kind change, then find extracted css file by `document.currentScript`.

So when a css file changed, We just need find which css file link element, and reload css file.

### License

(The MIT License)
