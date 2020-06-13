'use strict';

var merge = require('merge'),
    path = require('path'),
    fs = require('fs');

var searchArray = function (haystack, needle) {
  var i;
  for (i = 0; i < haystack.length; i++) {
    if (haystack[i].indexOf(needle) >= 0) {
      return i;
    }
  }
  return -1;
};

module.exports = function (config) {
  var handlers = [],
      i,
      rules;

  rules = fs.readdirSync(path.join(__dirname, 'rules'));
  for (i = 0; i < rules.length; i++) {
    rules[i] = path.join(__dirname, 'rules', rules[i]);
  }

  Object.keys(config.rules).forEach(function (rule) {
    var fullRule = config.rules[rule],
        loadRule,
        severity,
        options,
        ruleSearch;

    if (typeof fullRule === 'number') {
      severity = fullRule;
      options = {};
    }
    else {
      severity = fullRule[0];
      options = fullRule[1];
    }

    // Only seek out rules that are enabled
    if (severity !== 0) {
      var fileName = path.normalize(path.join('/', rule + '.js'));

      ruleSearch = searchArray(rules, fileName);

      if (ruleSearch >= 0) {
        loadRule = require(rules[ruleSearch]);

        options = merge.recursive(true, loadRule.defaults, options);

        handlers.push({
          'rule': loadRule,
          'severity': severity,
          'options': options
        });
      }
      else {
        throw new Error('Rule `' + rule + '` could not be found!');
      }
    }
  });

  return handlers;
};
