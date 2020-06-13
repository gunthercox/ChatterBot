'use strict';

var helpers = require('../helpers'),
    selectorHelpers = require('../selector-helpers');

var mergeableNodes = ['atrule', 'include', 'ruleset'],
    validAtRules = ['media'],
    curLevel = 0,
    curSelector = [],
    parentSelector = [],
    selectorList = [];


/**
 * Traverses a block and calls our callback function for each block encountered
 *
 * @param {object} block - The current node / part of our selector
 * @param {object} cb - The callback function we wish to apply to each block
 * @returns {undefined}
 */
var traverseBlock = function (block, cb) {
  block.forEach(function (contentItem) {
    cb(contentItem);
  });
};

/**
 * Traverses a block and calls our callback function for each block encountered
 *
 * @param {string} ruleSet - The current selector
 * @param {boolean} isAtRule - Whether the ruleSet is an atRule
 * @param {string} line - The line that the ruleset starts
 * @param {string} col - The column that the ruleset starts
 * @returns {undefined}
 */
var updateList = function (ruleSet, isAtRule, line, col) {
  parentSelector[curLevel] = ruleSet;
  curSelector = {
    selector: helpers.stripLastSpace(parentSelector.join('')),
    line: line,
    column: col
  };
  if (!isAtRule) {
    selectorList.push(curSelector);
  }
};

/**
 * Checks a rulesets contents for selectors and calls our consstructSelector method
 *
 * @param {object} ruleNode - The current node / part of our selector
 * @returns {undefined}
 */
var checkRuleset = function (ruleNode) {
  var ruleSet = '';
  ruleNode.forEach(function (ruleNodeItem) {
    if (!ruleNodeItem.is('block')) {
      if (ruleNodeItem.is('selector')) {
        ruleNodeItem.forEach(function (selectorContent) {
          ruleSet += selectorHelpers.constructSelector(selectorContent);
        });
      }
      else if (ruleNodeItem.is('delimiter') || ruleNodeItem.is('space')) {
        ruleSet += selectorHelpers.constructSelector(ruleNodeItem);
      }
    }
  });
  if (ruleSet !== '') {
    updateList(ruleSet, false, ruleNode.start.line, ruleNode.start.column);
  }
};

/**
 * Checks an atRule contents for selectors and calls our consstructSelector method
 *
 * @param {object} atRule - The current node / atRule part of our selector
 * @returns {undefined}
 */
var checkAtRule = function (atRule) {
  var test = '';
  atRule.forEach(function (atRuleItem) {
    if (!atRuleItem.is('block')) {
      test += selectorHelpers.constructSelector(atRuleItem);
    }
  });
  updateList(test, true, atRule.start.line, atRule.start.column);
};

/**
 * Checks an atRule to see if if it's part of our mergeable at rule list.
 *
 * @param {object} node - The current node / atRule part of our selector
 * @returns {boolean} Whether this atRule should be merged or not
 */
var isMergeableAtRule = function (node) {
  var isMergeable = false;
  node.forEach(function (item) {
    // TODO Check back when Gonzales updates to fix this
    // Gonzales has issues with nest levels in media queries :(
    if (item.is('atkeyword') && validAtRules.indexOf(item.first('ident').content) !== -1) {
      isMergeable = true;
    }
  });

  return isMergeable;
};

/**
 * Checks if a node contains a block and if so calls our traverseBlock method. Also
 * handles our current level counter.
 *
 * @param {object} node - The current node / atRule part of our selector
 * @param {object} cb - The callback function we wish to pass through
 * @returns {undefined}
 */
var checkForBlock = function (node, cb) {
  if (node.contains('block')) {
    curLevel += 1;
    node.forEach('block', function (block) {
      traverseBlock(block.content, cb);
    });
    curLevel -= 1;
    parentSelector.pop();
  }
};

/**
 * Traverses a node and checks for rulesets and at rules and then fires off to the
 * respective method for them to be handled
 *
 * @param {object} node - The current node / atRule part of our selector
 * @returns {undefined}
 */
var traverseNode = function (node) {
  if (mergeableNodes.indexOf(node.type) !== -1) {
    if (node.is('ruleset')) {
      checkRuleset(node);
      checkForBlock(node, traverseNode);
    }
    else if (node.is('atrule')) {
      if (isMergeableAtRule(node)) {
        checkAtRule(node);
        checkForBlock(node, traverseNode);
      }
    }
  }
};

/**
 * Checks our selector list for mergeable selectors and reports errors where needed
 *
 * @param {object} parser - The parser object
 * @returns {array} Array of result objects
 */
var checkMergeable = function (parser) {
  var result = [];
  selectorList.forEach(function (item, index, arr) {
    var pos = helpers.propertySearch(arr, item.selector, 'selector');
    if (pos !== index && parser.options.whitelist.indexOf(item.selector) === -1) {
      result = helpers.addUnique(result, {
        'ruleId': parser.rule.name,
        'line': item.line,
        'column': item.column,
        'message': 'Rule `' + item.selector + '` should be merged with the rule on line ' + selectorList[pos].line,
        'severity': parser.severity
      });
    }
  });
  return result;
};

module.exports = {
  'name': 'no-mergeable-selectors',
  'defaults': {
    'whitelist': []
  },
  'detect': function (ast, parser) {
    curLevel = 0;
    curSelector = [];
    parentSelector = [];
    selectorList = [];
    ast.traverseByType('stylesheet', function (styleSheet) {
      traverseBlock(styleSheet, traverseNode);
    });
    return checkMergeable(parser);
  }
};
