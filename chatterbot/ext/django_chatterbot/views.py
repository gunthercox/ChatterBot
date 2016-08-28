from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings


class ChatterBotView(View):

    def post(self, request, *args, **kwargs):
        input_statement = request.POST.get('text')

        response_data = settings.CHATTERBOT.get_response(input_statement)

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

