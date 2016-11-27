import json
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings


class ChatterBotViewMixin(object):
    """
    Subclass this mixin for access to the 'chatterbot' attribute.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def validate(self, data):
        """
        Validate the data recieved from the client.

        * The data should contain a text attribute.
        """
        from django.core.exceptions import ValidationError

        if 'text' not in data:
            raise ValidationError('The attribute "text" is required.')


class ChatterBotView(ChatterBotViewMixin, View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    def _serialize_conversation(self, session):
        if session.conversations.empty():
            return []

        conversation = []

        for statement, response in session.conversations:
            conversation.append([statement.serialize(), response.serialize()])

        return conversation

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        """

        if request.is_ajax():
            input_data = json.loads(request.read().decode('utf-8'))
        else:
            input_data = json.loads(request.body.decode('utf-8'))

        self.validate(input_data)

        chat_session_id = request.session.get('chat_session_id')
        if chat_session_id:
            session = self.chatterbot.conversation_sessions.get(chat_session_id)
        else:
            session = self.chatterbot.conversation_sessions.new()
            request.session['chat_session_id'] = str(session.uuid)

        response_data = self.chatterbot.get_response(input_data)

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        chat_session_id = request.session.get('chat_session_id')
        if chat_session_id:
            session = self.chatterbot.conversation_sessions.get(chat_session_id)
        else:
            session = self.chatterbot.conversation_sessions.new()
            request.session['chat_session_id'] = str(session.uuid)

        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': self.chatterbot.name,
            'conversation': self._serialize_conversation(chat_session_id)
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def patch(self, request, *args, **kwargs):
        """
        The patch method is not allowed for this endpoint.
        """
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def delete(self, request, *args, **kwargs):
        """
        The delete method is not allowed for this endpoint.
        """
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)
