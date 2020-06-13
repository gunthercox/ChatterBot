'use strict';

var helpers = require('../helpers');

var isVarRegex = /^[\$]/;

module.exports = {
  'name': 'url-quotes',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('uri', function (node) {
      node.traverse(function (item) {
        if (item.is('raw')) {
          if (!item.content.match(isVarRegex)) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'severity': parser.severity,
              'line': item.start.line,
              'column': item.start.column,
              'message': 'Quotes around URLs are required'
            });
          }
        }
      });
    });

    return result;
  }
};
