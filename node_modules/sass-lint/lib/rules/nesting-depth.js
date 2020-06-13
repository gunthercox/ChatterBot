'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'nesting-depth',
  'defaults': {
    'max-depth': 2
  },
  'detect': function (ast, parser) {
    var result = [],
        nodes = {},
        depth = 0;

    var recursiveSearch = function (node) {
      if (node.contains('block')) {
        node.forEach('block', function (block) {
          if (block.contains('ruleset')) {
            depth++;
            block.forEach('ruleset', function (ruleset) {
              var selector = ruleset.first('selector');

              if (depth > parser.options['max-depth']) {
                var nodeLineColumn = selector.start.line + ':' + selector.start.column;

                if (nodes[nodeLineColumn]) {
                  if (depth > nodes[nodeLineColumn].depth) {
                    nodes[nodeLineColumn].depth = depth;
                  }
                }
                else {
                  nodes[nodeLineColumn] = {
                    'line': selector.start.line,
                    'column': selector.start.column,
                    'depth': depth
                  };
                }
              }
              else {
                recursiveSearch(ruleset);
              }
            });
          }
        });
      }
      depth--;
    };

    ast.traverseByType('selector', function (selector, i, parent) {
      recursiveSearch(parent);
      depth = 0;
    });

    Object.keys(nodes).forEach(function (node) {
      node = nodes[node];
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': node.line,
        'column': node.column,
        'message': 'Nesting depth ' + node.depth + ' greater than max of ' + parser.options['max-depth'],
        'severity': parser.severity
      });
    });


    return result;
  }
};
