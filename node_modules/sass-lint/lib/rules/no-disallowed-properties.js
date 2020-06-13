'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-disallowed-properties',
  'defaults': {
    'properties': []
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('property', function (node) {
      var first = node.first();
      if (!first.is('ident') || parser.options.properties.indexOf(first.content) === -1) {
        return;
      }
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': node.start.line,
        'column': node.start.column,
        'message': 'Property `' + first.content + '` should not be used',
        'severity': parser.severity
      });
    });
    return result;
  }
};
