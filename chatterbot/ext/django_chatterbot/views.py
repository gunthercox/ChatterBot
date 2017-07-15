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
        from chatterbot.ext.django_chatterbot.models import Phrase

        class Obj(object):
            def __init__(self):
                self.id = None
                self.statements = []

        conversation = Obj()

        chat_session_id = request.session.get('chat_session_id', None)

        statements = self.chatterbot.storage.filter(
            phrase__conversations__id=chat_session_id
        )

        phrases = Phrase.objects.filter(
            conversations__id=chat_session_id
        )

        if not phrases:
            chat_session_id = self.chatterbot.storage.create_conversation()
            request.session['chat_session_id'] = chat_session_id

        conversation.id = chat_session_id
        conversation.statements = [
            {'text': phrase.text} for phrase in phrases
        ]

        return conversation


class ChatterBotView(ChatterBotViewMixin, View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        """
        input_data = json.loads(request.read().decode('utf-8'))

        self.validate(input_data)

        conversation = self.get_chat_session(request)

        response = self.chatterbot.get_response(input_data, conversation.id)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        conversation = self.get_chat_session(request)

        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': self.chatterbot.name,
            'conversation': conversation.statements
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
