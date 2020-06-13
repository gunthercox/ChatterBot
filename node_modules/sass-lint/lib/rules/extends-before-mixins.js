'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'extends-before-mixins',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('block', function (block) {
      var lastMixin = null;

      block.forEach(function (item, j) {
        if (item.is('include') || item.is('extend')) {
          if (item.contains('atkeyword')) {
            var atkeyword = item.first('atkeyword');

            if (atkeyword.contains('ident')) {
              var ident = atkeyword.first('ident');

              if (ident.content === 'extend') {
                if (j > lastMixin && lastMixin !== null) {
                  result = helpers.addUnique(result, {
                    'ruleId': parser.rule.name,
                    'line': item.start.line,
                    'column': item.start.column,
                    'message': 'Extends should come before mixins',
                    'severity': parser.severity
                  });
                }
              }
            }
          }
        }

        if (item.is('include')) {
          lastMixin = j;
        }
      });

      lastMixin = null;
    });

    return result;
  }
};
