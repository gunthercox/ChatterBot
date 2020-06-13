'use strict';

var helpers = require('../helpers');

/**
 * Check if it's an exception (combinator or a parent selector before or after a space)
 *
 * @param {Object} node - The node to check
 * @param {Object} next - The next node
 * @param {Object} previous - The previous node
 * @returns {Boolean} True if exception
 */
var isException = function (node, next, previous) {
  if (node.is('space')) {
    if (next && next.is('combinator') || next.is('parentSelector')) {
      return true;
    }

    if (previous && previous.is('combinator') || previous.is('parentSelector')) {
      return true;
    }
  }

  return false;
};

module.exports = {
  'name': 'no-combinators',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('selector', function (selector) {
      selector.forEach(function (item, i) {
        var previous = selector.content[i - 1] || false,
            next = selector.content[i + 1] || false;

        if (isException(item, next, previous)) {
          return false;
        }

        if (item.is('combinator') || item.is('space')) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': item.start.line,
            'column': item.start.column,
            'message': 'Combinators are not allowed',
            'severity': parser.severity
          });
        }
        return false;
      });
    });

    return result;
  }
};
