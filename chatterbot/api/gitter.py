import re
import logging
import requests


GITTER_HOST = 'https://api.gitter.im/v1/'


logger = logging.getLogger(__name__)


class HTTPStatusException(Exception):
    """
    Exception raised when unexpected non-success HTTP
    status codes are returned in a response.
    """
    pass


def get_request_headers(access_token):
    return {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }


def remove_mentions(text):
    """
    Return a string that has no leading mentions.
    """
    text_without_mentions = re.sub(r'@\S+', '', text)

    # Remove consecutive spaces
    text_without_mentions = re.sub(' +', ' ', text_without_mentions.strip())

    return text_without_mentions


def _validate_status_code(response):
    code = response.status_code
    if code not in [200, 201]:
        raise HTTPStatusException('{} status code received'.format(code))


def join_room(access_token, room_name):
    """
    Join the specified Gitter room.
    """
    endpoint = '{}rooms'.format(GITTER_HOST)
    response = requests.post(
        endpoint,
        headers=get_request_headers(access_token),
        json={'uri': room_name}
    )
    logger.info('{} joining room {}'.format(
        response.status_code, endpoint
    ))
    _validate_status_code(response)
    return response.json()


def get_user_data(access_token):
    endpoint = '{}user'.format(GITTER_HOST)
    response = requests.get(
        endpoint,
        headers=get_request_headers(access_token)
    )
    logger.info('{} retrieving user data {}'.format(
        response.status_code, endpoint
    ))
    _validate_status_code(response)
    return response.json()


def mark_messages_as_read(access_token, user_id, room_id, message_ids):
    """
    Mark the specified message ids as read.
    """
    endpoint = '{}user/{}/rooms/{}/unreadItems'.format(
        GITTER_HOST, user_id, room_id
    )
    response = requests.post(
        endpoint,
        headers=get_request_headers(access_token),
        json={'chat': message_ids}
    )
    logger.info('{} marking messages as read {}'.format(
        response.status_code, endpoint
    ))
    _validate_status_code(response)
    return response.json()


def get_most_recent_message(access_token, room_id):
    """
    Get the most recent message from the Gitter room.
    """
    endpoint = '{}rooms/{}/chatMessages?limit=1'.format(GITTER_HOST, room_id)
    response = requests.get(
        endpoint,
        headers=get_request_headers(access_token)
    )
    logger.info('{} getting most recent message'.format(
        response.status_code
    ))
    _validate_status_code(response)
    data = response.json()
    if data:
        return data[0]
    return None


def _contains_mention(mentions, username):
    for mention in mentions:
        if username == mention.get('screenName'):
            return True
    return False


def should_respond(data, username, only_respond_to_mentions):
    """
    Takes the API response data from a single message.
    Returns true if the chat bot should respond.
    """
    if data:
        unread = data.get('unread', False)

        if only_respond_to_mentions:
            if unread and _contains_mention(data['mentions'], username):
                return True
            else:
                return False
        elif unread:
            return True

    return False


def send_message(access_token, room_id, text):
    """
    Send a message to a Gitter room.
    """
    endpoint = '{}rooms/{}/chatMessages'.format(GITTER_HOST, room_id)
    response = requests.post(
        endpoint,
        headers=get_request_headers(access_token),
        json={'text': text}
    )
    logger.info('{} sending message to {}'.format(
        response.status_code, endpoint
    ))
    _validate_status_code(response)
    return response.json()
