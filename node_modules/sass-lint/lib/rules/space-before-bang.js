'use strict';

var helpers = require('../helpers.js');

module.exports = {
  'name': 'space-before-bang',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByTypes(['important', 'default', 'value'], function (block, i, parent) {
      var previous = parent.content[i - 1];
      if (block.is('value') && block.contains('important')) {
        if (block.content.length === 1 && block.first('important')) {
          if (previous) {
            if (!previous.is('space')) {
              if (parser.options.include) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': block.first('important').start.line,
                  'column': block.first('important').start.column,
                  'message': 'Whitespace required before !important',
                  'severity': parser.severity
                });
              }
            }
            else {
              if (!parser.options.include) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': block.first('important').start.line,
                  'column': block.first('important').start.column,
                  'message': 'Whitespace not allowed before !important',
                  'severity': parser.severity
                });
              }
            }
          }
        }
      }
      else
      if (block.is('important') || block.is('default')) {
        var blockString = block.is('important') ? '!important' : '!default';
        if (previous) {
          if (!previous.is('space')) {
            if (parser.options.include) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': block.start.line,
                'column': block.start.column,
                'message': 'Whitespace required before ' + blockString,
                'severity': parser.severity
              });
            }
          }
          else {
            if (!parser.options.include) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': previous.start.line,
                'column': previous.start.column,
                'message': 'Whitespace not allowed before ' + blockString,
                'severity': parser.severity
              });
            }
          }
        }
      }
      return false;
    });

    return result;
  }
};
