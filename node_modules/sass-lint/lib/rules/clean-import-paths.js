'use strict';

var helpers = require('../helpers'),
    path = require('path');

var getImportPath = function (parent, syntax) {
  if (parent.first('uri')) {
    return parent.first('uri');
  }

  if (parent.first('string')) {
    return helpers.stripQuotes(parent.first('string').content);
  }

  if (parent.first('ident')) {

    if (syntax === 'sass') {
      var output = '',
          isFinished = false;

      parent.forEach(function (item) {
        // Force an end if we've appended a 'class'.. aka file extension
        if (!isFinished) {
          // Since we don't have quotes, gonzales-pe will parse file path as
          // multiple different types
          if (
            item.type === 'string'
            || item.type === 'operator'
            || item.type === 'ident'
          ) {
            output += item.content;
          }

          // Gonzales-pe parses file extensions as classes if they are not
          // wrapped in quotes...
          if (item.type === 'class') {
            if (item.first('ident')) {
              output += '.' + item.first('ident').content;
            }

            isFinished = true;
          }
        }
      });

      return output.trim();
    }

    return parent.first('ident');
  }

  return false;
};

module.exports = {
  'name': 'clean-import-paths',
  'defaults': {
    'leading-underscore': false,
    'filename-extension': false
  },
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('atkeyword', function (keyword, i, parent) {
      keyword.forEach(function (item) {
        if (item.content === 'import') {
          var importPath = getImportPath(parent, keyword.syntax);

          if (importPath) {
            if (typeof importPath === 'string') {
              var filename = path.basename(importPath),
                  fileExtension = path.extname(filename);

              if (fileExtension === '.sass' || fileExtension === '.scss' || fileExtension === '') {
                if (filename.charAt(0) === '_') {
                  if (!parser.options['leading-underscore']) {
                    result = helpers.addUnique(result, {
                      'ruleId': parser.rule.name,
                      'line': item.start.line,
                      'column': item.start.column,
                      'message': 'Leading underscores are not allowed',
                      'severity': parser.severity
                    });
                  }
                }
                else {
                  if (parser.options['leading-underscore']) {
                    result = helpers.addUnique(result, {
                      'ruleId': parser.rule.name,
                      'line': item.start.line,
                      'column': item.start.column,
                      'message': 'Leading underscores are required',
                      'severity': parser.severity
                    });
                  }
                }

                if (fileExtension) {
                  if (!parser.options['filename-extension']) {
                    result = helpers.addUnique(result, {
                      'ruleId': parser.rule.name,
                      'line': item.start.line,
                      'column': item.start.column,
                      'message': 'File extensions are not allowed',
                      'severity': parser.severity
                    });
                  }
                }
                else {
                  if (parser.options['filename-extension']) {
                    result = helpers.addUnique(result, {
                      'ruleId': parser.rule.name,
                      'line': item.start.line,
                      'column': item.start.column,
                      'message': 'File extensions are required',
                      'severity': parser.severity
                    });
                  }
                }
              }
            }
          }
        }
      });
    });

    return result;
  }
};
