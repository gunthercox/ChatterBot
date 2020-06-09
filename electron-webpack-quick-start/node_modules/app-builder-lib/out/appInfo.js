"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.filterCFBundleIdentifier = filterCFBundleIdentifier;
exports.smarten = smarten;
exports.AppInfo = void 0;

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

function _semver() {
  const data = require("semver");

  _semver = function () {
    return data;
  };

  return data;
}

function _macroExpander() {
  const data = require("./util/macroExpander");

  _macroExpander = function () {
    return data;
  };

  return data;
}

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

class AppInfo {
  constructor(info, buildVersion, platformSpecificOptions = null) {
    this.info = info;
    this.platformSpecificOptions = platformSpecificOptions;
    this.description = smarten(this.info.metadata.description || "");
    this.version = info.metadata.version;

    if (buildVersion == null) {
      buildVersion = info.config.buildVersion;
    }

    this.buildNumber = process.env.BUILD_NUMBER || process.env.TRAVIS_BUILD_NUMBER || process.env.APPVEYOR_BUILD_NUMBER || process.env.CIRCLE_BUILD_NUM || process.env.BUILD_BUILDNUMBER || process.env.CI_PIPELINE_IID;

    if (buildVersion == null) {
      buildVersion = this.version;

      if (!(0, _builderUtil().isEmptyOrSpaces)(this.buildNumber)) {
        buildVersion += `.${this.buildNumber}`;
      }
    }

    this.buildVersion = buildVersion;
    this.productName = info.config.productName || info.metadata.productName || info.metadata.name;
    this.productFilename = (0, _sanitizeFilename().default)(this.productName);
  }

  get channel() {
    const prereleaseInfo = (0, _semver().prerelease)(this.version);

    if (prereleaseInfo != null && prereleaseInfo.length > 0) {
      return prereleaseInfo[0];
    }

    return null;
  }

  getVersionInWeirdWindowsForm(isSetBuildNumber = true) {
    const parsedVersion = new (_semver().SemVer)(this.version); // https://github.com/electron-userland/electron-builder/issues/2635#issuecomment-371792272

    let buildNumber = isSetBuildNumber ? this.buildNumber : null;

    if (buildNumber == null || !/^\d+$/.test(buildNumber)) {
      buildNumber = "0";
    }

    return `${parsedVersion.major}.${parsedVersion.minor}.${parsedVersion.patch}.${buildNumber}`;
  }

  get notNullDevMetadata() {
    return this.info.devMetadata || {};
  }

  get companyName() {
    const author = this.info.metadata.author || this.notNullDevMetadata.author;
    return author == null ? null : author.name;
  }

  get id() {
    let appId = null;

    for (const options of [this.platformSpecificOptions, this.info.config]) {
      if (options != null && appId == null) {
        appId = options.appId;
      }
    }

    const generateDefaultAppId = () => {
      const info = this.info;
      return `${info.framework.defaultAppIdPrefix}${info.metadata.name.toLowerCase()}`;
    };

    if (appId != null && (appId === "your.id" || (0, _builderUtil().isEmptyOrSpaces)(appId))) {
      const incorrectAppId = appId;
      appId = generateDefaultAppId();

      _builderUtil().log.warn(`do not use "${incorrectAppId}" as appId, "${appId}" will be used instead`);
    }

    return appId == null ? generateDefaultAppId() : appId;
  }

  get macBundleIdentifier() {
    return filterCFBundleIdentifier(this.id);
  }

  get name() {
    return this.info.metadata.name;
  }

  get linuxPackageName() {
    const name = this.name; // https://github.com/electron-userland/electron-builder/issues/2963

    return name.startsWith("@") ? this.productFilename : name;
  }

  get sanitizedName() {
    return (0, _sanitizeFilename().default)(this.name);
  }

  get updaterCacheDirName() {
    return this.sanitizedName.toLowerCase() + "-updater";
  }

  get copyright() {
    const copyright = this.info.config.copyright;

    if (copyright != null) {
      return (0, _macroExpander().expandMacro)(copyright, null, this);
    }

    return `Copyright © ${new Date().getFullYear()} ${this.companyName || this.productName}`;
  }

  async computePackageUrl() {
    const url = this.info.metadata.homepage || this.notNullDevMetadata.homepage;

    if (url != null) {
      return url;
    }

    const info = await this.info.repositoryInfo;
    return info == null || info.type !== "github" ? null : `https://${info.domain}/${info.user}/${info.project}`;
  }

}
/** @internal */


exports.AppInfo = AppInfo;

function filterCFBundleIdentifier(identifier) {
  // Remove special characters and allow only alphanumeric (A-Z,a-z,0-9), hyphen (-), and period (.)
  // Apple documentation: https://developer.apple.com/library/mac/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-102070
  return identifier.replace(/ /g, "-").replace(/[^a-zA-Z0-9.-]/g, "");
} // fpm bug - rpm build --description is not escaped, well... decided to replace quite to smart quote
// http://leancrew.com/all-this/2010/11/smart-quotes-in-javascript/


function smarten(s) {
  // opening singles
  s = s.replace(/(^|[-\u2014\s(\["])'/g, "$1\u2018"); // closing singles & apostrophes

  s = s.replace(/'/g, "\u2019"); // opening doubles

  s = s.replace(/(^|[-\u2014/\[(\u2018\s])"/g, "$1\u201c"); // closing doubles

  s = s.replace(/"/g, "\u201d");
  return s;
} 
// __ts-babel@6.0.4
//# sourceMappingURL=appInfo.js.map