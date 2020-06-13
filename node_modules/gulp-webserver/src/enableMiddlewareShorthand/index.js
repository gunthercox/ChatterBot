var extend = require('node.extend');

// TODO: Make this its own npm module and repo
module.exports = function(defaults, options, props)
{
  var originalDefaults = extend(true, {},defaults);
  var config = extend(true, defaults, options);

  // If we get a single string, convert it to a single item array
  if(Object.prototype.toString.call(props) == '[object String]') {
    props = [props];
  }

  // Loop through all of the given middlewares
  for (var i = 0, len = props.length; i < len; i++) {
    var prop = props[i];
    // If using the shorthand syntax
    if (config[prop] === true) {
      // Replace the given tree for the tree defaults
      config[prop] = extend(true, {}, originalDefaults[prop]);
      // Set the enable flag, which then can be reliably used for conditionals
      config[prop].enable = true;
    }
  }
  return config;
};