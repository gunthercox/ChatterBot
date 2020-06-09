"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.buildForge = buildForge;

var path = _interopRequireWildcard(require("path"));

function _index() {
  const data = require("./index");

  _index = function () {
    return data;
  };

  return data;
}

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = Object.defineProperty && Object.getOwnPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : {}; if (desc.get || desc.set) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } } newObj.default = obj; return newObj; } }

function buildForge(forgeOptions, options) {
  const appDir = forgeOptions.dir;
  return (0, _index().build)(Object.assign({
    prepackaged: appDir,
    config: {
      directories: {
        // https://github.com/electron-userland/electron-forge/blob/master/src/makers/generic/zip.js
        output: path.resolve(appDir, "..", "make")
      }
    }
  }, options));
} 
// __ts-babel@6.0.4
//# sourceMappingURL=forge-maker.js.map