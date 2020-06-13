'use strict';

var path = require('path'),
    merge = require('merge'),
    confHelpers = require('./config-helpers'),
    pathIsAbsolute = require('path-is-absolute');

var cacheConfig = {},
    cacheEnabled = false;

module.exports = function (options, configPath) {
  var meta = null,
      metaPath,
      configMerge = false,
      configMergeExists = false,
      optionsMerge = false,
      optionsMergeExists = false,
      finalCacheExists = false,
      config = {},
      finalConfig = {},
      defaults;

  // ensure our inline options and rules are not undefined
  options = options ? options : {};
  options.rules = options.rules ? options.rules : {};

  // ensure our user defined cache option is respected
  if (options.options && options.options.hasOwnProperty('cache-config')) {
    if (options.options['cache-config'] && Object.keys(cacheConfig).length) {
      return cacheConfig;
    }
  }
  else {
    // check to see if the config cache already exists and is enabled
    if (cacheEnabled && Object.keys(cacheConfig).length) {
      return cacheConfig;
    }
  }

  if (options.options && options.options['config-file']) {
    configPath = options.options['config-file'];
  }

  if (!configPath) {
    metaPath = confHelpers.findFile(false, 'package.json');
    if (metaPath) {
      meta = require(metaPath);
    }

    if (meta && meta.sasslintConfig) {
      configPath = path.resolve(path.dirname(metaPath), meta.sasslintConfig);
    }
    else {
      configPath = confHelpers.findFile(false, '.sass-lint.yml');

      if (!configPath) {
        configPath = confHelpers.findFile(false, '.sasslintrc');
      }
    }
  }
  else if (!pathIsAbsolute(configPath)) {
    configPath = path.resolve(process.cwd(), configPath);
  }

  config = confHelpers.loadConfig(configPath);
  config = confHelpers.checkForConfigExtend(config, configPath);

  // check to see if user config contains an options property and whether property has a property called merge-default-rules
  configMergeExists = (config.options && typeof config.options['merge-default-rules'] !== 'undefined');

  // If it does then retrieve the value of it here or return false
  configMerge = configMergeExists ? config.options['merge-default-rules'] : false;

  // check to see if inline options contains an options property and whether property has a property called merge-default-rules
  optionsMergeExists = (options.options && typeof options.options['merge-default-rules'] !== 'undefined');

  // If it does then retrieve the value of it here or return false
  optionsMerge = optionsMergeExists ? options.options['merge-default-rules'] : false;


  // order of preference is inline options > user config > default config
  // merge-default-rules defaults to true so each step above should merge with the previous. If at any step merge-default-rules is set to
  // false it should skip that steps merge.
  defaults = confHelpers.loadDefaults();
  finalConfig = merge.recursive(defaults, config, options);

  // if merge-default-rules is set to false in user config file then we essentially skip the merging with default rules by overwriting our
  // final rules with the content of our user config otherwise we don't take action here as the default merging has already happened
  if (configMergeExists && !configMerge) {
    finalConfig.rules = config.rules;
  }

  // if merge-default-rules is set to false in inline options we essentially skip the merging with our current rules by overwriting our
  // final rules with the content of our user config otherwise we check to see if merge-default-rules is true OR that we have any inline
  // rules, if we do then we want to merge these into our final ruleset.
  if (optionsMergeExists && !optionsMerge) {
    finalConfig.rules = options.rules;
  }
  else if ((optionsMergeExists && optionsMerge) || options.rules && Object.keys(options.rules).length > 0) {
    finalConfig.rules = merge.recursive(finalConfig.rules, options.rules);
  }

  // check to see if our final config contains a cache-config value
  finalCacheExists = (finalConfig.options && typeof finalConfig.options['cache-config'] !== 'undefined');

  // set our global cache enabled flag here, it will be false by default
  cacheEnabled = finalCacheExists ? finalConfig.options['cache-config'] : false;

  // set our cached config to our final config
  cacheConfig = cacheEnabled ? finalConfig : {};

  return finalConfig;
};
