'use strict';

var helpers = require('../helpers');

/**
 * Get the 'last' node of the tree to test for an EOL
 *
 * @param {Object} node - The node whose last child we want to return
 * @returns {Object} The last node
 */
var getLastNode = function (node) {
  var last = node.last();

  return last ? getLastNode(last) : node;
};

module.exports = {
  'name': 'final-newline',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [],
        last,
        error = {
          'ruleId': parser.rule.name,
          'severity': parser.severity
        };

    // If the syntax is Sass we must recursively loop to determine the last node.
    // This is not required for SCSS which will always use the last node in the
    // content of the parent stylesheet node
    if (ast.syntax === 'sass') {
      last = getLastNode(ast);
    }
    else {
      last = ast.content[ast.content.length - 1];
    }

    if (!last.is('space') && !last.is('declarationDelimiter')) {
      if (parser.options.include) {
        error.line = last.end.line;
        error.column = last.end.column;
        error.message = 'Files must end with a new line';
        result = helpers.addUnique(result, error);
      }
    }
    else if ((last.is('space') || last.is('declarationDelimiter'))) {
      if (!helpers.hasEOL(last.content) && parser.options.include) {
        error.line = last.start.line;
        error.column = last.start.column;
        error.message = 'Files must end with a new line';
        result = helpers.addUnique(result, error);
      }
      else if (helpers.hasEOL(last.content) && !parser.options.include) {
        error.line = last.start.line;
        error.column = last.start.column;
        error.message = 'Files must not end with a new line';
        result = helpers.addUnique(result, error);
      }
    }

    return result;
  }
};
