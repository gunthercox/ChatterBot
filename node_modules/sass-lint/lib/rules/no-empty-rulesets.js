'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-empty-rulesets',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('block', function (block) {
      var nonSpaceCount = 0,
          empty = false;

      if (block.content.length === 0) {
        empty = true;
      }
      else {
        block.traverse(function (item) {
          if (!helpers.isEqual(block, item)) {
            if (item.type !== 'space' &&
                item.type !== 'singlelineComment' &&
                item.type !== 'multilineComment') {
              nonSpaceCount++;
            }
          }
        });
        if (nonSpaceCount === 0) {
          empty = true;
        }
      }

      if (empty) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'severity': parser.severity,
          'line': block.start.line,
          'column': block.start.column,
          'message': 'No empty blocks allowed'
        });
      }
    });


    return result;
  }
};
