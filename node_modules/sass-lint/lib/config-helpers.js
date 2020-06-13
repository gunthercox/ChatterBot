var yaml = require('js-yaml'),
    fs = require('fs'),
    path = require('path'),
    merge = require('merge'),
    pathIsAbsolute = require('path-is-absolute');

/**
 * Loads the default sass-lint configuration file
 *
 * @returns {Object} The default sass-lint configuration
 */
var loadDefaults = function loadDefaults () {
  return yaml.safeLoad(fs.readFileSync(path.join(__dirname, 'config', 'sass-lint.yml'), 'utf8'));
};

/**
 * Attempts to traverse the tree looking for the specified file
 *
 * @param {String} configPath - The path to look for the file.
 * @param {String} filename - The name of the file.
 * @returns {String} The resolved path
 */
var findFile = function findFile (configPath, filename) {
  var HOME = process.env.HOME || process.env.HOMEPATH || process.env.USERPROFILE,
      dirname = null,
      parentDirname = null;

  configPath = configPath || path.join(process.cwd(), filename);

  if (configPath && fs.existsSync(configPath)) {
    return fs.realpathSync(configPath);
  }
  dirname = path.dirname(configPath);
  parentDirname = path.dirname(dirname);

  if (dirname === null || dirname === HOME || dirname === parentDirname) {
    return null;
  }
  configPath = path.join(parentDirname, filename);

  return findFile(configPath, filename);
};

/**
 * Loads a config file from a specified path if it exists. The resolved config will be returned
 * or a blank config will be in it's place.
 *
 * @param {String} cPath - The path to the config file
 * @returns {Object} The configuration object
 */
var loadConfig = function (cPath) {
  var configPath = cPath,
      resolvedConfig = {};

  if (configPath) {
    if (fs.existsSync(configPath)) {
      resolvedConfig = yaml.safeLoad(fs.readFileSync(configPath, 'utf8')) || {};
    }
  }

  return {
    options: resolvedConfig.options || {},
    files: resolvedConfig.files || {},
    rules: resolvedConfig.rules || {}
  };
};

/**
 * Checks a config file to see if another config file is specified, if it is, the file is laoded
 * and merged with the current configuration object.
 *
 * @param {Object} config - The current configuration
 * @param {String} curConfPath - The current path(incl filename) to the configuration object passed as 'config'
 * @returns {Object} The merged configuration object
 */
var checkForConfigExtend = function (config, curConfPath) {
  var mergedConfig = config,
      subConfig = config.options['config-file'] || false,
      confPath,
      resolvedSubConfig;

  if (subConfig) {
    if (!pathIsAbsolute(subConfig)) {
      // Process.cwd() in most IDE's will be / so therefore we need to pass the current directory
      // of the config from which you are 'extending' or we resort to process.cwd() which on the CLI
      // will be correct
      confPath = curConfPath ? path.dirname(curConfPath) : process.cwd();
      subConfig = path.resolve(confPath, subConfig);
    }
    // Attempt to load the new found config file
    resolvedSubConfig = loadConfig(subConfig, curConfPath);
    // Check the new config file to see if it too is extending
    resolvedSubConfig = checkForConfigExtend(resolvedSubConfig, subConfig);
    // Merge our configs with the first encountered being the most important, down to the last config
    // being the least.
    mergedConfig = merge.recursive(resolvedSubConfig, config);
  }

  return mergedConfig;
};

module.exports = {
  loadDefaults: loadDefaults,
  findFile: findFile,
  loadConfig: loadConfig,
  checkForConfigExtend: checkForConfigExtend
};
