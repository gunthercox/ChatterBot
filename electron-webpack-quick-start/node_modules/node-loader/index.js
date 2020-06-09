/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/
module.exports = function() {
  return "try {global.process.dlopen(module, " + JSON.stringify(this.resourcePath) + "); } catch(e) {" +
    "throw new Error('Cannot open ' + " + JSON.stringify(this.resourcePath) + " + ': ' + e);}";
}