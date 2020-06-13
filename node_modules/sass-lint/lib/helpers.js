'use strict';

var util = require('util'),
    fs = require('fs'),
    path = require('path'),
    yaml = require('js-yaml'),
    gonzales = require('gonzales-pe-sl');

var helpers = {};

helpers.log = function log (input) {
  console.log(util.inspect(input, false, null));
};

helpers.propertySearch = function (haystack, needle, property) {
  var length = haystack.length,
      i;

  for (i = 0; i < length; i++) {
    if (haystack[i][property] === needle) {
      return i;
    }
  }
  return -1;
};

helpers.isEqual = function (a, b) {
  var startLine = a.start.line === b.start.line ? true : false,
      endLine = a.end.line === b.end.line ? true : false,
      type = a.type === b.type ? true : false,
      length = a.content.length === b.content.length ? true : false;

  if (startLine && endLine && type && length) {
    return true;
  }
  else {
    return false;
  }
};

helpers.isUnique = function (results, item) {
  var search = this.propertySearch(results, item.line, 'line');

  if (search === -1) {
    return true;
  }
  else if (results[search].column === item.column && results[search].message === item.message) {
    return false;
  }
  else {
    return true;
  }
};

helpers.addUnique = function (results, item) {
  if (this.isUnique(results, item)) {
    results.push(item);
  }
  return results;
};

helpers.sortDetects = function (a, b) {
  if (a.line < b.line) {
    return -1;
  }
  if (a.line > b.line) {
    return 1;
  }
  if (a.line === b.line) {
    if (a.column < b.column) {
      return -1;
    }
    if (a.column > b.column) {
      return 1;
    }
    return 0;
  }
  return 0;
};

helpers.isNumber = function (val) {
  if (isNaN(parseInt(val, 10))) {
    return false;
  }
  return true;
};

helpers.isUpperCase = function (str) {
  var pieces = str.split(''),
      i,
      result = 0;

  for (i = 0; i < pieces.length; i++) {
    if (!helpers.isNumber(pieces[i])) {
      if (pieces[i] === pieces[i].toUpperCase() && pieces[i] !== pieces[i].toLowerCase()) {
        result++;
      }
      else {
        return false;
      }
    }
  }
  if (result) {
    return true;
  }
  return false;
};

helpers.isLowerCase = function (str) {
  var pieces = str.split(''),
      i,
      result = 0;

  for (i = 0; i < pieces.length; i++) {
    if (!helpers.isNumber(pieces[i])) {
      if (pieces[i] === pieces[i].toLowerCase() && pieces[i] !== pieces[i].toUpperCase()) {
        result++;
      }
      else {
        return false;
      }
    }
  }
  if (result) {
    return true;
  }
  return false;
};

/**
 * Determines if a given string adheres to camel-case format
 * @param   {string}  str String to test
 * @returns {boolean}     Whether str adheres to camel-case format
 */
helpers.isCamelCase = function (str) {
  return /^[a-z][a-zA-Z0-9]*$/.test(str);
};

/**
 * Determines if a given string adheres to pascal-case format
 * @param   {string}  str String to test
 * @returns {boolean}     Whether str adheres to pascal-case format
 */
helpers.isPascalCase = function (str) {
  return /^[A-Z][a-zA-Z0-9]*$/.test(str);
};

/**
 * Determines if a given string adheres to hyphenated-lowercase format
 * @param   {string}  str String to test
 * @returns {boolean}     Whether str adheres to hyphenated-lowercase format
 */
helpers.isHyphenatedLowercase = function (str) {
  return !(/[^\-a-z0-9]/.test(str));
};

/**
 * Determines if a given string adheres to snake-case format
 * @param   {string}  str String to test
 * @returns {boolean}     Whether str adheres to snake-case format
 */
helpers.isSnakeCase = function (str) {
  return !(/[^_a-z0-9]/.test(str));
};

/**
 * Determines if a given string adheres to strict-BEM format
 * @param   {string}  str String to test
 * @returns {boolean}     Whether str adheres to strict-BEM format
 */
helpers.isStrictBEM = function (str) {
  return /^[a-z](\-?[a-z0-9]+)*(__[a-z0-9](\-?[a-z0-9]+)*)?((_[a-z0-9](\-?[a-z0-9]+)*){0,2})?$/.test(str);
};

/**
 * Determines if a given string adheres to hyphenated-BEM format
 * @param   {string}  str String to test
 * @returns {boolean}     Whether str adheres to hyphenated-BEM format
 */
helpers.isHyphenatedBEM = function (str) {
  return !(/[A-Z]|-{3}|_{3}|[^_]_[^_]/.test(str));
};

helpers.isValidHex = function (str) {
  if (str.match(/^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/)) {
    return true;
  }
  return false;
};

/**
 * Check if a node is a newline character or not
 *
 * @param {Object} node - The node to test
 * @returns {boolean} Whether the node is a newline or not
 */
helpers.isNewLine = function (node) {
  // using type === instead of is just in case node happens to be a string
  return !!(node && node.type === 'space' && node.content.match('\n'));
};

/**
 * Check if a node is a non newline space character or not
 *
 * @param {Object} node - The node to test
 * @returns {boolean} Whether the node is a non newline space or not
 */
helpers.isSpace = function (node) {
  return !!(node && node.type === 'space' && !node.content.match('\n'));
};

helpers.loadConfigFile = function (configPath) {
  var fileDir = path.dirname(configPath),
      fileName = path.basename(configPath),
      fileExtension = path.extname(fileName),
      filePath = path.join(__dirname, 'config', fileDir, fileName),
      file = fs.readFileSync(filePath, 'utf8') || false;

  if (file) {
    if (fileExtension === '.yml') {
      return yaml.safeLoad(file);
    }
  }

  return file;
};

helpers.hasEOL = function (str) {
  return /\r\n|\n/.test(str);
};

helpers.isEmptyLine = function (str) {
  return /(\r\n|\n){2}/.test(str);
};

helpers.stripQuotes = function (str) {
  return str.substring(1, str.length - 1);
};

/**
 * Strips vendor prefixes from a string
 *
 * @param {string} str - The string we wish to remove vendor prefixes from
 * @returns {string} The string without vendor prefixes
 */
helpers.stripPrefix = function (str) {
  var modPropertyArr = str.split('-'),
      modProperty = '',
      prefLength = modPropertyArr[2] === 'osx' ? 2 : 1;

  modPropertyArr.splice(1, prefLength);

  modPropertyArr.forEach(function (item, index) {
    modProperty = modProperty + item;
    if (index > 0 && index < modPropertyArr.length - 1) {
      modProperty = modProperty + '-';
    }
  });

  return modProperty;
};

/**
 * Removes the trailing space from a string
 * @param {string} curSelector - the current selector string
 * @returns {string} curSelector - the current selector minus any trailing space.
 */

helpers.stripLastSpace = function (selector) {

  if (selector.charAt(selector.length - 1) === ' ') {
    return selector.substr(0, selector.length - 1);

  }

  return selector;

};

/**
 * Checks the current selector value against the previous selector value and assesses whether they are
 * a) currently an enforced selector type for nesting (user specified - all true by default)
 * b) whether they should be nested
 * @param {object} currentVal - the current node / part of our selector
 * @param {object} previousVal - the previous node / part of our selector
 * @param {array} elements - a complete array of nestable selector types
 * @param {array} nestable - an array of the types of selector to nest
 * @returns {object} Returns whether we or we should nest and the previous val
 */
helpers.isNestable = function (currentVal, previousVal, elements, nestable) {
  // check if they are nestable by checking the previous element against one
  // of the user specified selector types
  if (elements.indexOf(previousVal) !== -1 && nestable.indexOf(currentVal) !== -1) {
    return true;
  }

  return false;
};

/**
 * Tries to traverse the AST, following a specified path
 * @param   {object}  node           Starting node
 * @param   {array}   traversalPath  Array of Node types to traverse, starting from the first element
 * @returns {array}                  Nodes at the end of the path. Empty array if the traversal failed
 */
helpers.attemptTraversal = function (node, traversalPath) {
  var i,
      nextNodeList,
      currentNodeList = [],
      processChildNode = function processChildNode (child) {
        child.forEach(traversalPath[i], function (n) {
          if (n.content && typeof n.content !== 'string' && n.contains('interpolation')) {
            return false;
          }
          return nextNodeList.push(n);
        });
      };

  node.forEach(traversalPath[0], function (n) {
    currentNodeList.push(n);
  });

  for (i = 1; i < traversalPath.length; i++) {
    if (currentNodeList.length === 0) {
      return [];
    }

    nextNodeList = [];
    currentNodeList.forEach(processChildNode);
    currentNodeList = nextNodeList;
  }
  return currentNodeList;
};

/**
 * Collects all suffix extensions for a selector
 * @param   {object}  ruleset      ASTNode of type ruleset, containing a selector with nested suffix extensions
 * @param   {string}  selectorType Node type of the selector (e.g. class, id)
 * @returns {array}                Array of Nodes with the content property replaced by the complete selector
 *                                       (without '.', '#', etc) resulting from suffix extensions
 */
helpers.collectSuffixExtensions = function (ruleset, selectorType) {
  var parentSelectors = helpers.attemptTraversal(ruleset, ['selector', selectorType, 'ident']),
      childSuffixes = helpers.attemptTraversal(ruleset, ['block', 'ruleset']),
      selectorList = [];

  if (parentSelectors.length === 0) {
    return [];
  }

  // Goes recursively through all nodes that look like suffix extensions. There may be multiple parents that are
  // extended, so lots of looping is required.
  var processChildSuffix = function (child, parents) {
    var currentParents = [],
        selectors = helpers.attemptTraversal(child, ['selector', 'parentSelectorExtension', 'ident']),
        nestedChildSuffixes = helpers.attemptTraversal(child, ['block', 'ruleset']);

    selectors.forEach(function (childSuffixNode) {
      // append suffix extension to all parent selectors
      parents.forEach(function (parent) {
        // clone so we don't modify the actual AST
        var clonedChildSuffixNode = gonzales.createNode(childSuffixNode);
        clonedChildSuffixNode.content = parent.content + clonedChildSuffixNode.content;

        currentParents.push(clonedChildSuffixNode);
      });
    });

    selectorList = selectorList.concat(currentParents);

    nestedChildSuffixes.forEach(function (childSuffix) {
      processChildSuffix(childSuffix, currentParents);
    });
  };

  childSuffixes.forEach(function (childSuffix) {
    processChildSuffix(childSuffix, parentSelectors);
  });

  return parentSelectors.concat(selectorList);
};

/**
 * Check for the partial match of a string in an array
 *
 * @param {string} needle - The value to match
 * @param {Array} haystack - The array of values to try and match to
 * @returns {Boolean} Whether there is a partial match or not
 */
helpers.isPartialStringMatch = function (needle, haystack) {
  for (var i = 0; i < haystack.length; i++) {
    if (haystack[i].indexOf(needle) >= 0) {
      return true;
    }
  }

  return false;
};

/**
 *  A copy of the the stripBom module from https://github.com/sindresorhus/strip-bom/blob/master/index.js
 *  The module requires node > 4 whereas we support earlier versions.
 *  This function strips the BOM marker from the beginning of a file
 *
 * @param {string} str - The string we wish to strip the BOM marker from
 * @returns {string} The string without a BOM marker
 */
helpers.stripBom = function (str) {
  if (typeof str !== 'string') {
    throw new TypeError('Expected a string, got ' + typeof str);
  }

  if (str.charCodeAt(0) === 0xFEFF) {
    return str.slice(1);
  }

  return str;
};

module.exports = helpers;
