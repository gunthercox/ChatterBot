'use strict';

var helpers = require('../helpers');

module.exports = {
  'name': 'property-units',
  'defaults': {
    'per-property': {},
    'global': []
  },
  'detect': function (ast, parser) {
    var result = [],
        unitsAllowedGlobally = parser.options.global,
        unitsAllowedPerProperty = parser.options['per-property'];

    ast.traverseByType('declaration', function (declaration) {
      var property = declaration.first('property'),
          ident = property ? property.first('ident') : null,
          propertyName = ident ? ident.content : null,
          valueNode = declaration.first('value'),
          hasDimension = valueNode ? !!valueNode.first('dimension') : null;
      if (propertyName && hasDimension) {
        // properties such as box-shadow may have multiple dimensions defined so enumerate through them
        valueNode.forEach('dimension', function (dimension) {
          var dimensionIdent = dimension ? dimension.first('ident') : null,
              unitType = dimensionIdent ? dimensionIdent.content : null,
              unitsAllowed = unitsAllowedPerProperty[propertyName];
          // If a property is defined in unitsAllowed, then it will only validate those unit types
          if (unitType && unitsAllowed) {
            if (unitsAllowed.indexOf(unitType) === -1) {
              result = helpers.addUnique(result, {
                'ruleId': parser.rule.name,
                'severity': parser.severity,
                'line': dimension.start.line,
                'column': dimension.start.column,
                'message': 'Values for property \'' + propertyName + '\' may not use ' + unitType + ' units'
              });
            }
          }
          // If no units are defined in unitsAllowedGlobally, then allow all of them
          // Otherwise, verify the given unit is in the unitsAllowedGlobally list.
          else if (unitType && unitsAllowedGlobally.length && unitsAllowedGlobally.indexOf(unitType) === -1) {
            result = helpers.addUnique(result, {
              'ruleId': parser.rule.name,
              'severity': parser.severity,
              'line': dimension.start.line,
              'column': dimension.start.column,
              'message': 'Values for property \'' + propertyName + '\' may not use ' + unitType + ' units'
            });
          }
        });
      }
    });
    return result;
  }
};
