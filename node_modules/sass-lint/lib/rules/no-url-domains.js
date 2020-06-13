'use strict';

var helpers = require('../helpers'),
    url = require('url');

module.exports = {
  'name': 'no-url-domains',
  'defaults': {},
  'detect': function (ast, parser) {
    var result = [];

    ast.traverseByType('uri', function (uri) {
      uri.traverse(function (item) {
        if (item.is('string')) {
          var stripped = helpers.stripQuotes(item.content),
              parsedUrl = url.parse(stripped, false, true);

          if (parsedUrl.host && parsedUrl.protocol !== 'data:') {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'severity': parser.severity,
              'line': item.end.line,
              'column': item.end.column,
              'message': 'Domains in URLs are disallowed'
            });
          }
        }
      });
    });

    return result;
  }
};
