'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-transition-all',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('declaration', function (declaration) {

      if (declaration.first('property')) {
        if (declaration.first('property').first('ident')) {
          var propertyName = declaration.first('property').first('ident').content;

          if (propertyName.charAt(0) === '-') {
            propertyName = helpers.stripPrefix(propertyName);
          }

          if (propertyName === 'transition' || propertyName === 'transition-property' ) {
            declaration.forEach('value', function (val) {
              val.forEach('ident', function (ident) {
                if (ident.content === 'all') {
                  result = helpers.addUnique(result, {
                    'ruleId': parser.rule.name,
                    'line': declaration.start.line,
                    'column': declaration.start.column,
                    'message': 'The keyword `all` should not be used with the property `' + propertyName + '`',
                    'severity': parser.severity
                  });
                }
              });
            });
          }
        }
      }
    });
    return result;
  }
};
