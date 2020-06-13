'use strict';

/**
 * Adds each rule in our array of rules in a disable comment into the toggledRules object
 * under the correct rule name along with the line and column number where the disable comment
 * was encountered
 *
 * @param {Object} toggledRules - Contains the information about each rule disable/enable
                                  encountered and and what line/column it occurred on
 * @param {Array} rules - An array of rule names
 * @param {number} line - The line number the disable appeared on
 * @param {number} column - The column number the disable appeared on
 */
var addDisable = function (toggledRules, rules, line, column) {
  rules.map(function (rule) {
    toggledRules.ruleEnable[rule] = toggledRules.ruleEnable[rule] || [];
    toggledRules.ruleEnable[rule].push([false, line, column]);
  });
};

/**
 * Adds each rule in our array of rules in a enable comment into the toggledRules object
 * under the correct rule name along with the line and column number where the enable comment
 * was encountered
 *
 * @param {Object} toggledRules - Contains the information about each rule enable
                                  encountered and and what line/column it occurred on
 * @param {Array} rules - An array of rule names
 * @param {number} line - The line number the enable appeared on
 * @param {number} column - The column number the enable appeared on
 */
var addEnable = function (toggledRules, rules, line, column) {
  rules.map(function (rule) {
    toggledRules.ruleEnable[rule] = toggledRules.ruleEnable[rule] || [];
    toggledRules.ruleEnable[rule].push([true, line, column]);
  });
};

/**
 * Adds each rule in our array of rules in a disable block comment into the toggledRules object
 * under the correct rule name along with the line and column number where the disable block comment
 * was encountered
 *
 * @param {Object} toggledRules - Contains the information about each rule enable
                                  encountered and and what line/column that block occurred on
 * @param {Array} rules - An array of rule names
 * @param {Object} block - The block that is to be disabled
 */
var addDisableBlock = function (toggledRules, rules, block) {
  rules.map(function (rule) {
    toggledRules.ruleEnable[rule] = toggledRules.ruleEnable[rule] || [];
    toggledRules.ruleEnable[rule].push([false, block.start.line, block.start.column]);
    toggledRules.ruleEnable[rule].push([true, block.end.line, block.end.column]);
  });
};

/**
 * Adds a globally disabled flag to the toggled rules globalEnable property including the line and column
 * that this comment was encountered on.
 *
 * @param {Object} toggledRules - Contains the information about the global disable comment
                                  encountered and and what line/column it occurred on
 * @param {number} line - The line number the disable appeared on
 * @param {number} column - The column number the disable appeared on
 */
var addDisableAll = function (toggledRules, line, column) {
  toggledRules.globalEnable
    .push([false, line, column]);
};

/**
 * Adds a globally enabled flag to the toggled rules globalEnable property including the line and column
 * that this comment was encountered on.
 *
 * @param {Object} toggledRules - Contains the information about the global enable comment
                                  encountered and and what line/column it occurred on
 * @param {number} line - The line number the enable appeared on
 * @param {number} column - The column number the enable appeared on
 */
var addEnableAll = function (toggledRules, line, column) {
  toggledRules.globalEnable
    .push([true, line, column]);
};

/**
 * Adds a line disabled flag to the ruleEnable property of the toggledRules object for each rule name
 * encountered in the comment and which line this comment was discovered on / refers to
 *
 * @param {Object} toggledRules - Contains the information about the line disable comment encountered, the rules
 *                              it relates to and which line it was encountered on
 * @param {Array} rules - An array of rule names to apply
 * @param {number} line - The line number that this disable should refer to
 */
var addDisableLine = function (toggledRules, rules, line) {
  rules.map(function (rule) {
    toggledRules.ruleEnable[rule] = toggledRules.ruleEnable[rule] || [];
    // NOTE: corner case not handled here: a 2nd disable inside an ignored line, which is unrealistically pathological.
    toggledRules.ruleEnable[rule].push([false, line, 1]);
    toggledRules.ruleEnable[rule].push([true, line + 1, 1]);
  });
};

/**
 * This is the sorting function we use to sort the toggle stacks in our getToggledRules method
 * First sorts by line and then by column if the lines are identical
 *
 * @param {Array} toggleRangeA - The first rule to sort
 * @param {Array} toggleRangeB - The second rule to sort
 *
 * @returns {number} A pointer to signify to the sort method how the currently in focus value should be sorted
 */
var sortRange = function (toggleRangeA, toggleRangeB) {
  var aLine = toggleRangeA[1],
      aCol = toggleRangeA[2],
      bLine = toggleRangeB[1],
      bCol = toggleRangeB[2];
  if (aLine < bLine) {
    return -1;
  }
  if (aLine > bLine) {
    return 1;
  }
  if (aCol < bCol) {
    return -1;
  }
  if (aCol > bCol) {
    return 1;
  }
  return 0;
};

/**
 * Checks if line number A is before line number B, if it's the same then it checks if the column of A
 * is before the column of B
 *
 * @param {number} x - The line number of A
 * @param {number} y - The column number of A
 * @param {number} x2 - The line number of B
 * @param {number} y2 - The column number of B
 *
 * @returns {Boolean} Whether the current line/column A is before or the same as B
 */
var isBeforeOrSame = function (x, y, x2, y2) {
  return x < x2 || (x === x2 && y < y2);
};

/**
 * Traverses the AST looking for sass-lint disable/enable comments and then builds an Object/node representation
 * of any it encounters
 *
 * @param {Object} ast - Gonzales PE abstract syntax tree
 *
 * @returns {Object} The toggledRules object containing all of our rule enable/disable information
 */
module.exports.getToggledRules = function (ast) {
  var toggledRules = {
    ruleEnable: {
      // Format in here is [isEnabled, line, column]
    },
    globalEnable: []
  };
  if (!ast.traverseByTypes) {
    return toggledRules;
  }
  ast.traverseByTypes(['multilineComment', 'singlelineComment'], function (comment, i, parent) {
    var content = comment.content;
    if (!content) {
      return;
    }
    var tokens = content.split(/[\s,]+/)
      .filter(function (s) {
        return s.trim().length > 0;
      });
    if (!tokens.length) {
      return;
    }
    var first = tokens[0],
        rules = tokens.slice(1);
    switch (first) {
    case 'sass-lint:disable':
      addDisable(toggledRules, rules, comment.start.line, comment.start.column);
      break;
    case 'sass-lint:enable':
      addEnable(toggledRules, rules, comment.start.line, comment.start.column);
      break;
    case 'sass-lint:disable-block':
      // future ref: not sure what the appropriate behavior is if there is no parent block; currently NPEs
      addDisableBlock(toggledRules, rules, parent);
      break;
    case 'sass-lint:disable-all':
      addDisableAll(toggledRules, comment.start.line, comment.start.column);
      break;
    case 'sass-lint:enable-all':
      addEnableAll(toggledRules, comment.start.line, comment.start.column);
      break;
    case 'sass-lint:disable-line':
      addDisableLine(toggledRules, rules, comment.start.line);
      break;
    default:
      return;
    }
  });
  // Sort these toggle stacks so reading them is easier (algorithmically).
  // Usually already sorted but since it's not guaranteed by the contract with gonzales-pe, ensuring it is.
  toggledRules.globalEnable.sort(sortRange);
  Object.keys(toggledRules.ruleEnable).map(function (ruleId) {
    toggledRules.ruleEnable[ruleId].sort(sortRange);
  });
  return toggledRules;
};

/**
 * Filters our rule results by checking the lint result and its line/column against our
 * toggledRules object to see whether we should still be reporting this lint.
 *
 * @param {Object} toggledRules - The toggledRules object containing all of our rule enable/disable information
 *
 * @returns {Boolean} Whether the current rule is disabled for this lint report
 */
module.exports.isResultEnabled = function (toggledRules) {
  return function (ruleResult) {
    var ruleId = ruleResult.ruleId;
    // Convention: if no column or line, assume rule is targetting 1.
    var line = ruleResult.line || 1;
    var column = ruleResult.column || 1;
    var isGloballyEnabled = toggledRules.globalEnable
      .reduce(function (acc, toggleRange) {
        return isBeforeOrSame(line, column, toggleRange[1], toggleRange[2])
          ? acc
          : toggleRange[0];
      }, true);
    if (!isGloballyEnabled) {
      return false;
    }
    if (!toggledRules.ruleEnable[ruleId]) {
      return true;
    }
    var isRuleEnabled = toggledRules.ruleEnable[ruleId]
      .reduce(function (acc, toggleRange) {
        return isBeforeOrSame(line, column, toggleRange[1], toggleRange[2])
          ? acc
          : toggleRange[0];
      }, true);
    if (!isRuleEnabled) {
      return false;
    }
    return true;
  };
};
