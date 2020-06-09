"use strict"

const path = require("path")

function getPath() {
  if (process.env.USE_SYSTEM_APP_BUILDER === "true") {
    return "app-builder"
  }

  const platform = process.platform;
  if (platform === "darwin") {
    return path.join(__dirname, "mac", "app-builder")
  }
  else if (platform === "win32") {
    return path.join(__dirname, "win", process.arch, "app-builder.exe")
  }
  else {
    return path.join(__dirname, "linux", process.arch, "app-builder")
  }
}

exports.appBuilderPath = getPath()