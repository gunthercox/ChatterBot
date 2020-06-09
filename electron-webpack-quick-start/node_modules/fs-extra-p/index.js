"use strict"

const path = require("path")
const nodeFs = require("fs")
const fsExtra = require("fs-extra")
const Promise = require('bluebird-lst')

function makeFs(Promise) {
  const fs = Object.create(null)

  for (const methodName of Object.keys(fsExtra)) {
    const method = fsExtra[methodName]
    if (methodName === "createFile" || methodName === "mkdirp") {
      continue
    }

    if (typeof method !== "function" ||
        methodName.endsWith("Sync") ||
        methodName.endsWith("Stream") ||
        methodName.match(/^[A-Z]/) ||
        methodName === "exists" ||
        methodName === "watch" ||
        methodName === "watchFile" ||
        methodName === "unwatchFile") {
      fs[methodName] = method
    }
    else {
      fs[methodName] = Promise.promisify(method)
    }
  }

  fs.createFile = fs.ensureFile
  fs.mkdirp = fs.mkdirs
  return fs
}

const newFs = makeFs(Promise)

newFs.emptyDir = function (dir) {
  return new Promise((resolve, reject) => {
    nodeFs.readdir(dir, (error, files) => {
      if (error == null) {
        Promise.map(files, it => newFs.remove(path.join(dir, it)))
          .then(resolve)
          .catch(reject)
      }
      else {
        newFs.mkdirs(dir)
          .then(resolve)
          .catch(reject)
      }
    })
  })
}

module.exports = newFs