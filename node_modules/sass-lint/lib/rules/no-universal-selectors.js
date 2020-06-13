'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-universal-selectors',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('universalSelector', function (node) {
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': node.start.line,
        'column': node.start.column,
        'message': '* (universal) selectors are not allowed',
        'severity': parser.severity
      });
    });

    return result;
  }
};
