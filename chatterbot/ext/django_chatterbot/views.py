from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from chatterbot import ChatBot


class ChatterBotView(View):

    chatterbot = ChatBot(
        settings.CHATTERBOT['NAME'],
        storage_adapter='chatterbot.adapters.storage.DjangoStorageAdapter',
        input_adapter='chatterbot.adapters.input.VariableInputTypeAdapter',
        output_adapter='chatterbot.adapters.output.OutputFormatAdapter',
        output_format='json'
    )

    def post(self, request, *args, **kwargs):
        input_statement = request.POST.get('text')

        response_data = self.chatterbot.get_response(input_statement)

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def patch(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def delete(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

