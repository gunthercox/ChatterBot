var client = require(__dirname + "/client.js");
var async = require("async");

client.TrainAll = function(fn) {
	var convos = [["Hi", "Hello how are you?"],["Whats your name?", "Hal", "Are you a robot?", "Yes"]];
	async.each(convos, client.Train, function(err, done) {
		console.log("trained conversations", convos.length);
		return fn(err, done);
	});
}


client.TrainAll(function(err, done) {
	if (err) console.error(err);
	client.Ask("Hi", function(err, message) {
		if(err) console.error(err);
		console.log("got reply", message);

	});
})