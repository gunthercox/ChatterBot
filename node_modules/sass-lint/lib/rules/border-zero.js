'use strict';

var helpers = require('../helpers');

var borders = ['border', 'border-top', 'border-right', 'border-bottom', 'border-left'];
var allowedConventions = ['0', 'none'];

module.exports = {
  'name': 'border-zero',
  'defaults': {
    'convention': '0'
  },
  'detect': function (ast, parser) {
    var result = [];
    var userConvention = parser.options.convention.toString();
    var convention = allowedConventions.indexOf(userConvention) !== -1
      ? userConvention
      : allowedConventions[0];
    var invalidConvention = convention !== userConvention;

    ast.traverseByType('declaration', function (declaration) {
      var isBorder = false;

      declaration.traverse(function (item) {
        if (item.type === 'property') {
          item.traverse(function (child) {
            if (borders.indexOf(child.content) !== -1) {
              isBorder = true;
            }
          });
        }

        if (isBorder) {
          if (item.type === 'value') {
            var node = item.content[0];
            if (node.type === 'number' || node.type === 'ident') {
              if (node.content === '0' || node.content === 'none') {
                if (convention !== node.content) {
                  if (invalidConvention) {
                    invalidConvention = false;
                    result = helpers.addUnique(result, {
                      'ruleId': parser.rule.name,
                      'line': 1,
                      'column': 1,
                      'message': 'The border-zero convention `' + userConvention + ' in your config file is not valid. Defaulted to convention \'0\'',
                      'severity': parser.severity
                    });
                  }
                  result = helpers.addUnique(result, {
                    'ruleId': parser.rule.name,
                    'line': node.start.line,
                    'column': node.start.column,
                    'message': 'A value of `' + node.content + '` is not allowed. `' + convention + '` must be used.',
                    'severity': parser.severity
                  });
                }
              }
            }
          }
        }
      });
    });

    return result;
  }
};
