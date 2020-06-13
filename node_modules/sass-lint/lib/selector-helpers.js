'use strict';

// ==============================================================================
//  Helpers
// ==============================================================================

var simpleIdents = [
  'ident',
  'number',
  'operator',
  'combinator',
  'string',
  'parentSelector',
  'delimiter',
  'typeSelector',
  'attributeMatch'
];

var subSelectors = [
  'parentSelectorExtension',
  'attributeName',
  'attributeValue',
  'dimension',
  'selector',
  'function'
];

/**
 * Adds grammar around our content blocks to construct selectors with
 * more readable formats.
 *
 * @param {object} val - The current value node
 * @param {string} prefix - The grammar to prefix the value with
 * @param {string} suffix - The grammar to add after the value
 * @returns {string} The correct readable format
 */
var addGrammar = function (val, prefix, suffix) {
  return prefix + val.content + suffix;
};

/**
 * Adds grammar around our content blocks to construct selectors with
 * more readable formats and loops the content as they're within sub blocks.
 *
 * @param {object} val - The current value node
 * @param {string} prefix - The grammar to prefix the value with
 * @param {string} suffix - The grammar to add after the value
 * @param {function} constructSelector - The callback we wish to use which means constructSelector in this instance
 * @returns {string} The correct readable format
 */
var constructSubSelector = function (val, prefix, suffix, constructSelector) {
  var content = prefix;
  val.forEach(function (subItem) {
    content += constructSelector(subItem);
  });

  return content + suffix;
};

// ==============================================================================
//  Public Methods
// ==============================================================================

/**
 * Constructs a syntax complete selector for our selector matching and warning output
 *
 * @param {object} val - The current node / part of our selector
 * @returns {string} - Content: The current node with correct syntax e.g. class my-class = '.my-class'
 */
var constructSelector = function (val) {
  var content = null;

  if (val.is('arguments')) {
    content = constructSubSelector(val, '(', ')', constructSelector);
  }

  else if (val.is('atkeyword')) {
    content = constructSubSelector(val, '@', '', constructSelector);
  }

  else if (val.is('attributeSelector')) {
    content = constructSubSelector(val, '[', ']', constructSelector);
  }

  else if (val.is('class')) {
    content = addGrammar(val, '.', '');
  }

  else if (val.is('id')) {
    content = addGrammar(val, '#', '');
  }

  else if (val.is('interpolation')) {
    content = constructSubSelector(val, '#{', '}', constructSelector);
  }

  else if (val.is('nth')) {
    content = addGrammar(val, '(', ')');
  }

  else if (val.is('nthSelector')) {
    content = constructSubSelector(val, ':', '', constructSelector);
  }

  else if (val.is('parentheses')) {
    content = constructSubSelector(val, '(', ')', constructSelector);
  }

  else if (val.is('placeholder')) {
    content = constructSubSelector(val, '%', '', constructSelector);
  }

  else if (val.is('pseudoClass')) {
    content = constructSubSelector(val, ':', '', constructSelector);
  }

  else if (val.is('pseudoElement')) {
    content = addGrammar(val, '::', '');
  }

  else if (val.is('space')) {
    content = ' ';
  }

  else if (val.is('variable')) {
    content = constructSubSelector(val, '$', '', constructSelector);
  }

  else if (simpleIdents.indexOf(val.type) !== -1) {
    content = val.content;
  }

  else if (subSelectors.indexOf(val.type) !== -1) {
    content = constructSubSelector(val, '', '', constructSelector);
  }

  return content;
};

module.exports = {
  constructSelector: constructSelector
};
