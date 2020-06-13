var owns = {}.hasOwnProperty;
module.exports = function proxyMiddleware(options) {
  
  var httpLib = options.protocol === 'https:' ? 'https' : 'http';
  var request = require(httpLib).request;
  options = options || {};
  options.hostname = options.hostname;
  options.port = options.port;

  return function (req, resp, next) {
    var url = req.url;
    // You can pass the route within the options, as well
    if (typeof options.route === 'string') {
      var route = slashJoin(options.route, '');
      if (url.slice(0, route.length) === route) {
        url = url.slice(route.length);
      } else {
        return next();
      }
    }

    //options for this request
    var opts = extend({}, options);
    opts.path = slashJoin(options.pathname, url);
    opts.method = req.method;
    opts.headers = options.headers ? merge(req.headers, options.headers) : req.headers;

    applyViaHeader(req.headers, opts, opts.headers);

    // Forwarding the host breaks dotcloud
    delete opts.headers["host"];
    
    var myReq = request(opts, function (myRes) {
      var statusCode = myRes.statusCode
        , headers = myRes.headers
        , location = headers.location;
      // Fix the location
      if (statusCode > 300 && statusCode < 304 && location.indexOf(options.href) > -1) {
        // absoulte path
        headers.location = location.replace(options.href, slashJoin('', slashJoin((options.route || ''), '')));
      }
      applyViaHeader(myRes.headers, opts, myRes.headers);
      resp.writeHead(myRes.statusCode, myRes.headers);
      myRes.on('error', function (err) {
        next(err);
      });
      myRes.pipe(resp);
    });
    myReq.on('error', function (err) {
      next(err);
    });
    if (!req.readable) {
      myReq.end();
    } else {
      req.pipe(myReq);
    }
  };
};

function applyViaHeader(existingHeaders, opts, applyTo) {

  if(!opts.via) {
    return;
  }
  
  var viaName = (true === opts.via) ?
    // use the host name
    require('os').hostname() :
    // or use whatever was passed as the options.via value
    opts.via;

    var viaHeader = '1.1 ' + viaName;

    if(existingHeaders.via) {
        viaHeader = existingHeaders.via + ', ' + viaHeader;
    }

    applyTo.via = viaHeader;

}

function slashJoin(p1, p2) {
  if (p1.length && p1[p1.length - 1] === '/') {p1 = p1.substring(0, p1.length - 1); }
  if (p2.length && p2[0] === '/') {p2 = p2.substring(1); }
  return p1 + '/' + p2;
}

function extend(obj, src) {
  for (var key in src) if (owns.call(src, key)) obj[key] = src[key];
  return obj;
}

//merges data without changing state in either argument
function merge(src1, src2) {
    var merged = {};
    extend(merged, src1);
    extend(merged, src2);
    return merged;
}
