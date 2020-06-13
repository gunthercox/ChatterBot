'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'class-name-format',
  'defaults': {
    'allow-leading-underscore': true,
    'convention': 'hyphenatedlowercase',
    'convention-explanation': false,
    'ignore': []
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('ruleset', function (ruleset) {
      var selectorAndExtensions = helpers.collectSuffixExtensions(ruleset, 'class');

      selectorAndExtensions.forEach(function (node) {
        var name = node.content,
            strippedName,
            violationMessage = false;

        if (parser.options.ignore.indexOf(name) !== -1) {
          return;
        }

        strippedName = name;

        if (parser.options['allow-leading-underscore'] && name[0] === '_') {
          strippedName = name.slice(1);
        }

        switch (parser.options.convention) {
        case 'hyphenatedlowercase':
          if (!helpers.isHyphenatedLowercase(strippedName)) {
            violationMessage = 'Class \'.' + name + '\' should be written in lowercase with hyphens';
          }
          break;
        case 'camelcase':
          if (!helpers.isCamelCase(strippedName)) {
            violationMessage = 'Class \'.' + name + '\' should be written in camelCase';
          }
          break;
        case 'pascalcase':
          if (!helpers.isPascalCase(strippedName)) {
            violationMessage = 'Class \'.' + name + '\' should be written in PascalCase';
          }
          break;
        case 'snakecase':
          if (!helpers.isSnakeCase(strippedName)) {
            violationMessage = 'Class \'.' + name + '\' should be written in snake_case';
          }
          break;
        case 'strictbem':
          if (!helpers.isStrictBEM(strippedName)) {
            violationMessage = 'Class \'.' + name + '\' should be written in BEM (Block Element Modifier) format';
          }
          break;
        case 'hyphenatedbem':
          if (!helpers.isHyphenatedBEM(strippedName)) {
            violationMessage = 'Class \'.' + name + '\' should be written in hyphenated BEM (Block Element Modifier) format';
          }
          break;
        default:
          if (!(new RegExp(parser.options.convention).test(strippedName))) {
            violationMessage = 'Class \'.' + name + '\' should match regular expression /' + parser.options.convention + '/';

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
      });
    });

    return result;
  }
};
