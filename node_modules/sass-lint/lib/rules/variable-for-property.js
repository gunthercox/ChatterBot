'use strict';

var helpers = require('../helpers');

// The whitelisted ident values
var whitelistedValues = ['inherit', 'initial', 'transparent', 'none', 'currentColor'],
    ignoredValueTypes = ['important', 'space'];

/**
 * Checks If the property is of a valid type, either its a variable or it's a whitelisted ident value
 *
 * @param {Object} propertyElem - The property element
 * @returns {boolean} Whether the property is valid or not
 */
var isValidProperty = function (propertyElem) {
  if (propertyElem) {
    if (propertyElem.is('variable')) {
      return true;
    }
    else if (propertyElem.is('ident') && whitelistedValues.indexOf(propertyElem.content) !== -1) {
      return true;
    }
  }
  return false;
};

/**
 * Checks If the property type is an ignored value type
 *
 * @param {Object} propertyElem - The property element
 * @returns {boolean} Whether the property is an ignored type or not
 */
var isIgnoredType = function (propertyElem) {
  if (propertyElem) {
    return ignoredValueTypes.indexOf(propertyElem.type) !== -1;
  }
  return false;
};

/**
 * Checks If the property type is a function and whether it is allowed
 *
 * @param {Object} propertyElem - The property element
 * @param {boolean} allowMap - Whether the user has specified to allow Sass function map-get
 * @param {Array} functionWhitelist - An array of string - function names we wish to allow
 * @returns {boolean} Whether the property is an ignored type or not
 */
var isIgnoredFunction = function (propertyElem, allowMap, functionWhitelist) {
  if (propertyElem && propertyElem.is('function')) {
    var funcIdent = propertyElem.first('ident');

    // allow custom properties as values
    if (funcIdent.content === 'var') {
      return true;
    }

    if (allowMap && funcIdent.content === 'map-get') {
      return true;
    }

    if (functionWhitelist.length) {
      return functionWhitelist.indexOf(funcIdent.content) !== -1;
    }
  }
  return false;
};


module.exports = {
  'name': 'variable-for-property',
  'defaults': {
    'properties': [],
    'allow-map-get': true,
    'allowed-functions': []
  },
  'detect': function (ast, parser) {
    var result = [];

    if (parser.options.properties.length) {
      ast.traverseByType('value', function (node, i, parent) {
        var declaration = parent.content[0].content[0],
            declarationType = declaration.type,
            declarationIdent = declaration.content;

        if (declarationType === 'ident') {
          if (parser.options.properties.indexOf(declarationIdent) !== -1) {
            node.forEach(function (valElem) {

              if (valElem.is('function') && !isIgnoredFunction(valElem, parser.options['allow-map-get'], parser.options['allowed-functions'])) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': declaration.start.line,
                  'column': declaration.start.column,
                  'message': 'The function passed to \'' + declarationIdent + '\' is not allowed',
                  'severity': parser.severity
                });
              }
              else if (
                !valElem.is('function') &&
                !isValidProperty(valElem) &&
                !isIgnoredType(valElem) &&
                !valElem.is('interpolation')
              ) {
                result = helpers.addUnique(result, {
                  'ruleId': parser.rule.name,
                  'line': declaration.start.line,
                  'column': declaration.start.column,
                  'message': 'Values for properties of type \'' + declarationIdent + '\' may only be variables',
                  'severity': parser.severity
                });
              }
            });
          }
        }
      });
    }
    return result;
  }
};
