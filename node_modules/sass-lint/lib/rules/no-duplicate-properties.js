'use strict';

var helpers = require('../helpers');
var selectorHelpers = require('../selector-helpers');

module.exports = {
  'name': 'no-duplicate-properties',
  'defaults': {
    'exclude': []
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('block', function (block) {
      var properties = [],
          items = [],
          warnMessage = false;

      block.eachFor('declaration', function (declaration) {
        items.push(declaration);
      });

      items.reverse();

      items.forEach(function (declaration) {
        warnMessage = false;

        declaration.eachFor('property', function (item) {
          var property = '';

          // Check if declaration is actually a variable declaration
          if (item.content[0] && item.content[0].is('variable')) {
            return;
          }

          item.forEach(function (subItem) {
            // Although not a selector the method here helps us construct the proper property name
            // taking into account any interpolation etc
            property += selectorHelpers.constructSelector(subItem);
          });

          if (properties.indexOf(property) !== -1 && properties.length >= 1) {
            if (parser.options.exclude.indexOf(property) !== -1 && properties[properties.length - 1] !== property) {
              warnMessage = 'Excluded duplicate properties must directly follow each other.';
            }
            else if (parser.options.exclude.indexOf(property) === -1) {
              warnMessage = 'Duplicate properties are not allowed within a block';
            }
          }

          properties.push(property);

          if (warnMessage) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': item.start.line,
              'column': item.start.column,
              'message': warnMessage,
              'severity': parser.severity
            });
          }
        });
      });
    });

    return result;
  }
};
