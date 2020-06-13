'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'extends-before-declarations',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [],
        error;

    ast.traverseByType('block', function (block) {
      var lastDeclaration = null;

      block.forEach(function (item, j) {
        if (item.is('include') || item.is('extend')) {
          if (item.contains('atkeyword')) {
            var atkeyword = item.first('atkeyword');

            if (atkeyword.contains('ident')) {
              var ident = atkeyword.first('ident');

              if (ident.content === 'extend') {
                if (j > lastDeclaration && lastDeclaration !== null) {
                  error = {
                    'ruleId': parser.rule.name,
                    'line': item.start.line,
                    'column': item.start.column,
                    'message': 'Extends should come before declarations',
                    'severity': parser.severity
                  };
                  result = helpers.addUnique(result, error);
                }
              }
            }
          }
        }

        if (item.is('declaration')) {
          lastDeclaration = j;
        }
      });
      lastDeclaration = null;
    });

    return result;
  }
};
