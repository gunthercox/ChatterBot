'use strict';

module.exports = (socket, callback) => {
	if (socket.writable && !socket.connecting) {
		callback();
	} else {
		socket.once('connect', callback);
	}
};
