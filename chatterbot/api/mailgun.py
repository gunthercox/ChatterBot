import requests
import datetime


def get_email_stored_events(api_key, endpoint):
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    return requests.get(
        '{}/events'.format(endpoint),
        auth=('api', api_key),
        params={
            'begin': yesterday.isoformat(),
            'ascending': 'yes',
            'limit': 1
        }
    )


def get_stored_email_urls(api_key, endpoint):
    response = get_email_stored_events(api_key, endpoint)
    data = response.json()

    for item in data.get('items', []):
        if 'storage' in item:
            if 'url' in item['storage']:
                yield item['storage']['url']


def get_message(api_key, url):
    return requests.get(
        url,
        auth=('api', api_key)
    )


def send_message(api_key, endpoint, name, subject, text, from_address, recipients):
    """
    * subject: Subject of the email.
    * text: Text body of the email.
    * from_email: The email address that the message will be sent from.
    * recipients: A list of recipient email addresses.
    """
    return requests.post(
        endpoint,
        auth=('api', api_key),
        data={
            'from': '%s <%s>' % (name, from_address),
            'to': recipients,
            'subject': subject,
            'text': text
        }
    )
