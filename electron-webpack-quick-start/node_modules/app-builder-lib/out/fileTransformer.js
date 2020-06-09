"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.isElectronCompileUsed = isElectronCompileUsed;
exports.hasDep = hasDep;
exports.createTransformer = createTransformer;
exports.createElectronCompilerHost = createElectronCompilerHost;
exports.NODE_MODULES_PATTERN = void 0;

function _builderUtil() {
  const data = require("builder-util");

  _builderUtil = function () {
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

var path = _interopRequireWildcard(require("path"));

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = Object.defineProperty && Object.getOwnPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : {}; if (desc.get || desc.set) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } } newObj.default = obj; return newObj; } }

/** @internal */
const NODE_MODULES_PATTERN = `${path.sep}node_modules${path.sep}`;
/** @internal */

exports.NODE_MODULES_PATTERN = NODE_MODULES_PATTERN;

function isElectronCompileUsed(info) {
  if (info.config.electronCompile != null) {
    return info.config.electronCompile;
  } // if in devDependencies - it means that babel is used for precompilation or for some reason user decided to not use electron-compile for production


  return hasDep("electron-compile", info);
}
/** @internal */


function hasDep(name, info) {
  const deps = info.metadata.dependencies;
  return deps != null && name in deps;
}
/** @internal */


function createTransformer(srcDir, configuration, extraMetadata, extraTransformer) {
  const mainPackageJson = path.join(srcDir, "package.json");
  const isRemovePackageScripts = configuration.removePackageScripts !== false;
  const packageJson = path.sep + "package.json";
  return file => {
    if (file === mainPackageJson) {
      return modifyMainPackageJson(file, extraMetadata, isRemovePackageScripts);
    }

    if (file.endsWith(packageJson) && file.includes(NODE_MODULES_PATTERN)) {
      return (0, _fsExtraP().readFile)(file, "utf-8").then(it => cleanupPackageJson(JSON.parse(it), {
        isMain: false,
        isRemovePackageScripts
      })).catch(e => _builderUtil().log.warn(e));
    } else if (extraTransformer != null) {
      return extraTransformer(file);
    } else {
      return null;
    }
  };
}
/** @internal */


function createElectronCompilerHost(projectDir, cacheDir) {
  const electronCompilePath = path.join(projectDir, "node_modules", "electron-compile", "lib");
  return require(path.join(electronCompilePath, "config-parser")).createCompilerHostFromProjectRoot(projectDir, cacheDir);
}

const ignoredPackageMetadataProperties = new Set(["dist", "gitHead", "keywords", "build", "jspm", "ava", "xo", "nyc", "eslintConfig", "contributors", "bundleDependencies", "tags"]);

function cleanupPackageJson(data, options) {
  const deps = data.dependencies; // https://github.com/electron-userland/electron-builder/issues/507#issuecomment-312772099

  const isRemoveBabel = deps != null && typeof deps === "object" && !Object.getOwnPropertyNames(deps).some(it => it.startsWith("babel"));

  try {
    let changed = false;

    for (const prop of Object.getOwnPropertyNames(data)) {
      // removing devDependencies from package.json breaks levelup in electron, so, remove it only from main package.json
      if (prop[0] === "_" || ignoredPackageMetadataProperties.has(prop) || options.isRemovePackageScripts && prop === "scripts" || options.isMain && prop === "devDependencies" || !options.isMain && prop === "bugs" || isRemoveBabel && prop === "babel") {
        delete data[prop];
        changed = true;
      }
    }

    if (changed) {
      return JSON.stringify(data, null, 2);
    }
  } catch (e) {
    (0, _builderUtil().debug)(e);
  }

  return null;
}

async function modifyMainPackageJson(file, extraMetadata, isRemovePackageScripts) {
  const mainPackageData = JSON.parse((await (0, _fsExtraP().readFile)(file, "utf-8")));

  if (extraMetadata != null) {
    (0, _builderUtil().deepAssign)(mainPackageData, extraMetadata);
  } // https://github.com/electron-userland/electron-builder/issues/1212


  const serializedDataIfChanged = cleanupPackageJson(mainPackageData, {
    isMain: true,
    isRemovePackageScripts
  });

  if (serializedDataIfChanged != null) {
    return serializedDataIfChanged;
  } else if (extraMetadata != null) {
    return JSON.stringify(mainPackageData, null, 2);
  }

  return null;
} 
// __ts-babel@6.0.4
//# sourceMappingURL=fileTransformer.js.map