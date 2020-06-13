'use strict';

var helpers = require('../helpers'),
    yaml = require('js-yaml'),
    fs = require('fs'),
    path = require('path');

var colorFunctions = ['rgb', 'rgba', 'hsl', 'hsla'],
    cssColors = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../data', 'literals.yml'), 'utf8')).split(' ');

/**
 * Returns a copy of the colour functions array
 *
 * @param {Array} colorFunctionsArr - The color functions array we wish to clone
 * @returns {Array} A copy of the color functions array.
 */
var getColorFunctionsCopy = function (colorFunctionsArr) {
  return colorFunctionsArr.slice();
};

/**
 * Checks if the next node along is an operator of type ':'
 *
 * @param {Object} parent - The parent node
 * @param {number} i - The current child position in the parent node
 * @returns {boolean} If the sibling node is the correct type of operator
 */
var checkNextIsOperator = function (parent, i) {
  var next = parent.content[i + 1] && parent.content[i + 1].type === 'operator' && parent.content[i + 1].content === ':';
  var spacedNext = parent.content[i + 2] && parent.content[i + 2].type === 'operator' && parent.content[i + 2].content === ':';

  return next || spacedNext;
};

/**
 * Check nested function arguments for colors/idents or further nested functions
 *
 * @param {Object} node - The node we're checking
 * @returns {boolean} Whether the node matches the specified types
 */
var checkForNestedFuncArgs = function (node) {
  return node.type === 'color' || node.type === 'ident' || node.type === 'function';
};

/**
 * Check if the value is a color literal
 *
 * @param {Object} node - The node we're checking
 * @param {Array} validColorFunctions - The array of valid color function types to check against
 * @returns {boolean} Whether the node matches the specified types
 */
var checkIsLiteral = function (node, validColorFunctions) {
  return cssColors.indexOf(node.content) !== -1 || helpers.isValidHex(node.content) || validColorFunctions.indexOf(node.content) !== -1;
};

/**
 * Checks the see if the node type is a hex value if so return the correct prefix
 *
 * @param {String} nodeType - The node type identifier
 * @returns {String} Either a '#' or an empty string
 */
var checkHexPrefix = function (nodeType) {
  return nodeType === 'color' ? '#' : '';
};

module.exports = {
  'name': 'no-color-literals',
  'defaults': {
    'allow-map-identifiers': true,
    'allow-rgba': false,
    'allow-variable-identifiers': true
  },
  'detect': function (ast, parser) {
    var result = [],
        validColorFunctions = getColorFunctionsCopy(colorFunctions);

    if (parser.options['allow-rgba'] && validColorFunctions.indexOf('rgba') !== -1) {
      validColorFunctions.splice(validColorFunctions.indexOf('rgba'), 1);
    }

    ast.traverseByTypes(['value', 'variable'], function (node, i, parent) {

      // If we don't allow literals as variable names then check each variable name
      if (node.is('variable') && !parser.options['allow-variable-identifiers']) {
        if (cssColors.indexOf(node.content[0].content) !== -1) {
          result = helpers.addUnique(result, {
            'ruleId': parser.rule.name,
            'line': node.start.line,
            'column': node.start.column,
            'message': 'Color literals should not be used as variable names',
            'severity': parser.severity
          });
        }
      }
      // check the value nodes
      else if (node.is('value')) {
        node.forEach(function (valElem) {
          var declarationType = parent.content[0].content[0].type;
          // check type is color, content isn't a css color literal
          if (valElem.type === 'color' || cssColors.indexOf(valElem.content) !== -1) {
            if (declarationType === 'ident') {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': valElem.start.line,
                'column': valElem.start.column,
                'message': 'Color literals such as \'' + checkHexPrefix(valElem.type) + valElem.content + '\' should only be used in variable declarations',
                'severity': parser.severity
              });
            }
          }

          // if not a color value or a variable then check if it's a function
          else if (valElem.type === 'function') {
            var funcType = valElem.content[0].content;

            // check it's not a blacklisted color function and even if it is that it's not assigned to a variable
            if (validColorFunctions.indexOf(funcType) !== -1 && declarationType !== 'variable') {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': valElem.start.line,
                'column': valElem.start.column,
                'message': 'Color functions such as \'' + funcType + '\' should only be used in variable declarations',
                'severity': parser.severity
              });
            }

            // if rgba usage is allowed we need to make sure only variables are being passed to it.
            else if (
              parser.options['allow-rgba'] &&
              funcType === 'rgba' && (
                valElem.content[1].content[0].type !== 'variable' &&
                valElem.content[1].content[0].type !== 'function' &&
                valElem.content[1].content[0].type !== 'customProperty'
              ) &&
              declarationType !== 'variable'
            ) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': valElem.start.line,
                'column': valElem.start.column,
                'message': 'Only variables or functions must be passed to rgba, literals are restricted',
                'severity': parser.severity
              });
            }

            // if a non color function we should check its arguments
            else {
              valElem.content.forEach( function (funcContent) {
                if (funcContent.type === 'arguments') {
                  funcContent.forEach(function (funcArgs) {
                    // if the arguments are not functions themselves
                    if (funcArgs.type !== 'function') {
                      // check if the argument types are therefore color literals
                      if ((funcArgs.type === 'color' || funcArgs.type === 'ident') && (cssColors.indexOf(funcArgs.content) !== -1 || helpers.isValidHex(funcArgs.content))) {
                        result = helpers.addUnique(result, {
                          'ruleId': parser.rule.name,
                          'line': funcArgs.start.line,
                          'column': funcArgs.start.column,
                          'message': 'Color literals such as \'' + checkHexPrefix(funcArgs.type) + funcArgs.content + '\' should not be passed to functions, use variables',
                          'severity': parser.severity
                        });
                      }
                    }

                    // if the argument is a function itself
                    else {
                      // loop its arguments
                      funcArgs.forEach( function (nestedFuncArgs) {
                        // check again for color literals or blacklisted color functions
                        if (
                          checkForNestedFuncArgs(nestedFuncArgs) &&
                          checkIsLiteral(nestedFuncArgs, validColorFunctions)
                        ) {
                          result = helpers.addUnique(result, {
                            'ruleId': parser.rule.name,
                            'line': nestedFuncArgs.start.line,
                            'column': nestedFuncArgs.start.column,
                            'message': 'Color functions such as \'' + nestedFuncArgs.content + '\' should not be passed to functions, use variables',
                            'severity': parser.severity
                          });
                        }
                      });
                    }
                  });
                }
              });
            }
          }

          // if not allowing literals as map identifiers check to see if the property names
          // are the same as color literals - this is bad
          else if (valElem.type === 'parentheses' && !parser.options['allow-map-identifiers']) {
            valElem.traverse(function (mapVals, idx, mapValsParent) {
              // check if the parent is a variable to allow variables named after CSS colors, e.g. `$black`
              if (
                mapVals.type === 'ident' &&
                checkNextIsOperator(mapValsParent, idx) &&
                cssColors.indexOf(mapVals.content) !== -1
              ) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': mapVals.start.line,
                  'column': mapVals.start.column,
                  'message': 'Color literals should not be used as map identifiers',
                  'severity': parser.severity
                });
              }
            });
          }
        });
      }
    });
    return result;
  }
};
