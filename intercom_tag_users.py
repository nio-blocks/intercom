from nio.block.base import Block
from nio.signal.base import Signal
from nio.properties import IntProperty, StringProperty, ObjectProperty, \
    PropertyHolder
import requests


class IntercomNewMessages(Block):

    # Need: tag name, user email/id
    access_token = StringProperty(
        title="Access Token", default="[[INTERCOM_ACCESS_TOKEN]]")
    tag_name = StringProperty(title="Name of Tag", default="CrankyCustomer")
    email = StringProperty(title="User Email", default="{{ $user }}")
    user_id = StringProperty(title="User ID", default="{{ $user_id }}")

    def configure(self, context):
        super().configure(context)

    def process_signals(self, signals):
        response = self._request('post', body={
            "name": self.tag_name(),
            "users": [{"id": self.user_id()}, {"email": self.email()}],
        })
        if response.status_code != 200:
            raise Exception

    def _request(self, method='post', id=None, body=None):
        url = 'https://api.intercom.io/tags'
        kwargs = {}
        kwargs['headers'] = {
            "Authorization": "Bearer {}".format(self.access_token()),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        kwargs['json'] = body
        response = getattr(requests, method)(url, **kwargs)
        if response.status_code != 200:
            self.logger.error("Http request failed: {} {}".format(
                response, response.json()))
        self.logger.debug("Http response: {}".format(response.json()))
        return response
