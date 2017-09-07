from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from bottle import route, run, template, get, post, request
import json

chatbot = ChatBot(
	'SimpleApi')
chatbot.set_trainer(ListTrainer)
chatbot.read_only = True

@route('/train', method='POST')
def index():
	try:
		l = json.load(request.body)
		chatbot.train(l["convo"])
		return json.dumps({"trained": l["convo"]});
	except:
		pass
	return json.dump({"error": "exception"})

@route('/ask', method='POST')
def index():
	try:
		 l = json.load(request.body)
		 CONVERSATION_ID = chatbot.storage.create_conversation()
	 	 answer = chatbot.get_response(l["message"], CONVERSATION_ID)
		 return json.dumps({"message": str(answer)})
	except:
		pass
	return json.dumps({"error": "exception"})

run(host='localhost', port=8888)