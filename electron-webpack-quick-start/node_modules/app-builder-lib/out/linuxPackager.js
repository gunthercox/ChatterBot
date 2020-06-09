"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.toAppImageOrSnapArch = toAppImageOrSnapArch;
exports.LinuxPackager = void 0;

function _builderUtil() {
  const data = require("builder-util");

  _builderUtil = function () {
    return data;
  };

  return data;
}

function _sanitizeFilename() {
  const data = _interopRequireDefault(require("sanitize-filename"));

  _sanitizeFilename = function () {
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

function _platformPackager() {
  const data = require("./platformPackager");

  _platformPackager = function () {
    return data;
  };

  return data;
}

function _RemoteBuilder() {
  const data = require("./remoteBuilder/RemoteBuilder");

  _RemoteBuilder = function () {
    return data;
  };

  return data;
}

function _LinuxTargetHelper() {
  const data = require("./targets/LinuxTargetHelper");

  _LinuxTargetHelper = function () {
    return data;
  };

  return data;
}

function _targetFactory() {
  const data = require("./targets/targetFactory");

  _targetFactory = function () {
    return data;
  };

  return data;
}

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

class LinuxPackager extends _platformPackager().PlatformPackager {
  constructor(info) {
    super(info, _core().Platform.LINUX);
    const executableName = this.platformSpecificBuildOptions.executableName;
    this.executableName = executableName == null ? this.appInfo.sanitizedName.toLowerCase() : (0, _sanitizeFilename().default)(executableName);
  }

  get defaultTarget() {
    return ["snap", "appimage"];
  }

  createTargets(targets, mapper) {
    let helper;

    const getHelper = () => {
      if (helper == null) {
        helper = new (_LinuxTargetHelper().LinuxTargetHelper)(this);
      }

      return helper;
    };

    let remoteBuilder = null;

    for (const name of targets) {
      if (name === _core().DIR_TARGET) {
        continue;
      }

      const targetClass = (() => {
        switch (name) {
          case "appimage":
            return require("./targets/AppImageTarget").default;

          case "snap":
            return require("./targets/snap").default;

          case "deb":
          case "rpm":
          case "sh":
          case "freebsd":
          case "pacman":
          case "apk":
          case "p5p":
            return require("./targets/fpm").default;

          default:
            return null;
        }
      })();

      mapper(name, outDir => {
        if (targetClass === null) {
          return (0, _targetFactory().createCommonTarget)(name, outDir, this);
        }

        const target = new targetClass(name, this, getHelper(), outDir);

        if (process.platform === "win32" || process.env._REMOTE_BUILD) {
          if (remoteBuilder == null) {
            remoteBuilder = new (_RemoteBuilder().RemoteBuilder)(this);
          } // return remoteBuilder.buildTarget(this, arch, appOutDir, this.packager)


          return new RemoteTarget(target, remoteBuilder);
        }

        return target;
      });
    }
  }

}

exports.LinuxPackager = LinuxPackager;

class RemoteTarget extends _core().Target {
  constructor(target, remoteBuilder) {
    super(target.name, true
    /* all must be scheduled in time (so, on finishBuild RemoteBuilder will have all targets added - so, we must set isAsyncSupported to true (resolved promise is returned)) */
    );
    this.target = target;
    this.remoteBuilder = remoteBuilder;
    this.buildTaskManager = new (_builderUtil().AsyncTaskManager)(this.remoteBuilder.packager.info.cancellationToken);
  }

  get options() {
    return this.target.options;
  }

  get outDir() {
    return this.target.outDir;
  }

  async finishBuild() {
    await this.buildTaskManager.awaitTasks();
    await this.remoteBuilder.build();
  }

  build(appOutDir, arch) {
    const promise = this.doBuild(appOutDir, arch);
    this.buildTaskManager.addTask(promise);
    return promise;
  }

  async doBuild(appOutDir, arch) {
    _builderUtil().log.info({
      target: this.target.name,
      arch: _builderUtil().Arch[arch]
    }, "scheduling remote build");

    await this.target.checkOptions();
    this.remoteBuilder.scheduleBuild(this.target, arch, appOutDir);
  }

}

function toAppImageOrSnapArch(arch) {
  switch (arch) {
    case _builderUtil().Arch.x64:
      return "x86_64";

    case _builderUtil().Arch.ia32:
      return "i386";

    case _builderUtil().Arch.armv7l:
      return "arm";

    case _builderUtil().Arch.arm64:
      return "arm_aarch64";

    default:
      throw new Error(`Unsupported arch ${arch}`);
  }
} 
// __ts-babel@6.0.4
//# sourceMappingURL=linuxPackager.js.map