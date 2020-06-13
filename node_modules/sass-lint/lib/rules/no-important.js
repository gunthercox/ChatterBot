'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-important',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('important', function (item) {
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': item.start.line,
        'column': item.start.column,
        'message': '!important not allowed',
        'severity': parser.severity
      });
    });

    return result;
  }
};
