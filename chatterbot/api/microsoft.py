import logging
import requests


DIRECTLINE_HOST = 'https://directline.botframework.com'


logger = logging.getLogger(__name__)


class HTTPStatusException(Exception):
    """
    Exception raised when unexpected non-success HTTP
    status codes are returned in a response.
    """
    pass


def get_request_headers(access_token):
    return {
        'Authorization': 'BotConnector {}'.format(access_token),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'charset': 'utf-8'
    }


def _validate_status_code(response):
    code = response.status_code
    if code not in [200, 204]:
        raise HTTPStatusException('{} status code received'.format(code))


def get_most_recent_message(access_token, conversation_id):
    endpoint = '{host}/api/conversations/{id}/messages'.format(
        host=DIRECTLINE_HOST,
        id=conversation_id
    )

    response = requests.get(
        endpoint,
        headers=get_request_headers(access_token),
        verify=False
    )

    logger.info('{} retrieving most recent messages {}'.format(
        response.status_code, endpoint
    ))

    _validate_status_code(response)

    data = response.json()

    if data['messages']:
        last_msg = int(data['watermark'])
        return data['messages'][last_msg - 1]
    return None


def send_message(access_token, conversation_id, message):
    """
    Send a message to the specified conversation.
    """
    message_url = "{host}/api/conversations/{conversation_id}/messages".format(
        host=DIRECTLINE_HOST,
        conversation_id=conversation_id
    )

    response = requests.post(
        message_url,
        headers=get_request_headers(access_token),
        json={
            'message': message
        }
    )

    logger.info('{} sending message {}'.format(
        response.status_code, message_url
    ))
    _validate_status_code(response)
    # Microsoft return 204 on operation succeeded and no content was returned.
    return get_most_recent_message(access_token, conversation_id)


def start_conversation(access_token):
    endpoint = '{host}/api/conversations'.format(host=DIRECTLINE_HOST)
    response = requests.post(
        endpoint,
        headers=get_request_headers(access_token),
        verify=False
    )
    logger.info('{} starting conversation {}'.format(
        response.status_code, endpoint
    ))
    _validate_status_code(response)
    return response.json()
