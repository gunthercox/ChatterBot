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

    def get_chat_session(self, request):
        """
        Return the current session for the chat if one exists.
        Create a new session if one does not exist.
        """
        chat_session_id = request.session.get('chat_session_id', None)
        chat_session = self.chatterbot.conversation_sessions.get(chat_session_id, None)

        if not chat_session:
            chat_session = self.chatterbot.conversation_sessions.new()
            request.session['chat_session_id'] = chat_session.id_string

        return chat_session


class ChatterBotView(ChatterBotViewMixin, View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    def _serialize_conversation(self, session):
        if session.conversation.empty():
            return []

        conversation = []

        for statement, response in session.conversation:
            conversation.append([statement.serialize(), response.serialize()])

        return conversation

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        """
        input_data = json.loads(request.read().decode('utf-8'))

        self.validate(input_data)

        chat_session = self.get_chat_session(request)

        response = self.chatterbot.get_response(input_data, chat_session.id_string)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        chat_session = self.get_chat_session(request)

        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': self.chatterbot.name,
            'conversation': self._serialize_conversation(chat_session)
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
