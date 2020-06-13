'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-ids',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('id', function (id) {
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': id.start.line,
        'column': id.start.column,
        'message': 'ID selectors not allowed',
        'severity': parser.severity
      });
    });

    return result;
  }
};
