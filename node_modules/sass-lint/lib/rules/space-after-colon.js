'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'space-after-colon',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByTypes(['propertyDelimiter', 'operator'], function (delimiter, i, parent) {
      if (!parent.is('atrule')) {
        if (delimiter.content === ':') {
          var next = parent.content[i + 1];
          if (next && next.is('space')) {
            if (!parser.options.include) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': next.start.line,
                'column': next.start.column,
                'message': 'No space allowed after `:`',
                'severity': parser.severity
              });
            }
          }
          else {
            if (parser.options.include) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': delimiter.start.line,
                'column': delimiter.start.column,
                'message': 'Space expected after `:`',
                'severity': parser.severity
              });
            }
          }
        }
      }
    });

    return result;
  }
};
