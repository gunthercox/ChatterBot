'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'indentation',
  'defaults': {
    'size': 2
  },
  'detect': function (ast, parser) {
    var result = [],
        inAtRule = false,
        inProps = false,
        inBlock = false,
        lintSize = parser.options.size,
        lintType = 'space',
        plural = '',
        detected = [lintType];

    // Prepare to check for mixed spaces or tabs depending on what the user has specified
    if (parser.options.size === 'tab') {
      lintSize = 1;
      lintType = 'tab';
      detected[0] = lintType;
    }

    var processNode = function (node, level) {
      var i,
          n,
          prevNode,
          nextNode,
          sassNextNode,
          reportNode,
          reportCondition,
          space,
          spaceLength,
          newlineLength,
          spaceCount,
          tabCount,
          mixedWarning;

      level = level || 0;

      if (node.is('braces')) {
        return;
      }

      for (i = 0; i < node.length; i++) {
        n = node.get(i);
        prevNode = node.get(i - 1);
        nextNode = node.get(i + 1) || false;
        // Due to the Sass structure in gonzales we sometimes need to check 2 ahead
        sassNextNode = node.get(i + 2) || false;
        reportNode = null;

        if (!n) {
          continue;
        }

        if (n.syntax === 'scss') {
          if (n.type === 'space') {

            // Test for CRLF first, since it includes LF
            space = n.content.lastIndexOf('\r\n');
            newlineLength = 2;

            if (space === -1) {
              // Test for LF
              space = n.content.lastIndexOf('\n');
              newlineLength = 1;
            }

            if (space >= 0) {
              // Check how many spaces or tabs we have and set our plural character if necessary for
              // our lint reporting message
              spaceLength = n.content.slice(space + newlineLength).length;
              spaceCount = n.content.slice(space + newlineLength).match(/ /g);
              tabCount = n.content.slice(space + newlineLength).match(/\t/g);
              plural = level > 1 ? 's' : '';
              reportNode = nextNode;
              reportCondition = i !== node.length - 1;
            }
          }
        }
        else if (n.syntax === 'sass') {
          if (n.is('declarationDelimiter') || (helpers.isNewLine(n))) {
            // Due to the way gonzales handles line endings in Sass we don't care if it's CRLF or just LF
            if (nextNode && nextNode.is('space') && nextNode.content.indexOf('\n') === -1) {
              spaceLength = nextNode.content.length;
              spaceCount = nextNode.content.match(/ /g);
              tabCount = nextNode.content.match(/\t/g);
              plural = level > 1 ? 's' : '';

              // if we're at the end of a block we want to drop the level here for Sass
              if (!node.get(i + 2)) {
                level--;
              }

              reportNode = sassNextNode;
              reportCondition = true;
            }
          }
          // Check all the spaces in Sass that aren't newlines
          else if (helpers.isSpace(n)) {
            // This is a special condition for the first property in a block with Sass as it usually
            // doesn't have a previous node before the space appears so we need to check this is
            // valid and then we can rely on the declarationDelimiter check above.
            if (inBlock && (!prevNode || prevNode.is('space'))) {
              inBlock = false;
              spaceLength = n.content.length;
              spaceCount = n.content.match(/ /g);
              tabCount = n.content.match(/\t/g);
              plural = level > 1 ? 's' : '';
              reportNode = nextNode;
              reportCondition = true;
            }
            // A extra check for tabs when using spaces as single tab characters aren't highlighted
            // as mixed spaces and tabs without this. Spaces on the other hand are fine. Gonzales
            // reports them a little differently.
            else if (n.type === 'space' && lintType === 'space') {
              tabCount = n.content.match(/\t/g);
              reportNode = nextNode;
              // we dont want to check the lint levels here as it could be a tab between a prop and
              // value, totally unrealistic I know but we still want to report it.
              reportCondition = false;
            }
          }
        }
        if (reportNode) {
          // if we've encountered a space check if we have before if not save a reference
          if (spaceCount !== null && detected.indexOf('space') === -1) {
            detected.push('space');
          }

          // if we've encountered a tab check if we have before if not save a reference
          if (tabCount !== null && detected.indexOf('tab') === -1) {
            detected.push('tab');
          }

          if (detected.length > 1) {
            // Indicates we've told the user about mixed tabs and spaces in their file
            mixedWarning = true;
            // Remove the last detected type from our detected array,
            // if we encounter a mix again we'll output again but all the while keep a reference
            // to the first space character (tab or space) that we encountered so as to be
            // consistent with our warnings
            detected.pop();
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': reportNode.start.line,
              'column': reportNode.start.column,
              'message': 'Mixed tabs and spaces',
              'severity': parser.severity
            });
          }
          if (reportCondition && !mixedWarning && spaceLength / lintSize !== level) {
            // Check if expected indentation matches what it should be
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': reportNode.start.line,
              'column': reportNode.start.column,
              'message': 'Expected indentation of ' + level * lintSize + ' ' + lintType + plural + ' but found ' + spaceLength + '.',
              'severity': parser.severity
            });
          }
          mixedWarning = false;
        }
        // if we're in an atrule make we need to possibly handle multiline arguments
        if (n.is('atrule') && n.contains('block')) {
          inAtRule = true;
          inBlock = false;
        }

        // if a delimeter is encountered we check if it's directly after a parenthesis node
        // if it is we know next node will be the same level of indentation
        if (n.is('operator')) {
          if (n.content === ',' && prevNode.is('parentheses') && helpers.isNewLine(nextNode)) {
            if (inAtRule && !inProps) {
              level++;
              inProps = true;
            }
            else if (!inProps) {
              level--;
            }
          }
        }

        // if a block node is encountered we first check to see if it's within an include/function
        // by checking if the node also contains arguments, if it does we skip the block as we add a level
        // for arguments anyway. If not the the block is a usual ruleset block and should be treated accordingly
        // The other checks are kept from 1.0 and work for their respective types.
        if ((n.is('block') && !node.contains('arguments'))
          || n.is('arguments')
          || (n.is('parentheses') && !node.is('atrule'))
        ) {
          level++;
        }

        if (n.is('block')) {
          inAtRule = false;
          inProps = false;
          inBlock = true;
        }
        processNode(n, level);
      }
    };

    processNode(ast);
    return result;
  }
};
