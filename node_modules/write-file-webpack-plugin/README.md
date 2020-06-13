# write-file-webpack-plugin

[![NPM version](http://img.shields.io/npm/v/write-file-webpack-plugin.svg?style=flat-square)](https://www.npmjs.com/package/write-file-webpack-plugin)
[![js-canonical-style](https://img.shields.io/badge/code%20style-canonical-blue.svg?style=flat-square)](https://github.com/gajus/canonical)

Forces `webpack-dev-server` program to write bundle files to the file system.

This plugin has no effect when [`webpack`](https://webpack.github.io/docs/usage.html) program
is used instead of [`webpack-dev-server`](https://webpack.github.io/docs/webpack-dev-server.html).

## Install

```sh
npm install write-file-webpack-plugin --save-dev
```

## API

```js
/**
 * @typedef {Object} options
 * @property {boolean} atomicReplace Atomically replace files content (i.e., to prevent programs like test watchers from seeing partial files) (default: true).
 * @property {boolean} exitOnErrors Stop writing files on webpack errors (default: true).
 * @property {boolean} force Forces the execution of the plugin regardless of being using `webpack-dev-server` or not (default: false).
 * @property {boolean} log Logs names of the files that are being written (or skipped because they have not changed) (default: true).
 * @property {RegExp} test A regular expression used to test if file should be written. When not present, all bundle will be written.
 * @property {boolean} useHashIndex Use hash index to write only files that have changed since the last iteration (default: true).
 */

/**
 * @param {options} options
 * @returns {Object}
 */
new WriteFilePlugin();

new WriteFilePlugin({
    // Write only files that have ".css" extension.
    test: /\.css$/,
    useHashIndex: true
});
```

## Usage

Configure [`webpack.config.js`](https://webpack.github.io/docs/configuration.html) to use the `write-file-webpack-plugin` plugin.

```js
import path from 'path';
import WriteFilePlugin from 'write-file-webpack-plugin';

export default {
    output: {
        path: path.join(__dirname, './dist')
    },
    plugins: [
        new WriteFilePlugin()
    ],
    // ...
}
```

See [./sandbox](./sandbox) for a working `webpack` configuration.
