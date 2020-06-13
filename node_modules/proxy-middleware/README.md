[![Build Status](https://secure.travis-ci.org/andrewrk/connect-proxy.png)](http://travis-ci.org/andrewrk/connect-proxy)

### Usage:

```js
var connect = require('connect');
var url = require('url');
var proxy = require('proxy-middleware');

var app = connect();
app.use('/api', proxy(url.parse('https://example.com/endpoint')));
// now requests to '/api/x/y/z' are proxied to 'https://example.com/endpoint/x/y/z'
```

### Documentation:

`proxyMiddleware(options)`

`options` allows any options that are permitted on the [`http`](http://nodejs.org/api/http.html#http_http_request_options_callback) or [`https`](http://nodejs.org/api/https.html#https_https_request_options_callback) request options.

Other options:
- `route`: you can pass the route for connect middleware within the options, as well.
- `via`: by default no [via header](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.45) is added. If you pass `true` for this option the local hostname will be used for the via header. You can also pass a string for this option in which case that will be used for the via header.

### Usage with route:

```js
var proxyOptions = url.parse('https://example.com/endpoint');
proxyOptions.route = '/api';

var middleWares = [proxy(proxyOptions) /*, ...*/];

// Grunt connect uses this method
connect(middleWares);
```
