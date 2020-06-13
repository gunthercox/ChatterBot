'use strict';

var helpers = require('../helpers');

var operators = ['+', '-', '/', '*', '%', '<', '>', '==', '!=', '<=', '>='];

/**
 * Determine a relational operator based on the operator node
 *
 * @param {Object} node - The operator node
 * @returns {string} Returns a relational operator
 */
var getRelationalOperator = function (node) {
  if (node.content === '<') {
    return '<=';
  }

  if (node.content === '>') {
    return '>=';
  }
  return false;
};

/**
 * Determine if operator is negative number
 *
 * @param {string} operator - The operator
 * @param {Object} next - The next node
 * @param {Object} previous - The previous node
 * @param {Object} doublePrevious - The double previous node (back two)
 * @returns {bool} true / false
 */
var isNegativeNumber = function (operator, next, previous, doublePrevious) {
  if (operator === '-') {

    // Catch the following:
    // $foo: -20;
    // $foo: -#{$foo}
    // $foo: -($foo * 2)
    // $foo: -$foo
    if (next) {
      if (!previous || (previous.is('space') && doublePrevious && !doublePrevious.is('number'))) {
        if (
          next.is('number') ||
          next.is('interpolation') ||
          next.is('variable') ||
          next.is('parentheses')
        ) {
          return true;
        }
      }
    }

    // Catch the following:
    // .foo {
    //   property: -16px;
    // }
    if (next && (next.is('dimension') || next.is('percentage'))) {
      return true;
    }

    // Catch the following:
    // .foo {
    //   propery: 2 / -16;
    // }
    if (doublePrevious && doublePrevious.is('operator')) {
      return true;
    }

    // Catch the following:
    // .foo {
    //   property: 2 /-16px;
    // }
    if (previous && previous.is('operator')) {
      return true;
    }
  }

  return false;
};

/**
 * Determine if operator is divider
 *
 * @param {string} operator - The operator
 * @param {Object} next - The next node
 * @param {Object} previous - The previous node
 * @returns {bool} true / false
 */
var isDivider = function (operator, next, previous) {
  if (operator === '/') {

    // Catch the following:
    // .foo {
    //   property: calc(100% / 2);
    // }
    if (previous && next) {
      if (previous.is('dimension') && (next.is('dimension') || next.is('number'))) {
        return true;
      }
    }
  }

  return false;
};

/**
 * Determine if operator is part of unicode
 *
 * @param {string} operator - The operator
 * @param {Object} previous - The previous node
 * @returns {bool} true / false
 */
var isUnicode = function (operator, previous) {
  if (operator === '+') {

    // Catch the following:
    // @font-face {
    //   unicode-range: U+26;
    // }
    if (previous && previous.is('ident') && previous.content === 'U') {
      return true;
    }
  }

  return false;
};

/**
 * Determine if operator is part of import path
 *
 * @param {string} operator - The operator
 * @param {Object} parent - The parent node
 * @returns {bool} true / false
 */
var isImport = function (operator, parent) {
  if (operator === '/') {

    if (parent && parent.is('atrule') && parent.contains('atkeyword')) {
      var keyword = parent.first('atkeyword');

      if (keyword.contains('ident')) {
        var ident = keyword.first('ident');

        if (ident.content === 'import') {
          return true;
        }
      }
    }
  }

  return false;
};

/**
 * Determine if operator is part an ident
 *
 * @param {string} operator - The operator
 * @param {Object} next - The next node
 * @param {Object} previous - The previous node
 * @returns {bool} true / false
 */
var isPartialIdent = function (operator, next, previous) {
  if (operator === '-') {
    return next && previous && previous.is('interpolation');
  }
  return false;
};

/**
 * Determine if operator is exception
 *
 * @param {string} operator - The operator
 * @param {Object} parent - The parent node
 * @param {Object} i - The node index
 * @returns {bool} true / false
 */
var isException = function (operator, parent, i) {
  var previous = parent.content[i - 1] || false,
      doublePrevious = parent.content[i - 2] || false,
      next = parent.content[i + 1] || false;

  if (isNegativeNumber(operator, next, previous, doublePrevious)) {
    return true;
  }

  if (isDivider(operator, next, previous)) {
    return true;
  }

  if (isUnicode(operator, previous)) {
    return true;
  }

  if (isImport(operator, parent)) {
    return true;
  }

  if (isPartialIdent(operator, next, previous)) {
    return true;
  }

  return false;
};

/**
 * Check the spacing around an operator
 *
 * @param {Object} node - The node to check the spacing around
 * @param {int} i - The node's child index of it's parent
 * @param {Object} parent - The parent node
 * @param {Object} parser - The parser object
 * @param {Object} result - The result object
 * @returns {bool|null} false if exception
 */
var checkSpacing = function (node, i, parent, parser, result) {
  if (node.is('operator') || node.is('unaryOperator')) {
    var previous = parent.content[i - 1] || false,
        next = parent.content[i + 1] || false,
        operator = node.content;

    //////////////////////////
    // Multi-part operators
    //////////////////////////

    // If second part of relational operator move on
    if (node.content === '=' && previous) {
      if (previous.content === '<' || previous.content === '>') {
        return false;
      }
    }

    // If first part of relational operator, carry on and build it
    if ((node.content === '<' || node.content === '>') && next) {
      if (next.content === '=') {
        operator = getRelationalOperator(node);
        next = parent.content[i + 2] || false;
      }
    }

    //////////////////////////
    // Exceptions
    //////////////////////////

    if (isException(operator, parent, i)) {
      return false;
    }

    // If the operator checks out in our valid operator list
    if (operators.indexOf(operator) !== -1) {

      if (parser.options.include) {
        if (
          (previous && !previous.is('space'))
          || (next && !next.is('space'))
        ) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': node.start.line,
            'column': node.start.column,
            'message': 'Space expected around operator',
            'severity': parser.severity
          });
        }
        else {
          if (
              (previous && (previous.end.line >= previous.start.line) && (previous.end.column > previous.start.column))
              || (next && (next.end.line >= next.start.line) && (next.end.column > next.start.column))
            ) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': node.start.line,
              'column': node.start.column,
              'message': 'Multiple spaces not allowed around operator',
              'severity': parser.severity
            });
          }
        }
      }
      else {
        if (
          (previous && previous.is('space'))
          || (next && next.is('space'))
        ) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': node.start.line,
            'column': node.start.column,
            'message': 'No spaces allowed around operator',
            'severity': parser.severity
          });
        }
      }
    }
  }
  return result;
};

module.exports = {
  'name': 'space-around-operator',
  'defaults': {
    'include': true
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByTypes(['condition', 'atrule', 'value'], function (node) {
      node.forEach(function (item, i, parent) {
        // Perform another loop of the children if we come across a parenthesis
        // parent node
        if (item.is('parentheses')) {
          item.forEach(function (child, j, childParent) {
            // Do the spacing checks
            checkSpacing(child, j, childParent, parser, result);
          });
        }
        else {
          // Do the spacing checks
          checkSpacing(item, i, parent, parser, result);
        }
      });
    });

    return result;
  }
};
