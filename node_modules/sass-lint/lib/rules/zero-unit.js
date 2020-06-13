'use strict';

var helpers = require('../helpers');

var units = [
  '%',
  'em',
  'ex',
  'ch',
  'rem',
  'vh',
  'vw',
  'vmin',
  'vmax',
  'px',
  'mm',
  'cm',
  'in',
  'pt',
  'pc'
];

module.exports = {
  'name': 'zero-unit',
  'defaults': {
    'include': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('number', function (item, i, parent) {

      if (item.content === '0') {
        if (parent.type === 'dimension') {
          var next = parent.content[i + 1] || false;

          if (units.indexOf(next.content) !== -1) {
            if (!parser.options.include) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'severity': parser.severity,
                'line': item.end.line,
                'column': item.end.column,
                'message': 'No unit allowed for values of 0'
              });
            }
          }
        }
        else {
          if (parent.type === 'value') {
            if (parser.options.include) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'severity': parser.severity,
                'line': item.end.line,
                'column': item.end.column,
                'message': 'Unit required for values of 0'
              });
            }
          }
        }
      }
    });

    return result;
  }
};
