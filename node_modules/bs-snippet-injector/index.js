var fs    = require("fs");
var path  = require("path");

/**
 * @type {string}
 */
var PLUGIN_NAME = "Snippet Injector";

/**
 * @type
 */
var messages = {
    added: function (path) {
        return "{green:Snippet added to {cyan:" + path
    },
    removed: function (path) {
        return "{green:Snippet removed from {cyan:" + path
    },
    exists: function (path) {
        return "{green:Snippet already exists in: {cyan:" + path
    },
    notFound: function (path) {
        return "{red:ERROR:} Closing body tag not found in: {cyan:" + path
    },
    fileNotFound: function (path) {
        return "{red:ERROR:} File not found!: {cyan:" + path
    }
};

/**
 * Main export
 * @type {{name: string, plugin: plugin}}
 */
module.exports = {

    "plugin:name": PLUGIN_NAME,

    plugin: function (opts, bs) {

        opts.file = opts.file || "";

        opts.currentFilePath = path.resolve(opts.file);

        opts.logger = bs.getLogger(PLUGIN_NAME);
        opts.logger.debug("Setting events");

        bs.events.on("service:running", addSnippet.bind(null, bs, opts));
        bs.events.on("service:exit",  removeSnippet.bind(null, bs, opts));
    }
};


/**
 * Add the snippet before a body tag
 * @param {BrowserSync} bs
 * @param {Object} opts - plugin specific options
 */
function addSnippet(bs, opts) {

    var currentFilePath = opts.currentFilePath;

    opts.logger.debug("Reading the file: %s", currentFilePath);

    var read;

    try {
        read = fs.readFileSync(currentFilePath, "utf8");
    } catch (e) {
        opts.errored = true;
        return opts.logger.info(messages.fileNotFound(path.basename(currentFilePath)));
    }

    var found = false;

    if (read.indexOf(bs.options.get("snippet")) > -1) {
        opts.logger.info(messages.exists(currentFilePath));
        return;
    }

    var modded = read.replace(/<\/body>(?![\s\S]*<\/body>)/, function () {
        opts.currentSnippet = wrap(bs.options.get("snippet")) + "\n" + arguments[0];
        found = true;
        return opts.currentSnippet;
    });

    if (found) {
        opts.logger.debug("Writing the file: %s", currentFilePath);
        fs.writeFileSync(currentFilePath, modded);
        opts.logger.info(messages.added(path.basename(currentFilePath)));
    } else {
        opts.logger.info(messages.notFound(path.basename(currentFilePath)));
    }
}

/**
 * @param item snippet
 * @returns {string}
 */
function wrap (item) {
    return "<!-- BS:SNIPPET-->" + item + "<!-- BS:SNIPPET:END-->";
}

/**
 * @param {BrowserSync} bs
 * @param {Object} opts - plugin specific options
 */
function removeSnippet(bs, opts) {

    if (opts.errored) {
        return;
    }

    var read   = fs.readFileSync(opts.currentFilePath, "utf8");
    var modded = read.replace(opts.currentSnippet, function () {
        return "</body>";
    });
    fs.writeFileSync(opts.currentFilePath, modded);
    opts.logger.info(messages.removed(path.basename(opts.currentFilePath)));
}