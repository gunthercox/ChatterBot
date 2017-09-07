let client = {}
let request = require("request");
let baseUrl = "http://localhost:8888";

client.Ask = function(message, fn) {
	let ask = {
		url: baseUrl + "/ask",
		method: "post",
		body: JSON.stringify({message: message}),
	}
	request(ask, function(err, resp) {
		if (err) {
			console.log("error ", err);
			return fn(err);
		}
		return fn(null, resp.body);
	});
}


client.Train = function(convo, fn) {
		let train = {
			url: baseUrl + "/train",
			method: "post",
		}
		let train_data = {
			convo: convo
		}
		train.body = JSON.stringify(train_data);
		request(train, function(err, done) {
			if (err) {
				console.log("error" ,err);
			}
			return fn(err, done);
		});
}

module.exports = client;

