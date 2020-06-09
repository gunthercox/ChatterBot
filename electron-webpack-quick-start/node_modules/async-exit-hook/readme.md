# async-exit-hook
[![Build Status](https://api.travis-ci.org/Tapppi/async-exit-hook.svg)](https://travis-ci.org/Tapppi/async-exit-hook)
[![Coverage Status](https://coveralls.io/repos/github/Tapppi/async-exit-hook/badge.svg?branch=master)](https://coveralls.io/github/Tapppi/async-exit-hook?branch=master)

> Run some code when the process exits

The `process.on('exit')` event doesn't catch all the ways a process can exit. This module catches:

* process SIGINT, SIGTERM and SIGHUP, SIGBREAK signals  
* process beforeExit and exit events  
* PM2 clustering process shutdown message ([PM2 graceful reload](http://pm2.keymetrics.io/docs/usage/cluster-mode/#graceful-reload))  

Useful for cleaning up. You can also include async handlers, and add custom events to hook and exit on.

Forked and pretty much rewritten from [exit-hook](https://npmjs.com/package/exit-hook).


## Install

```
$ npm install --save async-exit-hook
```

## Usage

### Considerations and warning
#### On `process.exit()` and asynchronous code
**If you use asynchronous exit hooks, DO NOT use `process.exit()` to exit.
The `exit` event DOES NOT support asynchronous code.**
>['beforeExit' is not emitted for conditions causing explicit termination, such as process.exit()]
(https://nodejs.org/api/process.html#process_event_beforeexit)

#### Windows and `process.kill(signal)`
On windows `process.kill(signal)` immediately kills the process, and does not fire signal events, 
and as such, cannot be used to gracefully exit. See *Clustering and child processes* for a
workaround when killing child processes. I'm planning to support gracefully exiting 
with async support on windows soon.

### Clustering and child processes
If you use custom clustering / child processes, you can gracefully shutdown your child process
by sending a shutdown message (`childProc.send('shutdown')`).

### Example
```js
const exitHook = require('async-exit-hook');

exitHook(() => {
    console.log('exiting');
});

// you can add multiple hooks, even across files
exitHook(() => {
    console.log('exiting 2');
});

// you can add async hooks by accepting a callback
exitHook(callback => {
    setTimeout(() => {
        console.log('exiting 3');
        callback();
    }, 1000);
});

// You can hook uncaught errors with uncaughtExceptionHandler(), consequently adding 
// async support to uncaught errors (normally uncaught errors result in a synchronous exit).
exitHook.uncaughtExceptionHandler(err => {
    console.error(err);
});

// You can hook unhandled rejections with unhandledRejectionHandler()
exitHook.unhandledRejectionHandler(err => {
    console.error(err);
});

// You can add multiple uncaught error handlers
// Add the second parameter (callback) to indicate async hooks
exitHook.uncaughtExceptionHandler((err, callback) => {
    sendErrorToCloudOrWhatever(err) // Returns promise
        .then(() => { 
             console.log('Sent err to cloud'); 
         });
        .catch(sendError => {
             console.error('Error sending to cloud: ', err.stack));
        })
        .then(() => callback);
    });
});

// Add exit hooks for a signal or custom message:

// Custom signal
// Arguments are `signal, exitCode` (SIGBREAK is already handled, this is an example)
exitHook.hookEvent('SIGBREAK', 21);

// process event: `message` with a filter
// filter gets all arguments passed to *handler*: `process.on(message, *handler*)`
// Exits on process event `message` with msg `customShutdownMessage` only
exitHook.hookEvent('message', 0, msg => msg !== 'customShutdownMessage');

// All async hooks will work with uncaught errors when you have specified an uncaughtExceptionHandler
throw new Error('awesome');

//=> // Sync uncaughtExcpetion hooks called and retun
//=> '[Error: awesome]'
//=> // Sync hooks called and retun
//=> 'exiting'
//=> 'exiting 2'
//=> // Async uncaughtException hooks return
//=> 'Sent error to cloud'
//=> // Sync uncaughtException hooks return
//=> 'exiting 3'
```


## License

MIT © Tapani Moilanen  
MIT © [Sindre Sorhus](http://sindresorhus.com)
