'use strict';

var helpers = require('../helpers');
var lengths = {
  short: 3,
  long: 6
};
var canShorten = function (hex) {
  return hex.length === lengths.long &&
          hex[0] === hex[1] &&
          hex[2] === hex[3] &&
          hex[4] === hex[5];
};

module.exports = {
  'name': 'hex-length',
  'defaults': {
    'style': 'short'
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('color', function (value) {
      if (parser.options.style === 'short' && canShorten(value.content)) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': value.start.line,
          'column': value.start.column,
          'message': 'Hex values should use the shorthand format - 3 characters where possible',
          'severity': parser.severity
        });
      }
      else if (parser.options.style === 'long') {
        if (value.content.length !== lengths.long) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': value.start.line,
            'column': value.start.column,
            'message': 'Hex values should use the long-form format - 6 characters',
            'severity': parser.severity
          });
        }
      }
    });

    return result;
  }
};
