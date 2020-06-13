'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'trailing-semicolon',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [];

    var hasDoubleSemiColon = function (tree) {

      tree.traverseByType('declarationDelimiter', function (node, index, parent) {
        if (parent.content[index + 1] && parent.content[index + 1].is('declarationDelimiter')) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'severity': parser.severity,
            'line': parent.content[index + 1].start.line,
            'column': parent.content[index + 1].start.column,
            'message': 'No double semicolons allowed'
          });
        }
      });
    };

    if (ast.syntax !== 'sass') {
      ast.traverseByType('block', function (block) {
        var last,
            next;

        try {
          last = block.last('declaration');
        }
        catch (e) {
          return;
        }

        block.forEach('declaration', function (item, i, parent) {
          if (item.contains('value')) {
            var valueNode = item.last('value').content[0];

            if (!valueNode.is('block')) {
              if (helpers.isEqual(last, item)) {
                if (parent.content[i + 1]) {
                  next = parent.content[i + 1];

                  if (next.is('declarationDelimiter')) {
                    if (!parser.options.include) {
                      result = helpers.addUnique(result, {
                        'ruleId': parser.rule.name,
                        'severity': parser.severity,
                        'line': item.end.line,
                        'column': item.end.column,
                        'message': 'No trailing semicolons allowed'
                      });
                    }
                  }
                  else {
                    if (parser.options.include) {
                      result = helpers.addUnique(result, {
                        'ruleId': parser.rule.name,
                        'severity': parser.severity,
                        'line': item.last('value').start.line,
                        'column': item.last('value').start.column,
                        'message': 'Trailing semicolons required'
                      });
                    }
                  }
                }
              }
            }
          }
          hasDoubleSemiColon(parent);
        });
      });
    }

    return result;
  }
};
