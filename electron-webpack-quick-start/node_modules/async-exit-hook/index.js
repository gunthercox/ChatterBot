'use strict';

const hooks = [];
const errHooks = [];
let called = false;
let waitingFor = 0;
let asyncTimeoutMs = 10000;

const events = {};
const filters = {};

function exit(exit, code, err) {
	// Helper functions
	let doExitDone = false;

	function doExit() {
		if (doExitDone) {
			return;
		}
		doExitDone = true;

		if (exit === true) {
			// All handlers should be called even if the exit-hook handler was registered first
			process.nextTick(process.exit.bind(null, code));
		}
	}

	// Async hook callback, decrements waiting counter
	function stepTowardExit() {
		process.nextTick(() => {
			if (--waitingFor === 0) {
				doExit();
			}
		});
	}

	// Runs a single hook
	function runHook(syncArgCount, err, hook) {
		// Cannot perform async hooks in `exit` event
		if (exit && hook.length > syncArgCount) {
			// Hook is async, expects a finish callback
			waitingFor++;

			if (err) {
				// Pass error, calling uncaught exception handlers
				return hook(err, stepTowardExit);
			}
			return hook(stepTowardExit);
		}

		// Hook is synchronous
		if (err) {
			// Pass error, calling uncaught exception handlers
			return hook(err);
		}
		return hook();
	}

	// Only execute hooks once
	if (called) {
		return;
	}

	called = true;

	// Run hooks
	if (err) {
		// Uncaught exception, run error hooks
		errHooks.map(runHook.bind(null, 1, err));
	}
	hooks.map(runHook.bind(null, 0, null));

	if (waitingFor) {
		// Force exit after x ms (10000 by default), even if async hooks in progress
		setTimeout(() => {
			doExit();
		}, asyncTimeoutMs);
	} else {
		// No asynchronous hooks, exit immediately
		doExit();
	}
}

// Add a hook
function add(hook) {
	hooks.push(hook);

	if (hooks.length === 1) {
		add.hookEvent('exit');
		add.hookEvent('beforeExit', 0);
		add.hookEvent('SIGHUP', 128 + 1);
		add.hookEvent('SIGINT', 128 + 2);
		add.hookEvent('SIGTERM', 128 + 15);
		add.hookEvent('SIGBREAK', 128 + 21);

		// PM2 Cluster shutdown message. Caught to support async handlers with pm2, needed because
		// explicitly calling process.exit() doesn't trigger the beforeExit event, and the exit
		// event cannot support async handlers, since the event loop is never called after it.
		add.hookEvent('message', 0, function (msg) { // eslint-disable-line prefer-arrow-callback
			if (msg !== 'shutdown') {
				return true;
			}
		});
	}
}

// New signal / event to hook
add.hookEvent = function (event, code, filter) {
	events[event] = function () {
		const eventFilters = filters[event];
		for (let i = 0; i < eventFilters.length; i++) {
			if (eventFilters[i].apply(this, arguments)) {
				return;
			}
		}
		exit(code !== undefined && code !== null, code);
	};

	if (!filters[event]) {
		filters[event] = [];
	}

	if (filter) {
		filters[event].push(filter);
	}
	process.on(event, events[event]);
};

// Unhook signal / event
add.unhookEvent = function (event) {
	process.removeListener(event, events[event]);
	delete events[event];
	delete filters[event];
};

// List hooked events
add.hookedEvents = function () {
	const ret = [];
	for (const name in events) {
		if ({}.hasOwnProperty.call(events, name)) {
			ret.push(name);
		}
	}
	return ret;
};

// Add an uncaught exception handler
add.uncaughtExceptionHandler = function (hook) {
	errHooks.push(hook);

	if (errHooks.length === 1) {
		process.once('uncaughtException', exit.bind(null, true, 1));
	}
};

// Add an unhandled rejection handler
add.unhandledRejectionHandler = function (hook) {
	errHooks.push(hook);

	if (errHooks.length === 1) {
		process.once('unhandledRejection', exit.bind(null, true, 1));
	}
};

// Configure async force exit timeout
add.forceExitTimeout = function (ms) {
	asyncTimeoutMs = ms;
};

// Export
module.exports = add;
