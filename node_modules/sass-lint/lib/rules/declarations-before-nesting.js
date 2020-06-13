'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'declarations-before-nesting',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [],
        error;

    ast.traverseByType('block', function (block) {
      if (block.contains('ruleset') && block.contains('declaration')) {
        var rulesetIndex;

        block.forEach(function (item, j) {
          var declarationIndex;
          var declaration;

          if (item.is('ruleset') && rulesetIndex === void 0) {
            rulesetIndex = j;
          }

          if (item.is('declaration')) {
            var property = item.content[0];

            if (property && property.is('property')) {
              if (property.content[0] && property.content[0].is('variable')) {
                return;
              }
            }

            declarationIndex = j;
            declaration = item;
          }

          if (rulesetIndex < declarationIndex && declaration) {
            error = {
              'ruleId': parser.rule.name,
              'line': declaration.start.line,
              'column': declaration.start.column,
              'message': 'Declarations should come before nestings',
              'severity': parser.severity
            };
            result = helpers.addUnique(result, error);
          }
        });

        rulesetIndex = null;
      }
    });

    return result;
  }
};
