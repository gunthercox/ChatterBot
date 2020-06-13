'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-invalid-hex',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('color', function (value) {
      if (!helpers.isValidHex(value.content)) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': value.start.line,
          'column': value.start.column,
          'message': 'Hexadecimal values must be a valid format',
          'severity': parser.severity
        });
      }
    });
    return result;
  }
};
