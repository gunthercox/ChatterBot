const BluebirdPromise = require("bluebird/js/release/promise")()
BluebirdPromise.config({
  longStackTraces: true,
})
BluebirdPromise.default = BluebirdPromise
module.exports = BluebirdPromise