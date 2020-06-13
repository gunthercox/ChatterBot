'use strict';

var util = require('util');

module.exports = {
  SassLintFailureError: function (message) {
    Error.captureStackTrace(this, this.constructor);
    this.name = 'SassLintFailureError';
    this.message = message;
  },
  MaxWarningsExceededError: function (message) {
    Error.captureStackTrace(this, this.constructor);
    this.name = 'MaxWarningsExceededError';
    this.message = message;
  }
};

util.inherits(module.exports.SassLintFailureError, Error);
util.inherits(module.exports.MaxWarningsExceededError, Error);
