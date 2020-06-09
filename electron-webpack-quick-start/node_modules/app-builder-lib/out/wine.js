"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.execWine = execWine;
exports.prepareWindowsExecutableArgs = prepareWindowsExecutableArgs;

function _builderUtil() {
  const data = require("builder-util");

  _builderUtil = function () {
    return data;
  };

  return data;
}

/** @private */
function execWine(file, file64 = null, appArgs = [], options = {}) {
  if (process.platform === "win32") {
    if (options.timeout == null) {
      // 2 minutes
      options.timeout = 120 * 1000;
    }

    return (0, _builderUtil().exec)(file, appArgs, options);
  }

  const commandArgs = ["wine", "--ia32", file];

  if (file64 != null) {
    commandArgs.push("--x64", file64);
  }

  if (appArgs.length > 0) {
    commandArgs.push("--args", JSON.stringify(appArgs));
  }

  return (0, _builderUtil().executeAppBuilder)(commandArgs, undefined, options);
}
/** @private */


function prepareWindowsExecutableArgs(args, exePath) {
  if (process.platform !== "win32") {
    args.unshift(exePath);
  }

  return args;
} 
// __ts-babel@6.0.4
//# sourceMappingURL=wine.js.map