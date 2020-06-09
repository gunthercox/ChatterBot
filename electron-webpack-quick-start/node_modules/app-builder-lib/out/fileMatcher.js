"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getMainFileMatchers = getMainFileMatchers;
exports.getNodeModuleFileMatcher = getNodeModuleFileMatcher;
exports.getFileMatchers = getFileMatchers;
exports.copyFiles = copyFiles;
exports.FileMatcher = exports.excludedExts = exports.excludedNames = void 0;

function _bluebirdLst() {
  const data = _interopRequireDefault(require("bluebird-lst"));

  _bluebirdLst = function () {
    return data;
  };

  return data;
}

function _builderUtil() {
  const data = require("builder-util");

  _builderUtil = function () {
    return data;
  };

  return data;
}

function _fs() {
  const data = require("builder-util/out/fs");

  _fs = function () {
    return data;
  };

  return data;
}

function _fsExtraP() {
  const data = require("fs-extra-p");

  _fsExtraP = function () {
    return data;
  };

  return data;
}

function _minimatch() {
  const data = require("minimatch");

  _minimatch = function () {
    return data;
  };

  return data;
}

var path = _interopRequireWildcard(require("path"));

function _filter() {
  const data = require("./util/filter");

  _filter = function () {
    return data;
  };

  return data;
}

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = Object.defineProperty && Object.getOwnPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : {}; if (desc.get || desc.set) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// https://github.com/electron-userland/electron-builder/issues/733
const minimatchOptions = {
  dot: true
}; // noinspection SpellCheckingInspection

const excludedNames = ".git,.hg,.svn,CVS,RCS,SCCS," + "__pycache__,.DS_Store,thumbs.db,.gitignore,.gitkeep,.gitattributes,.npmignore," + ".idea,.vs,.flowconfig,.jshintrc,.eslintrc,.circleci," + ".yarn-integrity,.yarn-metadata.json,yarn-error.log,yarn.lock,package-lock.json,npm-debug.log," + "appveyor.yml,.travis.yml,circle.yml,.nyc_output";
exports.excludedNames = excludedNames;
const excludedExts = "iml,hprof,orig,pyc,pyo,rbc,swp,csproj,sln,suo,xproj,cc,d.ts";
exports.excludedExts = excludedExts;

function ensureNoEndSlash(file) {
  if (path.sep !== "/") {
    file = file.replace(/\//g, path.sep);
  }

  if (path.sep !== "\\") {
    file = file.replace(/\\/g, path.sep);
  }

  if (file.endsWith(path.sep)) {
    return file.substring(0, file.length - 1);
  } else {
    return file;
  }
}
/** @internal */


class FileMatcher {
  constructor(from, to, macroExpander, patterns) {
    this.macroExpander = macroExpander;
    this.excludePatterns = null;
    this.from = ensureNoEndSlash(macroExpander(from));
    this.to = ensureNoEndSlash(macroExpander(to));
    this.patterns = (0, _builderUtil().asArray)(patterns).map(it => this.normalizePattern(it));
    this.isSpecifiedAsEmptyArray = Array.isArray(patterns) && patterns.length === 0;
  }

  normalizePattern(pattern) {
    if (pattern.startsWith("./")) {
      pattern = pattern.substring("./".length);
    }

    return path.posix.normalize(this.macroExpander(pattern.replace(/\\/g, "/")));
  }

  addPattern(pattern) {
    this.patterns.push(this.normalizePattern(pattern));
  }

  prependPattern(pattern) {
    this.patterns.unshift(this.normalizePattern(pattern));
  }

  isEmpty() {
    return this.patterns.length === 0;
  }

  containsOnlyIgnore() {
    return !this.isEmpty() && this.patterns.find(it => !it.startsWith("!")) == null;
  }

  computeParsedPatterns(result, fromDir) {
    const relativeFrom = fromDir == null ? null : path.relative(fromDir, this.from);

    if (this.patterns.length === 0 && relativeFrom != null) {
      // file mappings, from here is a file
      result.push(new (_minimatch().Minimatch)(relativeFrom, minimatchOptions));
      return;
    }

    for (let pattern of this.patterns) {
      if (relativeFrom != null) {
        pattern = path.join(relativeFrom, pattern);
      }

      const parsedPattern = new (_minimatch().Minimatch)(pattern, minimatchOptions);
      result.push(parsedPattern); // do not add if contains dot (possibly file if has extension)

      if (!pattern.includes(".") && !(0, _filter().hasMagic)(parsedPattern)) {
        // https://github.com/electron-userland/electron-builder/issues/545
        // add **/*
        result.push(new (_minimatch().Minimatch)(`${pattern}/**/*`, minimatchOptions));
      }
    }
  }

  createFilter() {
    const parsedPatterns = [];
    this.computeParsedPatterns(parsedPatterns);
    return (0, _filter().createFilter)(this.from, parsedPatterns, this.excludePatterns);
  }

  toString() {
    return `from: ${this.from}, to: ${this.to}, patterns: ${this.patterns.join(", ")}`;
  }

}
/** @internal */


exports.FileMatcher = FileMatcher;

function getMainFileMatchers(appDir, destination, macroExpander, platformSpecificBuildOptions, platformPackager, outDir, isElectronCompile) {
  const packager = platformPackager.info;
  const buildResourceDir = path.resolve(packager.projectDir, packager.buildResourcesDir);
  let matchers = packager.isPrepackedAppAsar ? null : getFileMatchers(packager.config, "files", destination, {
    macroExpander,
    customBuildOptions: platformSpecificBuildOptions,
    globalOutDir: outDir,
    defaultSrc: appDir
  });

  if (matchers == null) {
    matchers = [new FileMatcher(appDir, destination, macroExpander)];
  }

  const matcher = matchers[0]; // add default patterns, but only if from equals to app dir

  if (matcher.from !== appDir) {
    return matchers;
  } // https://github.com/electron-userland/electron-builder/issues/1741#issuecomment-311111418 so, do not use inclusive patterns


  const patterns = matcher.patterns;
  const customFirstPatterns = []; // electron-webpack - we need to copy only package.json and node_modules from root dir (and these files are added by default), so, explicit empty array is specified

  if (!matcher.isSpecifiedAsEmptyArray && (matcher.isEmpty() || matcher.containsOnlyIgnore())) {
    customFirstPatterns.push("**/*");
  } else if (!patterns.includes("package.json")) {
    patterns.push("package.json");
  } // https://github.com/electron-userland/electron-builder/issues/1482


  const relativeBuildResourceDir = path.relative(matcher.from, buildResourceDir);

  if (relativeBuildResourceDir.length !== 0 && !relativeBuildResourceDir.startsWith(".")) {
    customFirstPatterns.push(`!${relativeBuildResourceDir}{,/**/*}`);
  }

  const relativeOutDir = matcher.normalizePattern(path.relative(packager.projectDir, outDir));

  if (!relativeOutDir.startsWith(".")) {
    customFirstPatterns.push(`!${relativeOutDir}{,/**/*}`);
  } // add our default exclusions after last user possibly defined "all"/permissive pattern


  let insertIndex = 0;

  for (let i = patterns.length - 1; i >= 0; i--) {
    if (patterns[i].startsWith("**/")) {
      insertIndex = i + 1;
      break;
    }
  }

  patterns.splice(insertIndex, 0, ...customFirstPatterns);
  patterns.push(`!**/*.{${excludedExts}${packager.config.includePdb === true ? "" : ",pdb"}`);
  patterns.push("!**/._*");
  patterns.push("!**/electron-builder.{yaml,yml,json,json5,toml}");
  patterns.push(`!**/{${excludedNames}}`);

  if (isElectronCompile) {
    patterns.push("!.cache{,/**/*}");
  } // https://github.com/electron-userland/electron-builder/issues/1969
  // exclude ony for app root, use .yarnclean to clean node_modules


  patterns.push("!.editorconfig");
  const debugLogger = packager.debugLogger;

  if (debugLogger.isEnabled) {
    //tslint:disable-next-line:no-invalid-template-strings
    debugLogger.add(`${macroExpander("${arch}")}.firstOrDefaultFilePatterns`, patterns);
  }

  return matchers;
}
/** @internal */


function getNodeModuleFileMatcher(appDir, destination, macroExpander, platformSpecificBuildOptions, packager) {
  // https://github.com/electron-userland/electron-builder/pull/2948#issuecomment-392241632
  // grab only excludes
  const matcher = new FileMatcher(appDir, destination, macroExpander);

  function addPatterns(patterns) {
    if (patterns == null) {
      return;
    } else if (!Array.isArray(patterns)) {
      if (typeof patterns === "string" && patterns.startsWith("!")) {
        matcher.addPattern(patterns);
        return;
      } // ignore object form


      return;
    }

    for (const pattern of patterns) {
      if (typeof pattern === "string") {
        if (pattern.startsWith("!")) {
          matcher.addPattern(pattern);
        }
      } else {
        const fileSet = pattern;

        if (fileSet.from == null || fileSet.from === ".") {
          for (const p of (0, _builderUtil().asArray)(fileSet.filter)) {
            matcher.addPattern(p);
          }
        }
      }
    }
  }

  addPatterns(packager.config.files);
  addPatterns(platformSpecificBuildOptions.files);

  if (!matcher.isEmpty()) {
    matcher.prependPattern("**/*");
  }

  const debugLogger = packager.debugLogger;

  if (debugLogger.isEnabled) {
    //tslint:disable-next-line:no-invalid-template-strings
    debugLogger.add(`${macroExpander("${arch}")}.nodeModuleFilePatterns`, matcher.patterns);
  }

  return matcher;
}
/** @internal */


function getFileMatchers(config, name, defaultDestination, options) {
  const defaultMatcher = new FileMatcher(options.defaultSrc, defaultDestination, options.macroExpander);
  const fileMatchers = [];

  function addPatterns(patterns) {
    if (patterns == null) {
      return;
    } else if (!Array.isArray(patterns)) {
      if (typeof patterns === "string") {
        defaultMatcher.addPattern(patterns);
        return;
      }

      patterns = [patterns];
    }

    for (const pattern of patterns) {
      if (typeof pattern === "string") {
        // use normalize to transform ./foo to foo
        defaultMatcher.addPattern(pattern);
      } else if (name === "asarUnpack") {
        throw new Error(`Advanced file copying not supported for "${name}"`);
      } else {
        const from = pattern.from == null ? options.defaultSrc : path.resolve(options.defaultSrc, pattern.from);
        const to = pattern.to == null ? defaultDestination : path.resolve(defaultDestination, pattern.to);
        fileMatchers.push(new FileMatcher(from, to, options.macroExpander, pattern.filter));
      }
    }
  }

  if (name !== "extraDistFiles") {
    addPatterns(config[name]);
  }

  addPatterns(options.customBuildOptions[name]);

  if (!defaultMatcher.isEmpty()) {
    // default matcher should be first in the array
    fileMatchers.unshift(defaultMatcher);
  } // we cannot exclude the whole out dir, because sometimes users want to use some file in the out dir in the patterns


  const relativeOutDir = defaultMatcher.normalizePattern(path.relative(options.defaultSrc, options.globalOutDir));

  if (!relativeOutDir.startsWith(".")) {
    defaultMatcher.addPattern(`!${relativeOutDir}/*-unpacked{,/**/*}`);
  }

  return fileMatchers.length === 0 ? null : fileMatchers;
}
/** @internal */


function copyFiles(matchers, transformer, isUseHardLink) {
  if (matchers == null || matchers.length === 0) {
    return Promise.resolve();
  }

  return _bluebirdLst().default.map(matchers, async matcher => {
    const fromStat = await (0, _fs().statOrNull)(matcher.from);

    if (fromStat == null) {
      _builderUtil().log.warn({
        from: matcher.from
      }, `file source doesn't exist`);

      return;
    }

    if (fromStat.isFile()) {
      const toStat = await (0, _fs().statOrNull)(matcher.to); // https://github.com/electron-userland/electron-builder/issues/1245

      if (toStat != null && toStat.isDirectory()) {
        return await (0, _fs().copyOrLinkFile)(matcher.from, path.join(matcher.to, path.basename(matcher.from)), fromStat, isUseHardLink);
      }

      await (0, _fsExtraP().ensureDir)(path.dirname(matcher.to));
      return await (0, _fs().copyOrLinkFile)(matcher.from, matcher.to, fromStat);
    }

    if (matcher.isEmpty() || matcher.containsOnlyIgnore()) {
      matcher.prependPattern("**/*");
    }

    _builderUtil().log.debug({
      matcher
    }, "copying files using pattern");

    return await (0, _fs().copyDir)(matcher.from, matcher.to, {
      filter: matcher.createFilter(),
      transformer,
      isUseHardLink: isUseHardLink ? _fs().USE_HARD_LINKS : null
    });
  });
} 
// __ts-babel@6.0.4
//# sourceMappingURL=fileMatcher.js.map