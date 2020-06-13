'use strict';

/*!
 * node.extend
 * Copyright 2011, John Resig
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * @fileoverview
 * Port of jQuery.extend that actually works on node.js
 */
var is = require('is');
var has = require('has');

var defineProperty = Object.defineProperty;
var gOPD = Object.getOwnPropertyDescriptor;

// If name is '__proto__', and Object.defineProperty is available, define __proto__ as an own property on target
var setProperty = function setP(target, name, value) {
  if (defineProperty && name === '__proto__') {
    defineProperty(target, name, {
      enumerable: true,
      configurable: true,
      value: value,
      writable: true
    });
  } else {
    target[name] = value;
  }
};

// Return undefined instead of __proto__ if '__proto__' is not an own property
var getProperty = function getP(obj, name) {
  if (name === '__proto__') {
    if (!has(obj, name)) {
      return void 0;
    } else if (gOPD) {
      // In early versions of node, obj['__proto__'] is buggy when obj has
      // __proto__ as an own property. Object.getOwnPropertyDescriptor() works.
      return gOPD(obj, name).value;
    }
  }

  return obj[name];
};

// eslint-disable-next-line func-style
function extend() {
  var target = arguments[0] || {};
  var i = 1;
  var length = arguments.length;
  var deep = false;
  var options, name, src, copy, copyIsArray, clone;

  // Handle a deep copy situation
  if (typeof target === 'boolean') {
    deep = target;
    target = arguments[1] || {};
    // skip the boolean and the target
    i = 2;
  }

  // Handle case when target is a string or something (possible in deep copy)
  if (typeof target !== 'object' && !is.fn(target)) {
    target = {};
  }

  for (; i < length; i++) {
    // Only deal with non-null/undefined values
    options = arguments[i];
    if (options != null) {
      if (typeof options === 'string') {
        options = options.split('');
      }
      // Extend the base object
      for (name in options) {
        src = getProperty(target, name);
        copy = getProperty(options, name);

        // Prevent never-ending loop
        if (target === copy) {
          continue;
        }

        // Recurse if we're merging plain objects or arrays
        if (deep && copy && (is.hash(copy) || (copyIsArray = is.array(copy)))) {
          if (copyIsArray) {
            copyIsArray = false;
            clone = src && is.array(src) ? src : [];
          } else {
            clone = src && is.hash(src) ? src : {};
          }

          // Never move original objects, clone them
          setProperty(target, name, extend(deep, clone, copy));

        // Don't bring in undefined values
        } else if (typeof copy !== 'undefined') {
          setProperty(target, name, copy);
        }
      }
    }
  }

  // Return the modified object
  return target;
}

/**
 * @public
 */
extend.version = '1.1.7';

/**
 * Exports module.
 */
module.exports = extend;
