'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-css-comments',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('multilineComment', function (node) {
      if (node.content.charAt(0) !== '!') {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': node.start.line,
          'column': node.start.column,
          'message': 'Multiline style comments should not be used',
          'severity': parser.severity
        });
      }
    });
    return result;
  }
};
