gulp-webserver [![Build Status](http://img.shields.io/travis/schickling/gulp-webserver.svg?style=flat)](https://travis-ci.org/schickling/gulp-webserver) [![](http://img.shields.io/npm/dm/gulp-webserver.svg?style=flat)](https://www.npmjs.org/package/gulp-webserver) [![](http://img.shields.io/npm/v/gulp-webserver.svg?style=flat)](https://www.npmjs.org/package/gulp-webserver)
==============

> Streaming gulp plugin to run a local webserver with LiveReload

##### Hint: This is a rewrite of [gulp-connect](https://github.com/AveVlad/gulp-connect/)

## Install

```sh
$ npm install --save-dev gulp-webserver
```

## Usage

The `gulp.src('root')` parameter is the root directory of the webserver. Multiple directories are possible.

```js
var gulp = require('gulp');
var webserver = require('gulp-webserver');

gulp.task('webserver', function() {
  gulp.src('app')
    .pipe(webserver({
      livereload: true,
      directoryListing: true,
      open: true
    }));
});
```

## Options

Key | Type | Default | Description |
--- | --- | --- | --- |
`host` | String | `localhost` | hostname of the webserver
`port` | Number | `8000` | port of the webserver
`path` | String | `/` | path to the webserver
`livereload` | Boolean/Object | `false` | whether to use livereload. For advanced options, provide an object. You can use the 'port' property to set a custom live reload port and the `filter` function to filter out files to watch. The object also needs to set `enable` property to true (e.g. `enable: true`) in order to activate the livereload mode. It is off by default.
`directoryListing` | Boolean/Object | `false` | whether to display a directory listing. For advanced options, provide an object with the 'enable' property set to true. You can use the 'path' property to set a custom path or the 'options' property to set custom [serve-index](https://github.com/expressjs/serve-index) options.
`fallback` | String | `undefined` | file to fall back to (relative to webserver root)
`open` | Boolean/String | `false` | open the localhost server in the browser. By providing a String you can specify the path to open (for complete path, use the complete url `http://my-server:8080/public/`) .
`https` | Boolean/Object | `false` | whether to use https or not. By default, `gulp-webserver` provides you with a development certificate but you remain free to specify a path for your key and certificate by providing an object like this one: `{key: 'path/to/key.pem', cert: 'path/to/cert.pem'}`.
`middleware` | Function/Array | `[]` | a connect middleware function or a list of middleware functions
`proxies` | Array | `[]`| a list of proxy objects.  Each proxy object can be specified by `{source: '/abc', target: 'http://localhost:8080/abc', options: {headers: {'ABC_HEADER': 'abc'}}}`.

## FAQ

#### Why can't I reach the server from the network?

**Solution**: Set `0.0.0.0` as `host` option.

#### How can I use `html5Mode` for my single page app with this plugin?

**Solution**: Set the `index.html` of your application as `fallback` option. For example:

```js
gulp.task('webserver', function() {
  gulp.src('app')
    .pipe(webserver({
      fallback: 'index.html'
    }));
});
```

#### How can I pass a custom filter to livereload?

**Solution**: Set `enable: true` and provide filter function in `filter:` property of the livereload object. For example:

```js
gulp.task('webserver', function() {
  gulp.src('app')
    .pipe(webserver({
      livereload: {
        enable: true, // need this set to true to enable livereload
        filter: function(fileName) {
          if (fileName.match(/.map$/)) { // exclude all source maps from livereload
            return false;
          } else {
            return true;
          }
        }
      }
    }));
});
```

#### How can I kill the running server?

**Solution**: Either by pressing `Ctrl + C` or programmatically like in this example:

```js
var stream = gulp.src('app').pipe(webserver());
stream.emit('kill');
```

## License

[MIT License](http://opensource.org/licenses/MIT)
