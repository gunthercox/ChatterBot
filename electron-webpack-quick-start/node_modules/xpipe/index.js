
'use strict';

/**
 * Xpipe - class consisting of only static methods
 * @class
 */
class Xpipe {

  /**
   * Return a cross-platform IPC path
   * @return {string}
   */
  static eq(path) {
    const prefix = Xpipe.prefix;
    if (prefix.endsWith('/') && path.startsWith('/')) {
      return prefix + path.substr(1);
    }
    return prefix + path;
  }

  /**
   * Returns the prefix on Windows and empty string otherwise
   * @return {string}
   */
  static get prefix() {
    return process.platform === 'win32' ? '//./pipe/' : '';
  }

}

module.exports = Xpipe;
