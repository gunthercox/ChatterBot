// Note that this file is nearly identical to function-name-format.js, mixin-name-format.js, and placeholder-name-format.js
'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'variable-name-format',
  'defaults': {
    'allow-leading-underscore': true,
    'convention': 'hyphenatedlowercase',
    'convention-explanation': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('variable', function (variable) {
      var strippedName,
          violationMessage = false,
          name = variable.first().content;


      strippedName = name;

      if (parser.options['allow-leading-underscore'] && name[0] === '_') {
        strippedName = strippedName.slice(1);
      }

      switch (parser.options.convention) {
      case 'hyphenatedlowercase':
        if (!helpers.isHyphenatedLowercase(strippedName)) {
          violationMessage = 'Variable \'' + name + '\' should be written in lowercase with hyphens';
        }
        break;
      case 'camelcase':
        if (!helpers.isCamelCase(strippedName)) {
          violationMessage = 'Variable \'' + name + '\' should be written in camelCase';
        }
        break;
      case 'pascalcase':
        if (!helpers.isPascalCase(strippedName)) {
          violationMessage = 'Variable \'' + name + '\' should be written in PascalCase';
        }
        break;
      case 'snakecase':
        if (!helpers.isSnakeCase(strippedName)) {
          violationMessage = 'Variable \'' + name + '\' should be written in snake_case';
        }
        break;
      case 'strictbem':
        if (!helpers.isStrictBEM(strippedName)) {
          violationMessage = 'Variable \'' + name + '\' should be written in BEM (Block Element Modifier) format';
        }
        break;
      case 'hyphenatedbem':
        if (!helpers.isHyphenatedBEM(strippedName)) {
          violationMessage = 'Variable \'' + name + '\' should be written in hyphenated BEM (Block Element Modifier) format';
        }
        break;
      default:
        if (!(new RegExp(parser.options.convention).test(strippedName))) {
          violationMessage = 'Variable \'' + name + '\' should match regular expression /' + parser.options.convention + '/';

          // convention-message overrides violationMessage
          if (parser.options['convention-explanation']) {
            violationMessage = parser.options['convention-explanation'];
          }
        }
      }

      if (violationMessage) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': variable.start.line,
          'column': variable.start.column,
          'message': violationMessage,
          'severity': parser.severity
        });
      }
    });

    return result;
  }
};
