'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'hex-notation',
  'defaults': {
    'style': 'lowercase'
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('color', function (value) {
      if (value.content.match(/[a-z]/i)) {
        if (parser.options.style === 'lowercase') {
          if (!helpers.isLowerCase(value.content)) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': value.start.line,
              'column': value.start.column,
              'message': 'Hex notation should all be lower case',
              'severity': parser.severity
            });
          }
        }
        else if (parser.options.style === 'uppercase') {
          if (!helpers.isUpperCase(value.content)) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': value.start.line,
              'column': value.start.column,
              'message': 'Hex notation should all be upper case',
              'severity': parser.severity
            });
          }
        }
      }
    });

    return result;
  }
};
