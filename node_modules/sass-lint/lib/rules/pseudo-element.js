'use strict';

var helpers = require('../helpers'),
    yaml = require('js-yaml'),
    fs = require('fs'),
    path = require('path');

var pseudoElements = yaml.safeLoad(
      fs.readFileSync(path.join(__dirname, '../../data', 'pseudoElements.yml'), 'utf8')
    ).split(' '),
    pseudoClasses = yaml.safeLoad(
      fs.readFileSync(path.join(__dirname, '../../data', 'pseudoClasses.yml'), 'utf8')
    ).split(' ');

/**
 * Check if the given argument is a prefixed string. If it is we return an unprefixed
 * version, else return it unmodified
 *
 * @param {Object|string} name - The value to test
 * @returns {string} A prefix free version of the string
 */
var prefixFree = function prefixFree (name) {
  return typeof name === 'string' && name.charAt(0) === '-' ? helpers.stripPrefix(name) : name;
};

/**
 * Determine if the given string matches a pseudo-element
 *
 * @param {string} name - The name to check
 * @returns {Boolean} Whether or not name is pseudo-element
 */
var isPseudoElement = function isPseudoElement (name) {
  return pseudoElements.indexOf(prefixFree(name)) !== -1;
};

/**
 * Determine if the given string matches a pseudo-class
 *
 * @param {string} name - The name to check
 * @returns {Boolean} Whether or not name is pseudo-class
 */
var isPseudoClass = function isPseudoClass (name) {
  return pseudoClasses.indexOf(prefixFree(name)) !== -1;
};

module.exports = {
  'name': 'pseudo-element',
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('pseudoClass', function (node) {
      if (isPseudoElement(node.content[0].content)) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': node.start.line,
          'column': node.start.column,
          'message': 'Pseudo-elements must start with double colons',
          'severity': parser.severity
        });
      }
    });

    ast.traverseByType('pseudoElement', function (node) {
      if (isPseudoClass(node.content[0].content)) {
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': node.start.line,
          'column': node.start.column,
          'message': 'Pseudo-classes must start with a single colon',
          'severity': parser.severity
        });
      }
    });

    return result;
  }
};
