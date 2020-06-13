'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-attribute-selectors',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('attributeSelector', function (item) {
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': item.start.line,
        'column': item.start.column,
        'message': 'Attribute selectors are not allowed',
        'severity': parser.severity
      });
    });

    return result;
  }
};
