'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'max-file-line-count',
  'defaults': {
    length: 300
  },
  'detect': function (ast, parser) {
    var result = [];

    if (ast.end.line > parser.options.length) {
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': ast.end.line,
        'column': 0,
        'message': 'This file has ' + ast.end.line + ' lines, which exceeds the maximum of ' + parser.options.length + ' lines allowed.',
        'severity': parser.severity
      });
    }

    return result;
  }
};
