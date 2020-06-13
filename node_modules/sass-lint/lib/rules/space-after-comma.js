'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'space-after-comma',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByTypes(['operator', 'delimiter'], function (operator, i, parent) {
      var next,
          doubleNext;

      if (operator.content === ',') {
        next = parent.content[i + 1] || false;
        doubleNext = parent.content[i + 2] || false;

        if (next) {
          if (operator.is('delimiter')) {
            if (next.is('selector')) {
              next = next.content[0];
            }
          }

          if ((next.is('space') && !helpers.hasEOL(next.content)) && !parser.options.include) {
            if (doubleNext && doubleNext.is('singlelineComment')) {
              return false;
            }

            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': next.start.line,
              'column': next.start.column,
              'message': 'Commas should not be followed by a space',
              'severity': parser.severity
            });
          }

          if (!next.is('space') && parser.options.include) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': operator.start.line,
              'column': operator.start.column,
              'message': 'Commas should be followed by a space',
              'severity': parser.severity
            });
          }
        }
      }
      return true;
    });

    return result;
  }
};
