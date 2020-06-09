"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.checkBuildRequestOptions = checkBuildRequestOptions;
exports.build = build;
Object.defineProperty(exports, "getArchSuffix", {
  enumerable: true,
  get: function () {
    return _builderUtil().getArchSuffix;
  }
});
Object.defineProperty(exports, "Arch", {
  enumerable: true,
  get: function () {
    return _builderUtil().Arch;
  }
});
Object.defineProperty(exports, "archFromString", {
  enumerable: true,
  get: function () {
    return _builderUtil().archFromString;
  }
});
Object.defineProperty(exports, "CancellationToken", {
  enumerable: true,
  get: function () {
    return _builderUtilRuntime().CancellationToken;
  }
});
Object.defineProperty(exports, "Packager", {
  enumerable: true,
  get: function () {
    return _packager().Packager;
  }
});
Object.defineProperty(exports, "PlatformPackager", {
  enumerable: true,
  get: function () {
    return _platformPackager().PlatformPackager;
  }
});
Object.defineProperty(exports, "PublishManager", {
  enumerable: true,
  get: function () {
    return _PublishManager().PublishManager;
  }
});
Object.defineProperty(exports, "Platform", {
  enumerable: true,
  get: function () {
    return _core().Platform;
  }
});
Object.defineProperty(exports, "Target", {
  enumerable: true,
  get: function () {
    return _core().Target;
  }
});
Object.defineProperty(exports, "DIR_TARGET", {
  enumerable: true,
  get: function () {
    return _core().DIR_TARGET;
  }
});
Object.defineProperty(exports, "DEFAULT_TARGET", {
  enumerable: true,
  get: function () {
    return _core().DEFAULT_TARGET;
  }
});
Object.defineProperty(exports, "AppInfo", {
  enumerable: true,
  get: function () {
    return _appInfo().AppInfo;
  }
});
Object.defineProperty(exports, "buildForge", {
  enumerable: true,
  get: function () {
    return _forgeMaker().buildForge;
  }
});

function _promise() {
  const data = require("builder-util/out/promise");

  _promise = function () {
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

function _builderUtilRuntime() {
  const data = require("builder-util-runtime");

  _builderUtilRuntime = function () {
    return data;
  };

  return data;
}

function _packager() {
  const data = require("./packager");

  _packager = function () {
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

function _PublishManager() {
  const data = require("./publish/PublishManager");

  _PublishManager = function () {
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

function _appInfo() {
  const data = require("./appInfo");

  _appInfo = function () {
    return data;
  };

  return data;
}

function _forgeMaker() {
  const data = require("./forge-maker");

  _forgeMaker = function () {
    return data;
  };

  return data;
}

const expectedOptions = new Set(["publish", "targets", "mac", "win", "linux", "projectDir", "platformPackagerFactory", "config", "effectiveOptionComputed", "prepackaged"]);

function checkBuildRequestOptions(options) {
  for (const optionName of Object.keys(options)) {
    if (!expectedOptions.has(optionName) && options[optionName] !== undefined) {
      throw new (_builderUtil().InvalidConfigurationError)(`Unknown option "${optionName}"`);
    }
  }
}

function build(options, packager = new (_packager().Packager)(options)) {
  checkBuildRequestOptions(options);
  const publishManager = new (_PublishManager().PublishManager)(packager, options);

  const sigIntHandler = () => {
    _builderUtil().log.warn("cancelled by SIGINT");

    packager.cancellationToken.cancel();
    publishManager.cancelTasks();
  };

  process.once("SIGINT", sigIntHandler);
  const promise = packager.build().then(async buildResult => {
    const afterAllArtifactBuild = (0, _platformPackager().resolveFunction)(buildResult.configuration.afterAllArtifactBuild, "afterAllArtifactBuild");

    if (afterAllArtifactBuild != null) {
      const newArtifacts = (0, _builderUtilRuntime().asArray)((await Promise.resolve(afterAllArtifactBuild(buildResult))));

      if (newArtifacts.length === 0 || !publishManager.isPublish) {
        return buildResult.artifactPaths;
      }

      const publishConfigurations = await publishManager.getGlobalPublishConfigurations();

      if (publishConfigurations == null || publishConfigurations.length === 0) {
        return buildResult.artifactPaths;
      }

      for (const newArtifact of newArtifacts) {
        buildResult.artifactPaths.push(newArtifact);

        for (const publishConfiguration of publishConfigurations) {
          publishManager.scheduleUpload(publishConfiguration, {
            file: newArtifact,
            arch: null
          }, packager.appInfo);
        }
      }
    }

    return buildResult.artifactPaths;
  });
  return (0, _promise().executeFinally)(promise, isErrorOccurred => {
    let promise;

    if (isErrorOccurred) {
      publishManager.cancelTasks();
      promise = Promise.resolve(null);
    } else {
      promise = publishManager.awaitTasks();
    }

    return promise.then(() => process.removeListener("SIGINT", sigIntHandler));
  });
} 
// __ts-babel@6.0.4
//# sourceMappingURL=index.js.map