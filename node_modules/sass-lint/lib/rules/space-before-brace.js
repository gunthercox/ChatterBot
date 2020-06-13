'use strict';

var helpers = require('../helpers');

var getLastWhitespace = function (node) {
  if (node === false) {
    return null;
  }

  if (!node) {
    return false;
  }
  if (node.is('space')) {
    return node;
  }

  return getLastWhitespace(node.last());
};

module.exports = {
  'name': 'space-before-brace',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [];
    if (ast.syntax === 'scss') {
      ast.traverseByTypes(['block', 'atrulers', 'declaration'], function (block, i, parent) {
        var previous = false,
            whitespace,
            warn = {};

        if ((block.is('block') || block.is('atrulers')) && !parent.is('value')) {
          previous = parent.get(i - 1);
        }
        else if (block.is('declaration')) {
          if (block.contains('value')) {
            for (var j = 0; j < block.content.length; j++) {
              if (block.content[j].is('value') && block.content[j].content[0].is('block')) {
                previous = block.content[j - 1];
                warn.line = block.content[j].content[0].start.line;
                warn.col = block.content[j].content[0].start.column;
              }
            }
          }
        }
        whitespace = getLastWhitespace(previous);
        if (whitespace === false) {
          if (parser.options.include) {
            if (!warn.hasOwnProperty('line')) {
              warn.line = block.start.line;
              warn.col = block.start.column;
            }
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': warn.line,
              'column': warn.col - 1,
              'message': 'Whitespace required before {',
              'severity': parser.severity
            });
          }
        }
        else {
          if (!parser.options.include && whitespace !== null) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': whitespace.start.line,
              'column': whitespace.start.column,
              'message': 'Whitespace not allowed before {',
              'severity': parser.severity
            });
          }
        }
      });
    }
    return result;
  }
};
