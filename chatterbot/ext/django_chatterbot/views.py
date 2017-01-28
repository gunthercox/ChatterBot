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

    def get_conversation(self, request):
        """
        Return the current conversation for the chat if one exists.
        Create a new conversation if one does not exist.
        """
        conversation_id = request.session.get('chat_conversation_id', None)
        conversation = self.chatterbot.conversations.get(conversation_id, None)

        if not conversation:
            conversation = self.chatterbot.conversations.create()
            request.session['chat_conversation_id'] = conversation.id

        return conversation


class ChatterBotView(ChatterBotViewMixin, View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    def _serialize_conversation(self, conversation):
        statements = []

        for statement in conversation.statements.all():
            statements.append(statement.serialize())

        return statements

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        """
        input_data = json.loads(request.read().decode('utf-8'))

        self.validate(input_data)

        # Convert the extra_data to a string to be stored by the Django model
        if 'extra_data' in input_data:
            extra_data = input_data['extra_data']
            input_data['extra_data'] = json.dumps(extra_data)

        conversation = self.get_conversation(request)

        response = self.chatterbot.get_response(input_data, conversation.id)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        conversation = self.get_conversation(request)

        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': self.chatterbot.name,
            'conversation': self._serialize_conversation(conversation)
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
