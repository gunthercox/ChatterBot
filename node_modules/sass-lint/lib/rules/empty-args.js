'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'empty-args',
  'defaults': {
    'include': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByTypes(['mixin', 'include'], function (item) {
      if (item.contains('arguments')) {
        item.traverse(function (node) {
          if (node.type === 'arguments') {
            if (node.content.length === 0) {
              if (!parser.options.include) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': node.start.line,
                  'column': node.start.column,
                  'message': 'Parenthesis should be removed.',
                  'severity': parser.severity
                });
              }
            }
          }
        });
      }
      else {
        if (parser.options.include) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': item.start.line,
            'column': item.start.column,
            'message': 'Parenthesis are required.',
            'severity': parser.severity
          });
        }
      }
    });

    return result;
  }
};
