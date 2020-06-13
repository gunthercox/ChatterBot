'use strict';

var helpers = require('../helpers'),
    capitalize = require('lodash.capitalize'),
    kebabcase = require('lodash.kebabcase');

// Our nestable selector types, separated by type for ease of use with rules
// we replace ident with 'selector' for readability'
var nestableElements = ['selector', 'class', 'id', 'typeSelector', 'parentSelectorExtension'],
    nestableAttributes = ['attributeSelector'],
    nestablePseudo = ['pseudoClass', 'pseudoElement', 'nth', 'nthSelector'];

/**
 * Formats a string from camelCase to hyphens and capitalizes
 * @param {string} str - The string to be formatted
 * @returns {string} A hyphenated and capitalized string
 */
var formatOutput = function (str) {
  return capitalize(kebabcase(str));
};

module.exports = {
  'name': 'force-element-nesting',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [],
        elements = nestableElements.concat(nestableAttributes, nestablePseudo);

    ast.traverseByType('ruleset', function (ruleset) {
      ruleset.forEach(function (selector) {

        var previousVal;
        selector.forEach(function (item) {
          if (previousVal) {
            if (helpers.isNestable(item.type, previousVal.type, elements, nestableElements)) {
              helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': selector.start.line,
                'column': selector.start.column,
                'message': formatOutput(item.type) + ' should be nested within its parent ' + formatOutput(previousVal.type),
                'severity': parser.severity
              });
            }
          }
          if (!item.is('space')) {
            previousVal = item;
          }
        });
      });
    });

    return result;
  }
};
