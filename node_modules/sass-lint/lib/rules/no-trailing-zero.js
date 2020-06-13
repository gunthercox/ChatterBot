'use strict';

var helpers = require('../helpers');

var trailingZeroRegex = /^(\d+\.|\.)+(\d*?)0+$/;

module.exports = {
  'name': 'no-trailing-zero',
  'defaults': {
    'include': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('number', function (num) {

      if (num.content.match(trailingZeroRegex)) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': num.start.line,
          'column': num.start.column,
          'message': 'Don\'t include trailing zeros on numbers',
          'severity': parser.severity
        });
      }
    });

    return result;
  }
};
