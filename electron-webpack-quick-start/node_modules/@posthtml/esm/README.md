[![npm][npm]][npm-url]
[![node][node]][node-url]
[![deps][deps]][deps-url]
[![tests][tests]][tests-url]
[![coverage][cover]][cover-url]
[![code style][style]][style-url]
[![chat][chat]][chat-url]

<div align="center">
  <img width="110" height="200" title="PostHTML Plugin" src="http://michael-ciniawsky.github.io/postcss-load-plugins/logo.svg">
  <img width="160" height="200" title="PostHTML" src="http://posthtml.github.io/posthtml/logo.svg">
  <a href="https://github.com/webpack/webpack">
    <img width="110" height="200"
      src="https://webpack.js.org/assets/icon-square-big.svg">
  </a>
  <h1>ESM Plugin</h1>
</div>

> ⚠️ These plugins are **helpers** mainly for `html-loader` to extract URL's and make them separate module request as ES2015 Module Imports and are not intended for general usage with `posthtml`. Other bundlers targeting ES2015 Modules (e.g Parcel, Rollup) may utilize them aswell, but usage besides `webpack` is currently untested. Feel free to open an issue if your integration
requires changes

<h2 align="center">Install</h2>

```bash
npm i -D @posthtml/esm
```

<h2 align="center">Usage</h2>

```js
const posthtml = require('posthtml')
const { urls, imports } = require('@posthtml/esm')

const html = `
<img src="path/to/url.png">
<import src="path/to/import.html"></import>
`
posthtml([ urls(), imports() ])
  .process(html, { from: './src/index.html' })
  .then((result) => {
    result.html
    result.messages
  })
```  

**result.html**
```html
<img src="${HTML__URL__0}">
${HTML__IMPORT__0}
```

**result.messages**
```js
[
  {
    type: 'import',
    plugin: '@posthtml/esm',
    url: 'path/to/url.png',
    name: `HTML__URL__0`,
    import () {
      return `import ${this.name} from '${this.url}';\n`
    }
  },
  {
    type: 'import',
    plugin: '@posthtml/esm',
    url: 'path/to/import.html',
    name: `HTML__IMPORT__0`,
    import () {
      return `import ${this.name} from '${this.url}';\n`
    }
  }
]
```

<h2 align="center">Options</h2>

### `urls`

|Name|Type|Default|Description|
|:--:|:--:|:-----:|:----------|
|**[`url`](#urls)**|`{RegExp\|Function}`|`''`|Filter URL's|

#### `{RegExp}`

```js
urls({
  url: /filter/
})
```

#### `{Function<{String} -> {Boolean}>}`

```js
urls({
  url (url) {
    return /filter/.test(url)
  }
})
```

### `imports`

|Name|Type|Default|Description|
|:--:|:--:|:-----:|:----------|
|**[`import`](#imports)**|`{RegExp\|Function}`|`''`|Filter Import URL's|
|**[`template`](#imports)**|`{String}`|`''`|Placeholder for HTML Templates|

#### `{RegExp}`

```js
imports({
  import: /filter/
})
```

#### `{Function<{String} -> {Boolean}>}`

```js
imports({
  import (url) {
    return /filter/.test(url)
  }
})
```

<h2 align="center">Maintainer</h2>

<table>
  <tbody>
   <tr>
    <td align="center">
      <img width="150" height="150"
     src="https://github.com/michael-ciniawsky.png?v=3&s=150">
      <br />
      <a href="https://github.com/michael-ciniawsky">Michael Ciniawsky</a>
    </td>
   </tr>
  <tbody>
</table>

<h2 align="center">Contributors</h2>

<!-- <table>
  <tbody>
   <tr>
    <td align="center">
      <img width="150" height="150"
      src="https://github.com/${user}.png?v=3&s=150">
      <br />
      <a href="https://github.com/${user}">${name}</a>
    </td>
   </tr>
  <tbody>
</table> -->


[npm]: https://img.shields.io/npm/v/@posthtml/esm.svg
[npm-url]: https://npmjs.com/package/@posthtml/esm

[node]: https://img.shields.io/node/v/@posthtml/esm.svg
[node-url]: https://nodejs.org/

[deps]: https://david-dm.org/posthtml/esm.svg
[deps-url]: https://david-dm.org/posthtml/esm

[tests]: http://img.shields.io/travis/posthtml/esm.svg
[tests-url]: https://travis-ci.org/posthtml/esm

[cover]: https://coveralls.io/repos/github/posthtml/esm/badge.svg
[cover-url]: https://coveralls.io/github/posthtml/esm

[style]: https://img.shields.io/badge/code%20style-standard-yellow.svg
[style-url]: http://standardjs.com/

[chat]: https://badges.gitter.im/posthtml/posthtml.svg
[chat-url]: https://gitter.im/posthtml/posthtml
