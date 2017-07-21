from nio.block.base import Block
from nio.properties import StringProperty
import requests


class IntercomTagUsers(Block):

    access_token = StringProperty(
        title="Access Token", default="[[INTERCOM_ACCESS_TOKEN]]")
    tag_name = StringProperty(title="Name of Tag", default="HappyCustomer")
    email = StringProperty(title="User Email", default="{{ $user }}")

    def process_signals(self, signals):
        for signal in signals:
            response = self._request(body={
                "name": self.tag_name(signal),
                "users": [{"email": self.email(signal)}],
            })
            if response.status_code != 200:
                raise Exception

    def _request(self, body={}):
        url = 'https://api.intercom.io/tags'
        kwargs = {}
        kwargs['headers'] = {
            "Authorization": "Bearer {}".format(self.access_token()),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        kwargs['json'] = body
        response = getattr(requests, 'post')(url, **kwargs)
        if response.status_code != 200:
            self.logger.error("Http request failed: {} {}".format(
                response, response.json()))
        self.logger.debug("Http response: {}".format(response.json()))
        return response
