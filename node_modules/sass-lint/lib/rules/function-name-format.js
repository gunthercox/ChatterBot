// Note that this file is nearly identical to mixin-name-format.js, placeholder-name-format.js, and variable-name-format.js
'use strict';

var helpers = require('../helpers'),
    yaml = require('js-yaml'),
    fs = require('fs'),
    path = require('path');

var whitelist = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../data', 'functions.yml'), 'utf8')).split(' ');

module.exports = {
  'name': 'function-name-format',
  'defaults': {
    'allow-leading-underscore': true,
    'convention': 'hyphenatedlowercase',
    'convention-explanation': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('function', function (node) {
      var name = node.first('ident').content,
          strippedName,
          violationMessage = false;

      // ignore functions on whitelist - css3 transforms
      if (whitelist.indexOf(name) !== -1) {
        return;
      }

      strippedName = name;

      if (parser.options['allow-leading-underscore'] && name[0] === '_') {
        strippedName = name.slice(1);
      }

      switch (parser.options.convention) {
      case 'hyphenatedlowercase':
        if (!helpers.isHyphenatedLowercase(strippedName)) {
          violationMessage = 'Function \'' + name + '\' should be written in lowercase with hyphens';
        }
        break;
      case 'camelcase':
        if (!helpers.isCamelCase(strippedName)) {
          violationMessage = 'Function \'' + name + '\' should be written in camelCase';
        }
        break;
      case 'pascalcase':
        if (!helpers.isPascalCase(strippedName)) {
          violationMessage = 'Function \'' + name + '\' should be written in PascalCase';
        }
        break;
      case 'snakecase':
        if (!helpers.isSnakeCase(strippedName)) {
          violationMessage = 'Function \'' + name + '\' should be written in snake_case';
        }
        break;
      case 'strictbem':
        if (!helpers.isStrictBEM(strippedName)) {
          violationMessage = 'Function \'' + name + '\' should be written in BEM (Block Element Modifier) format';
        }
        break;
      case 'hyphenatedbem':
        if (!helpers.isHyphenatedBEM(strippedName)) {
          violationMessage = 'Function \'' + name + '\' should be written in hyphenated BEM (Block Element Modifier) format';
        }
        break;
      default:
        if (!(new RegExp(parser.options.convention).test(strippedName))) {
          violationMessage = 'Function \'' + name + '\' should match regular expression /' + parser.options.convention + '/';

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

    return result;
  }
};
