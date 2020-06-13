'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'quotes',
  'defaults': {
    'style': 'single'
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('string', function (node) {
      var firstQuote = node.content.charAt(0),
          lastQuote = node.content.charAt(node.content.length - 1);

      if (firstQuote !== lastQuote) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': node.start.line,
          'column': node.start.column,
          'message': 'Mixed quote styles',
          'severity': parser.severity
        });
      }

      if (parser.options.style === 'single' && firstQuote !== '\'') {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': node.start.line,
          'column': node.start.column,
          'message': 'Strings must use single quotes',
          'severity': parser.severity
        });
      }
      else if (parser.options.style === 'double' && firstQuote !== '"') {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': node.start.line,
          'column': node.start.column,
          'message': 'Strings must use double quotes',
          'severity': parser.severity
        });
      }
    });

    return result;
  }
};
