"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.ProtonFramework = void 0;

function _builderUtil() {
  const data = require("builder-util");

  _builderUtil = function () {
    return data;
  };

  return data;
}

function _builderUtilRuntime() {
  const data = require("builder-util-runtime");

  _builderUtilRuntime = function () {
    return data;
  };

  return data;
}

function _core() {
  const data = require("./core");

  _core = function () {
    return data;
  };

  return data;
}

function _fileTransformer() {
  const data = require("./fileTransformer");

  _fileTransformer = function () {
    return data;
  };

  return data;
}

function _LibUiFramework() {
  const data = require("./frameworks/LibUiFramework");

  _LibUiFramework = function () {
    return data;
  };

  return data;
}

function _pathManager() {
  const data = require("./util/pathManager");

  _pathManager = function () {
    return data;
  };

  return data;
}

class ProtonFramework extends _LibUiFramework().LibUiFramework {
  constructor(version, distMacOsAppName, isUseLaunchUi) {
    super(version, distMacOsAppName, isUseLaunchUi);
    this.name = "proton"; // noinspection JSUnusedGlobalSymbols

    this.defaultAppIdPrefix = "com.proton-native.";
  }

  getDefaultIcon(platform) {
    if (platform === _core().Platform.WINDOWS) {
      return (0, _pathManager().getTemplatePath)("icons/proton-native/proton-native.ico");
    } else if (platform === _core().Platform.LINUX) {
      return (0, _pathManager().getTemplatePath)("icons/proton-native/linux");
    } else {
      return (0, _pathManager().getTemplatePath)("icons/proton-native/proton-native.icns");
    }
  }

  createTransformer() {
    let babel;
    const babelOptions = {
      ast: false,
      sourceMaps: "inline"
    };

    if (process.env.TEST_SET_BABEL_PRESET === "true") {
      babel = require("@babel/core");
      babel = testOnlyBabel(babel, babelOptions, this.version);
    } else {
      try {
        babel = require("babel-core");
      } catch (e) {
        // babel isn't installed
        _builderUtil().log.debug(null, "don't transpile source code using Babel");

        return null;
      }
    }

    _builderUtil().log.info({
      options: (0, _builderUtilRuntime().safeStringifyJson)(babelOptions, new Set(["presets"]))
    }, "transpile source code using Babel");

    return file => {
      if (!(file.endsWith(".js") || file.endsWith(".jsx")) || file.includes(_fileTransformer().NODE_MODULES_PATTERN)) {
        return null;
      }

      return new Promise((resolve, reject) => {
        return babel.transformFile(file, babelOptions, (error, result) => {
          if (error == null) {
            resolve(result.code);
          } else {
            reject(error);
          }
        });
      });
    };
  }

}

exports.ProtonFramework = ProtonFramework;

function testOnlyBabel(babel, babelOptions, nodeVersion) {
  // out test dir can be located outside of electron-builder node_modules and babel cannot resolve string names of preset
  babelOptions.presets = [[require("@babel/preset-env").default, {
    targets: {
      node: nodeVersion
    }
  }], require("@babel/preset-react")];
  babelOptions.plugins = [// stage 0
  require("@babel/plugin-proposal-function-bind").default, // stage 1
  require("@babel/plugin-proposal-export-default-from").default, require("@babel/plugin-proposal-logical-assignment-operators").default, [require("@babel/plugin-proposal-optional-chaining").default, {
    loose: false
  }], [require("@babel/plugin-proposal-pipeline-operator").default, {
    proposal: "minimal"
  }], [require("@babel/plugin-proposal-nullish-coalescing-operator").default, {
    loose: false
  }], require("@babel/plugin-proposal-do-expressions").default, // stage 2
  [require("@babel/plugin-proposal-decorators").default, {
    legacy: true
  }], require("@babel/plugin-proposal-function-sent").default, require("@babel/plugin-proposal-export-namespace-from").default, require("@babel/plugin-proposal-numeric-separator").default, require("@babel/plugin-proposal-throw-expressions").default, // stage 3
  require("@babel/plugin-syntax-dynamic-import").default, require("@babel/plugin-syntax-import-meta").default, [require("@babel/plugin-proposal-class-properties").default, {
    loose: false
  }], require("@babel/plugin-proposal-json-strings").default];
  babelOptions.babelrc = false;
  return babel;
} 
// __ts-babel@6.0.4
//# sourceMappingURL=ProtonFramework.js.map