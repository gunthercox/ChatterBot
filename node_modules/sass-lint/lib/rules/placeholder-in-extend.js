'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'placeholder-in-extend',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('atkeyword', function (keyword, i, parent) {
      keyword.forEach(function (item) {
        if (item.content === 'extend') {

          parent.forEach('selector', function (selector) {
            var placeholder = false;

            selector.content.forEach(function (selectorPiece) {
              if (selectorPiece.type === 'placeholder') {
                placeholder = true;
              }
            });

            if (!placeholder) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': selector.start.line,
                'column': selector.start.column,
                'message': '@extend must be used with a %placeholder',
                'severity': parser.severity
              });
            }
          });
        }
      });
    });

    return result;
  }
};
