'use strict';

var helpers = require('../helpers');

var leadingZeroRegex = /^0\.\d+$/,
    noLeadingZeroRegex = /^\.\d+$/;

module.exports = {
  'name': 'leading-zero',
  'defaults': {
    'include': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('number', function (num) {
      if (num.content.match(/^-?(0?\.\d+)/)) {
        if (num.content.match(leadingZeroRegex)) {
          if (!parser.options.include) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': num.start.line,
              'column': num.start.column,
              'message': 'Don\'t include leading zeros on numbers',
              'severity': parser.severity
            });
          }
        }
        if (num.content.match(noLeadingZeroRegex)) {
          if (parser.options.include) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': num.start.line,
              'column': num.start.column - 1,
              'message': 'Include leading zeros on numbers',
              'severity': parser.severity
            });
          }
        }
      }
    });

    return result;
  }
};
