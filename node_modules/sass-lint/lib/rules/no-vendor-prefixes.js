'use strict';

var helpers = require('../helpers'),
    yaml = require('js-yaml'),
    fs = require('fs'),
    path = require('path');

var properties = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../data', 'properties.yml'), 'utf8')).split(' '),
    prefixes = ['webkit', 'moz', 'ms'];

/**
 * Returns a copy of the prefixes array so that it can be safely modified
 *
 * @param {Array} prefixArr - The array of prefixes
 * @returns {Array} A copy of the prefixes array
 */
var getPrefixCopy = function (prefixArr) {
  return prefixArr.slice();
};

/**
 * Removes specified vendor prefixes from the prefixes array
 *
 * @param {Array} prefixArr - The array of prefixes
 * @param {Array} excludes - An array of prefixes to exclude
 * @returns {Array} The prefixes array minus any excluded prefixes
 */
var handleExcludes = function (prefixArr, excludes) {
  excludes.forEach(function (item) {
    var index = prefixArr.indexOf(item);

    if (index > -1) {
      prefixArr.splice(index, 1);
    }
  });

  return prefixArr;
};

/**
 * Adds specified vendor prefixes to the prefixes array
 *
 * @param {Array} prefixArr - The array of prefixes
 * @param {Array} includes - An array of prefixes to include
 * @returns {Array} The prefixes array plus any extra included prefixes
 */
var handleIncludes = function (prefixArr, includes) {
  includes.forEach(function (item) {
    if (prefixArr.indexOf(item) === -1) {
      prefixArr.push(item);
    }
  });

  return prefixArr;
};

/**
 * Creates and returns a regex pattern based on all the included prefixes so that
 * we can test our values against it.
 *
 * @param {Array} prefixArr - The array of prefixes
 * @param {Array} includes - An array of prefixes to include
 * @param {Array} excludes - An array of prefixes to exclude
 * @returns {RegExp} The regex pattern for us to test values against
 */
var precompileRegEx = function (prefixArr, includes, excludes) {
  if (includes.length) {
    prefixArr = handleIncludes(prefixArr, includes);
  }

  if (excludes.length) {
    prefixArr = handleExcludes(prefixArr, excludes);
  }

  return new RegExp('-(' + prefixArr.join('|') + ')-');
};

/**
 * Checks to see if the property is a standard property or a browser specific one
 *
 * @param {string} property - The property string we want to test
 * @returns {boolean} Whether the property is standard or not
 */
var isStandardProperty = function (property) {
  return properties.indexOf(helpers.stripPrefix(property)) !== -1;
};

module.exports = {
  'name': 'no-vendor-prefixes',
  'defaults': {
    'additional-identifiers': [],
    'excluded-identifiers': [],
    'ignore-non-standard': false
  },
  'detect': function (ast, parser) {

    var result = [],
        validPrefixes = getPrefixCopy(prefixes),
        statement = precompileRegEx(validPrefixes, parser.options['additional-identifiers'], parser.options['excluded-identifiers']);

    ast.traverseByType('ident', function (value) {
      if (statement.test(value.content)) {
        if (!isStandardProperty(value.content) && parser.options['ignore-non-standard']) {
          return;
        }
        result = helpers.addUnique(result, {
          'ruleId': parser.rule.name,
          'line': value.start.line,
          'column': value.start.column,
          'message': 'Vendor prefixes should not be used',
          'severity': parser.severity
        });
      }
    });
    return result;
  }
};
