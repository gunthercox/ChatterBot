# crocket

[![Build status](https://travis-ci.org/Hexagon/crocket.svg)](https://travis-ci.org/Hexagon/crocket) [![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://img.shields.io/badge/license-MIT-blue.svg)

Minimal node.js cross platform IPC communication library.

* Communcates over TCP, unix sockets or windows pipe.
* Works both locally and remotely.
* Works on Linux, Windows AND macOS.
* Pluggable event mediator, uses EventEmitter by default. But can be extended with something like [qbus](https://www.npmjs.com/package/qbus) for extended functionality.


# Installation

```npm install crocket```

# Usage

### Host process

```javascript
var ipc = require("crocket"),
	server = new ipc();

// Start listening, this example communicate by file sockets
server.listen({ "path": "/tmp/crocket-ipc-test.sock" }, (e) => { 

	// Fatal errors are supplied as the first parameter to callback
	if(e) throw e; 

	// All is well if we got this far
	console.log('IPC listening on /tmp/crocket-test.sock');

});

// Events are handled by EventEmitter by default ...
server.on('/request/food', function (payload) {
	
	// Respond to the query
	server.emit('/response', 'You asked for food and supplied ' + payload);

});


// React to communication errors
server.on('error', (e) => { console.error('Communication error occurred: ', e); });
```

Output

```
> node test-server.js
IPC listening on /tmp/crocket-test.sock
```

### Client process

```javascript
var ipc = require("crocket"),
	client = new ipc();
	
client.connect({ "path": "/tmp/crocket-test.sock" }, (e) => { 

    // Connection errors are supplied as the first parameter to callback
    if(e) throw e; 

    // Instantly a message to the server
    client.emit('/request/food', 'cash');

});

// Expect a reply on '/response'
client.on('/response', function (what) {

    // Should print 'Server said: You asked for food and supplied cash'
    console.log('Server said: ' + what);

    // Work is done now, no need to keep a connection open
    client.close();

});
```

Output

```
> node test-client.js
Server said: You asked for food and supplied cash
```

### Replacing EventEmitter

### Host process

```javascript
var ipc = require("crocket"),
	server = new ipc(),

	// Require the alternative event handler
	qbus = require("qbus");

// Use!
server.use(qbus);

// Start listening, this example communicate by file sockets
server.listen({ "path": "/tmp/crocket-ipc-test.sock" }, (e) => { 

	// Fatal errors are supplied as the first parameter to callback
	if(e) throw e; 

	// All is well if we got this far
	console.log('IPC listening on /tmp/crocket-test.sock');

});

// Now we're using qbus to handle events
//   Documentation:	https://github.com/unkelpehr/qbus
//   Query tester: 	http://unkelpehr.github.io/qbus/
server.on('/request/:what', function (what, payload) {
	
	// Respond to the query
	server.emit('/response', 'You asked for ' + what + ' and supplied ' + payload);

});

// React to communication errors
server.on('error', (e) => { console.error('Communication error occurred: ', e); });
```

Output

```
> node test-server.js
IPC listening on /tmp/crocket-test.sock
```


### Options

All available options for server.listen

**Server**
```json
{
	"path": "/tmp/node-ipc.sock",
	"host": null,
	"port": null,
	"reconnect": 2000,
	"encoding": "utf8"
}
```

All available options for client.connect

**Client**
```json
{
	"path": "/tmp/node-ipc.sock",
	"host": null,
	"port": null,
	"reconnect": -1,
	"timeout": 5000,
	"encoding": "utf8"
}
```

**Path** is a file-socket path, normalized by [xpipe](https://www.npmjs.com/package/xpipe). As an example, ```/tmp/my.sock``` is unchanged on Linux/OS X, while it is transformed to ```//./pipe/tmp/my.sock``` on Windows.

**Port** is specified if you want to use TCP instead of file sockets.

**Host** Only used in TCP mode. For server, ```0.0.0.0``` makes crocket listen on any IPv4-interface. ```::``` Is the equivalent for IPv6. For client, you specify the host address.

**Reconnect** is the number of milliseconds to wait before reviving a broken listener/connection, or -1 to disable automtic revive.

**Encoding** the encoding used by the underlaying sockets, in most cases this should be left at default.


# License

MIT
