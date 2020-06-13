'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-trailing-whitespace',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];
    var trailing = (/( |\t)+\n/);
    var trailingCRLF = (/( |\t)+\r\n/);

    ast.traverseByType('space', function (space, i, parent) {
      var content = space.content;
      var nextIndex = i + 1;
      var next = parent.content[nextIndex];

      while (next && (next.is('space') || next.is('declarationDelimiter'))) {
        content += next.content;
        nextIndex++;
        next = parent.content[nextIndex];
      }

      if (trailing.test(content) || trailingCRLF.test(content)) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'severity': parser.severity,
          'line': space.start.line,
          'column': space.start.column,
          'message': 'No trailing whitespace allowed'
        });
      }
    });

    return result;
  }
};

