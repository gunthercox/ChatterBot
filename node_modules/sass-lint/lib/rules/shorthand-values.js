'use strict';

var helpers = require('../helpers');

var shortVals = [
  'border-color',
  'border-radius',
  'border-style',
  'border-width',
  'margin',
  'padding'
];

/**
 * Checks to see if a series of values can be condensed down to a singular value
 *
 * @param {array} value - The array of values to check
 * @param {array} allowed - The parser options to specify the levels allowed to condense to
 * @returns {boolean} Whether the values can be condensed to a singular value
 */
var condenseToOne = function (value, allowed) {
  if (allowed.indexOf(1) !== -1 && value.length > 1) {
    for (var i = 1; i < value.length; i++) {
      if (value[i] !== value[0]) {
        return false;
      }
    }
    return true;
  }
  return false;
};

/**
 * Checks to see if a series of values can be condensed down to two values
 *
 * @param {array} value - The array of values to check
 * @param {array} allowed - The parser options to specify the levels allowed to condense to
 * @returns {boolean} Whether the values can be condensed to two values
 */
var condenseToTwo = function (value, allowed) {
  if (allowed.indexOf(2) !== -1 && value.length > 2) {
    if ((value[0] === value[2] && value[1] === value[3]) || (value[0] === value[2] && !value[3] && value[0] !== value[1])) {
      return true;
    }
  }
  return false;
};

/**
 * Checks to see if a series of values can be condensed down to three values
 *
 * @param {array} value - The array of values to check
 * @param {array} allowed - The parser options to specify the levels allowed to condense to
 * @returns {boolean} Whether the values can be condensed to three values
 */
var condenseToThree = function (value, allowed) {
  if (allowed.indexOf(3) !== -1 && value.length > 3) {
    if (value[1] === value[3] ) {
      return true;
    }
  }
  return false;
};

/**
 * Used to scan property values and create a string representation of the values to display
 *
 * @param {Object} node - The current node
 * @returns {string} A string reconstruction of the current properties value
 */
var scanValue = function (node) {
  var curValue = [];
  var fullVal = '';
  node.forEach(function (val) {
    // add to our value string depending on node type
    if (val.is('dimension')) {
      val.forEach(function (el) {
        fullVal += el.content;
      });
    }

    else if (val.is('percentage')) {
      val.forEach(function (el) {
        fullVal += el.content + '%';
      });
    }

    else if (val.is('interpolation')) {
      fullVal += '#{' + scanValue(val.content) + '}';
    }

    else if (val.is('color')) {
      fullVal += '#' + val.content + '';
    }

    else if (
      val.is('operator') ||
      val.is('ident') ||
      val.is('number') ||
      val.is('unaryOperator') ||
      val.is('string')
    ) {
      fullVal += val.content;
    }

    else if (val.is('variable')) {
      val.forEach(function (el) {
        fullVal += '$' + el.content;
      });
    }

    else if (val.is('function')) {

      var func = val.first('ident'),
          args = '';

      val.forEach('arguments', function (arg) {
        args = scanValue(arg).join(' ');
      });

      fullVal = func + '(' + args + ')';
    }

    else if (val.is('parentheses')) {
      fullVal += '(' + scanValue(val).join(' ') + ')';
    }

    else if (val.is('space')) {
      // This is a non value character such as a space
      // We want to start another value here
      curValue.push(fullVal);

      // reset the value string for the next iteration
      fullVal = '';
    }
  });

  if (fullVal !== '') {
    // The last dimension in a value will not be followed by a character so we push here
    curValue.push(fullVal);
  }
  return curValue;
};

module.exports = {
  'name': 'shorthand-values',
  'defaults': {
    'allowed-shorthands': [1, 2, 3]
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('declaration', function (declaration) {
      var isShorthandProperty = false,
          property;

      declaration.traverse(function (item) {

        if (item.is('property')) {
          item.traverse(function (child) {
            // check if the property is a possible shorthand property
            if (shortVals.indexOf(child.content) !== -1) {
              isShorthandProperty = true;

              // store a reference to the property for our error
              property = shortVals[shortVals.indexOf(child.content)];
            }
          });
        }

        if (isShorthandProperty) {
          var value = [];

          if (item.is('value')) {
            var node = item.content;

            // Build each value into an array of strings with value and type
            value = scanValue(node);

            if (value.length <= 4 && value.length >= 1) {
              var output = [];

              // check which values can condense
              if (condenseToOne(value, parser.options['allowed-shorthands'])) {
                output = [value[0]];
              }
              else if (condenseToTwo(value, parser.options['allowed-shorthands'])) {
                output = [value[0], value[1]];
              }
              else if (condenseToThree(value, parser.options['allowed-shorthands'])) {
                output = [value[0], value[1], value[2]];
              }

              if (output.length) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': item.start.line,
                  'column': item.start.column,
                  'message': 'Property `' + property + '` should be written more concisely as `' + output.join(' ') + '` instead of `' + value.join(' ') + '`',
                  'severity': parser.severity
                });
              }
            }
          }
        }
      });
    });
    return result;
  }
};
