'use strict';

const isNpm =
	'npm_config_username' in process.env ||
	'npm_package_name' in process.env ||
	'npm_config_heading' in process.env;

// TODO: This named export should be replaced by a default export as soon as we move to ES modules
exports.isNpm = isNpm;
