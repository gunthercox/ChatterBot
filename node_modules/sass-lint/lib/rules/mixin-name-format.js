'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'mixin-name-format',
  'defaults': {
    'allow-leading-underscore': true,
    'convention': 'hyphenatedlowercase',
    'convention-explanation': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByTypes(['mixin', 'include'], function (node) {
      var name,
          strippedName,
          violationMessage = false;

      if (node.is('mixin')) {
        if (node.contains('ident')) {
          name = node.first('ident').content;
        }
      }
      else {
        // We're not linting extends here
        if (node.contains('atkeyword')) {
          if (node.first('atkeyword').contains('ident')) {
            if (node.first('atkeyword').first('ident').content === 'extend') {
              return false;
            }
          }
        }

        if (node.contains('ident')) {
          name = node.first('ident').content;
        }
      }

      if (name) {
        strippedName = name;

        if (parser.options['allow-leading-underscore'] && name[0] === '_') {
          strippedName = name.slice(1);
        }

        switch (parser.options.convention) {
        case 'hyphenatedlowercase':
          if (!helpers.isHyphenatedLowercase(strippedName)) {
            violationMessage = 'Mixin \'' + name + '\' should be written in lowercase with hyphens';
          }
          break;
        case 'camelcase':
          if (!helpers.isCamelCase(strippedName)) {
            violationMessage = 'Mixin \'' + name + '\' should be written in camelCase';
          }
          break;
        case 'pascalcase':
          if (!helpers.isPascalCase(strippedName)) {
            violationMessage = 'Mixin \'' + name + '\' should be written in PascalCase';
          }
          break;
        case 'snakecase':
          if (!helpers.isSnakeCase(strippedName)) {
            violationMessage = 'Mixin \'' + name + '\' should be written in snake_case';
          }
          break;
        case 'strictbem':
          if (!helpers.isStrictBEM(strippedName)) {
            violationMessage = 'Mixin \'' + name + '\' should be written in BEM (Block Element Modifier) format';
          }
          break;
        case 'hyphenatedbem':
          if (!helpers.isHyphenatedBEM(strippedName)) {
            violationMessage = 'Mixin \'' + name + '\' should be written in hyphenated BEM (Block Element Modifier) format';
          }
          break;
        default:
          if (!(new RegExp(parser.options.convention).test(strippedName))) {
            violationMessage = 'Mixin \'' + name + '\' should match regular expression /' + parser.options.convention + '/';

            // convention-message overrides violationMessage
            if (parser.options['convention-explanation']) {
              violationMessage = parser.options['convention-explanation'];
            }
          }
        }

        if (violationMessage) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': node.start.line,
            'column': node.start.column,
            'message': violationMessage,
            'severity': parser.severity
          });
        }
      }
      return true;
    });

    return result;
  }
};
