'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-debug',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('atkeyword', function (keyword) {
      keyword.traverse(function (item) {
        if (item.content === 'debug') {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': item.start.line,
            'column': item.start.column,
            'message': '@debug not allowed',
            'severity': parser.severity
          });
        }
      });
    });

    return result;
  }
};
