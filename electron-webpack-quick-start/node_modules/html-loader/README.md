[![npm][npm]][npm-url]
[![node][node]][node-url]
[![deps][deps]][deps-url]
[![test][test]][test-url]
[![coverage][cover]][cover-url]
[![chat][chat]][chat-url]

<div align="center">
  <img width="180" height="180"
    src="https://worldvectorlogo.com/logos/html5.svg">
  <a href="https://github.com/webpack/webpack">
    <img width="200" height="200"
      src="https://webpack.js.org/assets/icon-square-big.svg">
  </a>
  <h1>HTML Loader</h1>
  <p>Exports HTML as `{String}` or template `{Function}`</p>
</div>

<h2 align="center">Install</h2>

```bash
npm i -D html-loader
```

<h2 align="center">Usage</h2>

By default all assets (`<img src="./image.png">`) are transpiled to their own module requests (`import HTML__URL__O from './image.png'`) to be correctly handled by `webpack` as an ES Module

> ⚠️ You need to specify additional loaders for your assets (e.g images) separately in your `webpack.config.js`, like the `file-loader` or `url-loader`, to handle these requests

**webpack.config.js**
```js
{
  test: /\.html$/,
  use: {
    loader: 'html-loader',
    options: {}
  }
}
```

### `Caching`

If your application includes many HTML Components or certain HTML Components are of significant size, we highly recommend to use the [`cache-loader`](https://github.com/webpack-contrib/cache-loader) for persistent caching (faster initial builds)

**webpack.config.js**
```js
{
  test: /\.html$/,
  use: [
    'cache-loader',
    {
      loader: 'html-loader',
      options: {}
    }
  ]
}
```


<h2 align="center">Options</h2>

|Name|Type|Default|Description|
|:--:|:--:|:-----:|:----------|
|**[`url`](#url)**|`{Boolean}`|`true`| Enable/Disable HTML Assets (`<img src="./file.png">`)|
|**[`import`](#import)** |`{Boolean}`|`true`| Enable/Disable HTML Imports (`<import src="./file.html">`)|
|**[`template`](#template)**|`{Boolean\|String}`|`false`|Export HTML as a template `{Function}`. The template placeholder defaults to `<div>${ _.x }</div>` (`_`)|
|**[`minimize`](#minimize)**|`{Boolean}`|`false`|Enable/Disable HTML Minification|

### `url`

It's possible to completely disable or filter certain URL's from resolving in case these assets shouldn't be handled by `webpack`. Protocol URL's like (`<img src="https://cnd.domain.com/image.png">`) are ignored by default

#### `{Boolean}`

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    url: false
  }
}
```

#### `{RegExp}`

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    url: /filter/
  }
}
```

#### `{Function}`

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    url (url) {
      return /filter/.test(url)
    }
  }
}
```

### `import`

**import.html**
```html
<div class="import">Import</div>
```

**file.html**
```html
<div>
  <import src="./import.html"></import>
</div>
```

#### `{Boolean}`

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    import: false
  }
}
```

#### `{RegExp}`

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    import: /filter/
  }
}
```

#### `{Function}`

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    import (url) {
      return /filter/.test(url)
    }
  }
}
```

### `template`

When set to `true` the loader will export a template `{Function}` instead of a `{String}`. The `locals` param is configurable and defaults to `_`

#### `{Boolean}`

**file.html**
```html
<div>
  <p>${ _.txt }</p>
</div>
```

**file.js**
```js
import template from './file.html'

const html = template({ txt: 'Hello World!' })

document.body.innerHTML = html
```

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    template: true
  }
}
```

#### `{String}`

Sets a custom placeholder for your template `{Function}`

**file.html**
```html
<div>
  <p>${ $.txt }</p>
</div>
```

**file.js**
```js
import template from './file.html'

const html = template({ txt: 'Hello World!' })

document.body.innerHTML = html
```

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    template: '$'
  }
}
```

### `minimize`

#### `{Boolean}`

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    minimize: true
  }
}
```

#### `{Object}`

Set custom [options](https://github.com/posthtml/htmlnano#modules) for minification

**webpack.config.js**
```js
{
  loader: 'html-loader',
  options: {
    minimize: {...options}
  }
}
```

<h2 align="center">Examples</h2>

### `HMR`

**component.js**
```js
import template from './component.html';

const component = document.createElement('div')

component.innerHTML = template({ hello: 'Hello World!' })

document.body.appendChild(component);

// HMR Interface
if (module.hot) {
  // Capture hot update
  module.hot.accept('./component.html', () => {
    // Replace old content with the hot loaded one
    component.innerHTML = template({ ...locals })
  })
}
```

### `npm Packages (Modules)`

> :information_source: Any key matching with `resolve.mainFields` is valid and should work. `pkg.template` is just used as an example here.

**package.json**
```json
{
  "name": "@package",
  "version": "1.0.0",
  "template": "path/to/component.html"
}
```

**webpack.config.js**
```js
const config = {
  module: {
    rules: [
      {
        test: /\.html$/,
        use: [ 'html-loader' ],
        resolve: {
          mainFields: [ 'template' ]
        }
      }
    ]
  }
}

module.exports = config
```

**component.html**
```html
<import src="@package"></import>
<div>...<div>
```

**component.js**
```js
import html from './file.html'

const el = document.createElement('div')

el.innerHTML = html
```

<h2 align="center">Maintainers</h2>

<table>
  <tbody>
    <tr>
      <td align="center">
        <img width="150" height="150"
        src="https://avatars.githubusercontent.com/u/18315?v=3">
        </br>
        <a href="https://github.com/hemanth">Hemanth</a>
      </td>
      <td align="center">
        <img width="150" height="150"
        src="https://avatars.githubusercontent.com/u/8420490?v=3">
        </br>
        <a href="https://github.com/d3viant0ne">Joshua Wiens</a>
      </td>
      <td align="center">
        <img width="150" height="150" src="https://avatars.githubusercontent.com/u/5419992?v=3">
        </br>
        <a href="https://github.com/michael-ciniawsky">Michael Ciniawsky</a>
      </td>
      <td align="center">
        <img width="150" height="150"
        src="https://avatars.githubusercontent.com/u/6542274?v=3">
        </br>
        <a href="https://github.com/imvetri">Imvetri</a>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img width="150" height="150"
        src="https://avatars.githubusercontent.com/u/1520965?v=3">
        </br>
        <a href="https://github.com/andreicek">Andrei Crnković</a>
      </td>
      <td align="center">
        <img width="150" height="150"
        src="https://avatars.githubusercontent.com/u/3367801?v=3">
        </br>
        <a href="https://github.com/abouthiroppy">Yuta Hiroto</a>
      </td>
      <td align="center">
        <img width="150" height="150" src="https://avatars.githubusercontent.com/u/80044?v=3">
        </br>
        <a href="https://github.com/petrunov">Vesselin Petrunov</a>
      </td>
      <td align="center">
        <img width="150" height="150"
        src="https://avatars.githubusercontent.com/u/973543?v=3">
        </br>
        <a href="https://github.com/gajus">Gajus Kuizinas</a>
      </td>
    </tr>
  </tbody>
</table>


[npm]: https://img.shields.io/npm/v/html-loader.svg
[npm-url]: https://npmjs.com/package/html-loader

[node]: https://img.shields.io/node/v/html-loader.svg
[node-url]: https://nodejs.org

[deps]: https://david-dm.org/webpack-contrib/html-loader.svg
[deps-url]: https://david-dm.org/webpack-contrib/html-loader

[test]: http://img.shields.io/travis/webpack-contrib/html-loader.svg
[test-url]: https://travis-ci.org/webpack-contrib/html-loader

[cover]: https://codecov.io/gh/webpack-contrib/html-loader/branch/master/graph/badge.svg
[cover-url]: https://codecov.io/gh/webpack-contrib/html-loader

[chat]: https://badges.gitter.im/webpack/webpack.svg
[chat-url]: https://gitter.im/webpack/webpack
