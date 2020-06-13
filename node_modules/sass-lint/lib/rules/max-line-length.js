'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'max-line-length',
  'defaults': {
    length: 80
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('space', function (space) {
      var lineLength = 0;
      if (helpers.hasEOL(space.content)) {
        lineLength = space.start.column - 1;
      }

      if (lineLength > parser.options.length) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'severity': parser.severity,
          'line': space.start.line,
          'column': 0,
          'message': 'line ' + space.start.line + ' exceeds the maximum line length of ' + parser.options.length
        });
      }
    });

    return result;
  }
};
