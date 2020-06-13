//////////////////////////////
// Tree Abstraction
//////////////////////////////
'use strict';

var gonzales = require('gonzales-pe-sl');
var fm = require('front-matter');
var helpers = require('./helpers');

module.exports = function (text, syntax, filename) {
  var tree;

  // Run `.toString()` to allow Buffers to be passed in
  text = helpers.stripBom(text.toString());

  // if we're skipping front matter do it here, fall back to just our text in case it fails
  if (fm.test(text)) {
    var withFrontMatter = fm(text);
    // Replace front matter by empty lines, so that line numbers are preserved
    var numEmptyLines = 2;
    if (withFrontMatter.frontmatter !== '') {
      numEmptyLines += withFrontMatter.frontmatter.split('\r\n|\r|\n').length;
    }
    var emptyLines = new Array(numEmptyLines + 1).join('\n');
    text = emptyLines + withFrontMatter.body || text;
  }

  try {
    tree = gonzales.parse(text, {
      'syntax': syntax
    });
  }
  catch (e) {
    throw {
      message: e.message,
      file: filename,
      line: e.line
    };
  }

  if (typeof tree === 'undefined') {
    throw {
      message: 'Undefined tree',
      file: filename,
      text: text.toString(),
      tree: tree.toString()
    };
  }

  return tree;
};
