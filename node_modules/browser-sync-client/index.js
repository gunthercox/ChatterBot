"use strict";

var etag = require("etag");
var fresh = require("fresh");
var fs = require("fs");
var path = require("path");
var zlib = require("zlib");

var minifiedScript = path.join(__dirname, "dist", "index.min.js");
var unminifiedScript = path.join(__dirname, "dist", "index.js");

/**
 * Does the current request support compressed encoding?
 * @param {Object} req
 * @returns {boolean}
 */
function supportsGzip(req) {
    var accept = req.headers["accept-encoding"];
    return accept && accept.indexOf("gzip") > -1;
}

/**
 * Set headers on the response
 * @param {Object} res
 * @param {String} body
 */
function setHeaders(res, body) {
    res.setHeader("Cache-Control", "public, max-age=0");
    res.setHeader("Content-Type", "text/javascript");
    res.setHeader("ETag", etag(body));
}

/**
 * @param {Object} req
 * @returns {String}
 */
function isConditionalGet(req) {
    return req.headers["if-none-match"] || req.headers["if-modified-since"];
}

/**
 * Return a not-modified response
 * @param {Object} res
 */
function notModified(res) {
    res.removeHeader("Content-Type");
    res.statusCode = 304;
    res.end();
}

function processItems(items) {
    return [].concat(items)
        .filter(Boolean)
        .reduce((stringOutput, item) => {
            if (typeof item === 'string') {
                return stringOutput + item;
            }
            if (typeof item === 'function') {
                return stringOutput + item();
            }
            return stringOutput;
        }, "");
}

/**
 * Public method for returning either a middleware fn
 * or the content as a string
 * @param {Object} options
 * @param requestBody
 * @param {String} type - either `file` or `middleware`
 * @returns {*}
 */
function init(options, requestBody, type) {
    /**
     * If the user asked for a file, simply return the string.
     */
    if (type && type === "file") {
        return processItems(requestBody);
    }

    /**
     * Otherwise return a function to be used a middleware
     */
    return function(req, res) {
        /**
         * default to using the uncompressed string
         * @type {String}
         */
        var output = processItems(requestBody);

        /**
         * Set the appropriate headers for caching
         */
        setHeaders(res, output);
        var resHeaders = res.getHeaders ? res.getHeaders() : res._headers;
        if (isConditionalGet(req) && fresh(req.headers, resHeaders)) {
            return notModified(res);
        }

        /**
         * If gzip is supported, compress the string once
         * and save for future requests
         */
        if (supportsGzip(req)) {
            res.setHeader("Content-Encoding", "gzip");
            var buf = new Buffer(output, "utf-8");
            zlib.gzip(buf, function(_, result) {
                res.end(result);
            });
        } else {
            res.end(output);
        }
    };
}

module.exports.middleware = init;
module.exports.plugin = init;
module.exports.minified = function() {
    return fs.readFileSync(minifiedScript, "utf8");
};
module.exports.unminified = function() {
    return fs.readFileSync(unminifiedScript, "utf8");
};
