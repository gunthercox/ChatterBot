'use strict';

var slConfig = require('./lib/config'),
    groot = require('./lib/groot'),
    exceptions = require('./lib/exceptions'),
    helpers = require('./lib/helpers'),
    slRules = require('./lib/rules'),
    ruleToggler = require('./lib/ruleToggler'),
    glob = require('glob'),
    path = require('path'),
    fs = require('fs-extra'),
    globule = require('globule');

var getToggledRules = ruleToggler.getToggledRules,
    isResultEnabled = ruleToggler.isResultEnabled;

var sassLint = function (config) { // eslint-disable-line no-unused-vars
  config = require('./lib/config')(config);
  return;
};

/**
 * Takes any user specified options and a configPath
 * which returns a compiled config object
 *
 * @param {object} config user specified rules/options passed in
 * @param {string} configPath path to a config file
 * @returns {object} the compiled config object
 */
sassLint.getConfig = function (config, configPath) {
  return slConfig(config, configPath);
};

/**
 * Parses our results object to count errors and return
 * paths to files with detected errors.
 *
 * @param {object} results our results object
 * @returns {object} errors object containing the error count and paths for files incl. errors
 */
sassLint.errorCount = function (results) {
  var errors = {
    count: 0,
    files: []
  };

  results.forEach(function (result) {
    if (result.errorCount) {
      errors.count += result.errorCount;
      errors.files.push(result.filePath);
    }
  });

  return errors;
};

/**
 * Parses our results object to count warnings and return
 * paths to files with detected warnings.
 *
 * @param {object} results our results object
 * @returns {object} warnings object containing the error count and paths for files incl. warnings
 */
sassLint.warningCount = function (results) {
  var warnings = {
    count: 0,
    files: []
  };

  results.forEach(function (result) {
    if (result.warningCount) {
      warnings.count += result.warningCount;
      warnings.files.push(result.filePath);
    }
  });

  return warnings;
};

/**
 * Parses our results object to count warnings and errors and return
 * a cumulative count of both
 *
 * @param {object} results our results object
 * @returns {int} the cumulative count of errors and warnings detected
 */
sassLint.resultCount = function (results) {
  var warnings = this.warningCount(results),
      errors = this.errorCount(results);

  return warnings.count + errors.count;
};

/**
 * Runs each rule against our AST tree and returns our main object of detected
 * errors, warnings, messages and filenames.
 *
 * @param {object} file file object from fs.readFileSync
 * @param {object} options user specified rules/options passed in
 * @param {string} configPath path to a config file
 * @returns {object} an object containing error & warning counts plus lint messages for each parsed file
 */
sassLint.lintText = function (file, options, configPath) {
  var rules = slRules(this.getConfig(options, configPath)),
      ast = {},
      detects,
      results = [],
      errors = 0,
      warnings = 0,
      ruleToggles = null,
      isEnabledFilter = null;

  try {
    ast = groot(file.text, file.format, file.filename);
  }
  catch (e) {
    var line = e.line || 1;
    errors++;

    results = [{
      ruleId: 'Fatal',
      line: line,
      column: 1,
      message: e.message,
      severity: 2
    }];
  }

  if (ast.content && ast.content.length > 0) {
    ruleToggles = getToggledRules(ast);
    isEnabledFilter = isResultEnabled(ruleToggles);

    rules.forEach(function (rule) {
      detects = rule.rule.detect(ast, rule)
        .filter(isEnabledFilter);
      results = results.concat(detects);
      if (detects.length) {
        if (rule.severity === 1) {
          warnings += detects.length;
        }
        else if (rule.severity === 2) {
          errors += detects.length;
        }
      }
    });
  }

  results.sort(helpers.sortDetects);

  return {
    'filePath': file.filename,
    'warningCount': warnings,
    'errorCount': errors,
    'messages': results
  };
};

/**
 * Handles ignored files for plugins such as the gulp plugin. Checks every file passed to it against
 * the ignores as specified in our users config or passed in options.
 *
 * @param {object} file - The file/text to be linted
 * @param {object} options - The user defined options directly passed in
 * @param {object} configPath - Path to a config file
 * @returns {object} Return the results of lintText - a results object
 */
sassLint.lintFileText = function (file, options, configPath) {
  var config = this.getConfig(options, configPath),
      ignores = config.files ? config.files.ignore : [];

  if (!globule.isMatch(ignores, file.filename)) {
    return this.lintText(file, options, configPath);
  }

  return {
    'filePath': file.filename,
    'warningCount': 0,
    'errorCount': 0,
    'messages': []
  };
};

/**
 * Takes a glob pattern or target string and creates an array of files as targets for
 * linting taking into account any user specified ignores. For each resulting file sassLint.lintText
 * is called which returns an object of results for that file which we push to our results object.
 *
 * @param {string} files a glob pattern or single file path as a lint target
 * @param {object} options user specified rules/options passed in
 * @param {string} configPath path to a config file
 * @returns {object} results object containing all results
 */
sassLint.lintFiles = function (files, options, configPath) {
  var that = this,
      results = [],
      includes = [],
      ignores = '';

  // Files passed as a string on the command line
  if (files) {
    ignores = this.getConfig(options, configPath).files.ignore || '';
    if (files.indexOf(', ') !== -1) {
      files.split(', ').forEach(function (pattern) {
        includes = includes.concat(glob.sync(pattern, {ignore: ignores, nodir: true}));
      });
    }
    else {
      includes = glob.sync(files, {ignore: ignores, nodir: true});
    }
  }
  // If not passed in then we look in the config file
  else {
    files = this.getConfig(options, configPath).files;
    // A glob pattern of files can be just a string
    if (typeof files === 'string') {
      includes = glob.sync(files, {nodir: true});
    }
    // Look into the include property of files and check if there's an array of files
    else if (files.include && files.include instanceof Array) {
      files.include.forEach(function (pattern) {
        includes = includes.concat(glob.sync(pattern, {ignore: files.ignore, nodir: true}));
      });
    }
    // Or there is only one pattern in the include property of files
    else {
      includes = glob.sync(files.include, {ignore: files.ignore, nodir: true});
    }
  }

  includes.forEach(function (file, index) {
    // Only lint non duplicate files from our glob results
    if (includes.indexOf(file) === index) {
      var lint = that.lintText({
        'text': fs.readFileSync(file),
        'format': options.syntax ? options.syntax : path.extname(file).replace('.', ''),
        'filename': file
      }, options, configPath);
      results.push(lint);
    }
  });

  return results;
};

/**
 * Handles formatting of results using EsLint formatters
 *
 * @param {object} results our results object
 * @param {object} options user specified rules/options passed in
 * @param {string} configPath path to a config file
 * @returns {object} results our results object in the user specified format
 */
sassLint.format = function (results, options, configPath) {
  var config = this.getConfig(options, configPath),
      format = config.options.formatter.toLowerCase();

  var formatted = require('eslint/lib/formatters/' + format);

  return formatted(results);
};

/**
 * Handles outputting results whether this be straight to the console/stdout or to a file.
 * Passes results to the format function to ensure results are output in the chosen format
 *
 * @param {object} results our results object
 * @param {object} options user specified rules/options passed in
 * @param {string} configPath path to a config file
 * @returns {object} results our results object
 */
sassLint.outputResults = function (results, options, configPath) {
  var config = this.getConfig(options, configPath);

  if (this.resultCount(results)) {

    var formatted = this.format(results, options, configPath);

    if (config.options['output-file']) {
      try {
        fs.outputFileSync(path.resolve(process.cwd(), config.options['output-file']), formatted);
        console.log('Output successfully written to ' + path.resolve(process.cwd(), config.options['output-file']));
      }
      catch (e) {
        console.log('Error: Output was unable to be written to ' + path.resolve(process.cwd(), config.options['output-file']));
      }
    }
    else {
      console.log(formatted);
    }
  }
  return results;
};

/**
 * Throws an error if there are any errors detected. The error includes a count of all errors
 * and a list of all files that include errors.
 *
 * @param {object} results - our results object
 * @param {object} [options] - extra options to use when running failOnError, e.g. max-warnings
 * @param {string} [configPath] - path to the config file
 * @returns {void}
 */
sassLint.failOnError = function (results, options, configPath) {
  // Default parameters
  options = typeof options !== 'undefined' ? options : {};
  configPath = typeof configPath !== 'undefined' ? configPath : null;

  var errorCount = this.errorCount(results),
      warningCount = this.warningCount(results),
      configOptions = this.getConfig(options, configPath).options;

  if (errorCount.count > 0) {
    throw new exceptions.SassLintFailureError(errorCount.count + ' errors were detected in \n- ' + errorCount.files.join('\n- '));
  }

  if (!isNaN(configOptions['max-warnings']) && warningCount.count > configOptions['max-warnings']) {
    throw new exceptions.MaxWarningsExceededError(
      'Number of warnings (' + warningCount.count +
      ') exceeds the allowed maximum of ' + configOptions['max-warnings'] +
      '.\n'
    );
  }
};

module.exports = sassLint;
