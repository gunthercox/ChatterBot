'use strict';

var helpers = require('../helpers');

var counter,
    syntax;

var findNearestReturnSCSS = function (parent, i) {
  var previous,
      doublePrevious,
      space;

  if (parent.content[i - 1]) {
    previous = parent.content[i - 1];

    if (i >= 2) {
      doublePrevious = parent.content[i - 2];

      // First check to see that the previous line is not a new line as if it is
      // we don't want to recursively run the function again

      if (!helpers.isEmptyLine(previous.content)) {
        if (doublePrevious.type.indexOf('Comment') !== -1) {
          return findNearestReturnSCSS(parent, i - 1);
        }
      }
    }

    if (i >= 1) {
      if (previous.type.indexOf('Comment') !== -1) {
        return findNearestReturnSCSS(parent, i - 1);
      }

      if (previous.type === 'space') {
        space = helpers.isEmptyLine(previous.content);

        // If there's not a new line and it's the first within the block, ignore
        if (!space && (i - 1 === 0)) {
          return false;
        }

        return {
          'space': space,
          'previous': previous
        };
      }
    }
  }
  return false;
};

var findNearestReturnSass = function (parent, i) {
  var previous;

  if (!parent.is('ident') && parent.content[i - 1]) {
    previous = parent.content[i - 1];

    if (counter === 2) {
      return {
        space: true,
        previous: previous
      };
    }

    if (previous.is('space') || previous.is('declarationDelimiter')) {
      if (helpers.hasEOL(previous.content)) {
        counter++;
      }

      return findNearestReturnSass(parent, i - 1);
    }

    // If ruleset, we must reset the parent to be the previous node and
    // loop through that
    else if (previous.is('ruleset') || previous.is('include')) {
      var previousNode = previous.content[previous.content.length - 1];

      // Set the i parameter for findNearestReturn to be the length of the
      // content array in order to get the last one
      return findNearestReturnSass(previousNode, previousNode.content.length);
    }
    else {
      counter = 0;

      if (previous.type.indexOf('Comment') !== -1) {

        // If it's the first line
        if (previous.start.line === 1) {
          return {
            space: true,
            previous: previous
          };
        }

        return findNearestReturnSass(parent, i - 1);
      }
    }
  }

  return {
    space: false,
    previous: previous
  };
};

module.exports = {
  'name': 'empty-line-between-blocks',
  'defaults': {
    'include': true,
    'allow-single-line-rulesets': true
  },
  'detect': function (ast, parser) {
    var result = [];
    syntax = ast.syntax;

    ast.traverseByType('ruleset', function (node, j, p) {
      var space;

      if ((node.start.line === node.end.line) && parser.options['allow-single-line-rulesets']) {
        return false;
      }

      if (syntax === 'scss') {
        space = findNearestReturnSCSS(p, j);

        if (space) {
          if (parser.options.include && !space.space && j !== 1) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': space.previous.end.line,
              'column': 1,
              'message': 'Space expected between blocks',
              'severity': parser.severity
            });
          }
          else if (!parser.options.include && space.space) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': space.previous.end.line,
              'column': 1,
              'message': 'Space not allowed between blocks',
              'severity': parser.severity
            });
          }
        }
      }
      else if (syntax === 'sass') {
        // Reset the counter for each ruleset
        counter = 0;

        if (node.is('ruleset')) {

          node.forEach('block', function (block, i, parent) {
            var previous;

            // Capture the previous node
            if (parent.content[i - 1]) {
              previous = parent.content[i - 1];
            }
            else {
              // Else set the block to act as the previous node
              previous = block;
            }

            // If it's a new line, lets go back up to the selector
            if (previous.is('space') && helpers.hasEOL(previous.content)) {
              space = findNearestReturnSass(p, j);
            }
          });
        }

        if (space && space.previous) {
          if (space.previous.start.line !== 1) {
            if (parser.options.include && !space.space) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': space.previous.end.line + 1,
                'column': 1,
                'message': 'Space expected between blocks',
                'severity': parser.severity
              });
            }
            else if (!parser.options.include && space.space) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'line': space.previous.end.line + 1,
                'column': 1,
                'message': 'Space not allowed between blocks',
                'severity': parser.severity
              });
            }
          }
        }
      }
      return true;
    });

    return result;
  }
};
