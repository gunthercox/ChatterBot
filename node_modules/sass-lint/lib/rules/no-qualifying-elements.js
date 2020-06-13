'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'no-qualifying-elements',
  'defaults': {
    'allow-element-with-attribute': false,
    'allow-element-with-class': false,
    'allow-element-with-id': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('selector', function (selector) {
      selector.forEach(function (item, i) {
        if (item.is('attributeSelector') || item.is('class') || item.is('id')) {
          var previous = selector.content[i - 1] || false;

          if (previous && previous.is('typeSelector')) {
            if (previous.contains('ident')) {
              var type = null;

              if (item.is('attributeSelector')) {
                type = 'attribute';
              }

              if (item.is('class')) {
                type = 'class';
              }

              if (item.is('id')) {
                type = 'id';
              }

              if (type && !parser.options['allow-element-with-' + type]) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': item.start.line,
                  'column': item.start.column,
                  'message': 'Qualifying elements are not allowed for ' + type + ' selectors',
                  'severity': parser.severity
                });
              }
            }
          }
        }
      });
    });

    return result;
  }
};
