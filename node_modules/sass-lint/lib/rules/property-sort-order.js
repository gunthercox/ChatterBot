'use strict';

var helpers = require('../helpers'),
    yaml = require('js-yaml'),
    fs = require('fs'),
    path = require('path');

var propertyCheckList = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../data', 'properties.yml'), 'utf8')).split(' ');

var orderPresets = {
  'recess': 'recess.yml',
  'smacss': 'smacss.yml',
  'concentric': 'concentric.yml'
};

var getOrderConfig = function (order) {
  if (typeof order === 'string') {
    if (orderPresets.hasOwnProperty(order)) {
      var filename = orderPresets[order],
          orderConfig = helpers.loadConfigFile('property-sort-orders/' + filename);

      return orderConfig.order;
    }
  }

  return false;
};

var sortProperties = function (obj, order) {
  var keys = Object.keys(obj),
      unknown = [],
      sorted = {},
      i;

  if (typeof order === 'string') {
    if (order === 'alphabetical') {
      keys = keys.sort();
    }
  }
  else if (typeof order === 'object') {
    var orderedKeys = [];

    for (i = 0; i < order.length; i++) {
      if (keys.indexOf(order[i]) !== -1) {
        orderedKeys.push(order[i]);
      }
    }

    keys = orderedKeys;
  }
  else {
    keys = keys.sort(function (a, b) {
      if (order.indexOf(a) === -1) {
        if (unknown.indexOf(a) === -1) {
          unknown.push(a);
        }
      }
      if (order.indexOf(b) === -1) {
        if (unknown.indexOf(b) === -1) {
          unknown.push(b);
        }
      }

      if (order.indexOf(a) > order.indexOf(b)) {
        return 1;
      }
      if (order.indexOf(a) < order.indexOf(b)) {
        return -1;
      }
      return 0;
    });
  }

  for (i = 0; i < unknown.length; i++) {
    if (keys.indexOf(unknown[i]) !== -1) {
      keys.splice(keys.indexOf(unknown[i]), 1);
    }
  }

  keys = keys.concat(unknown.sort());

  for (i = 0; i < keys.length; i++) {
    sorted[keys[i]] = obj[keys[i]];
  }

  return sorted;
};

module.exports = {
  'name': 'property-sort-order',
  'defaults': {
    'order': 'alphabetical',
    'ignore-custom-properties': false
  },
  'detect': function (ast, parser) {
    var result = [],
        order = getOrderConfig(parser.options.order) || parser.options.order;

    ast.traverseByType('block', function (block) {
      var properties = {},
          sorted,
          pKeys,
          sKeys;

      if (block) {
        block.forEach('declaration', function (dec) {
          var prop = dec.first('property'),
              name = prop.first('ident');

          if (name) {
            if (parser.options['ignore-custom-properties']) {
              if (propertyCheckList.indexOf(name.content) !== -1) {
                properties[name.content] = prop;
              }
            }
            else {
              properties[name.content] = prop;
            }
          }
        });

        sorted = sortProperties(properties, order);

        pKeys = Object.keys(properties);
        sKeys = Object.keys(sorted);

        sKeys.every(function (e, i) {
          var pKey = pKeys[i],
              prop = properties[pKey];

          if (e !== pKey) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'line': prop.start.line,
              'column': prop.start.column,
              'message': 'Expected `' + e + '`, found `' + pKey + '`',
              'severity': parser.severity
            });
          }
          return true;
        });
      }
    });

    return result;
  }
};
