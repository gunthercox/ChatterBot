'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'attribute-quotes',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('attributeValue', function (item) {
      if (item.content[0].is('string') && !parser.options.include) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': item.start.line,
          'column': item.start.column,
          'message': 'Attribute values should not be surrounded by quotes',
          'severity': parser.severity
        });
      }
      else if (item.content[0].is('ident') && parser.options.include) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': item.start.line,
          'column': item.start.column,
          'message': 'Attribute values should be surrounded by quotes',
          'severity': parser.severity
        });
      }
    });

    return result;
  }
};
