from nio import TerminatorBlock
from nio.properties import StringProperty, PropertyHolder, ObjectProperty, \
    VersionProperty
import requests


class UserInfo(PropertyHolder):
    email = StringProperty(
        title="User Email", default="{{ $user }}", allow_none=True)
    id = StringProperty(
        title="ID", default="{{ $user_id }}", allow_none=True)


class IntercomTagUsers(TerminatorBlock):

    version = VersionProperty("1.0.0")
    access_token = StringProperty(
        title="Access Token", default="[[INTERCOM_ACCESS_TOKEN]]")
    tag_name = StringProperty(title="Name of Tag", default="HappyCustomer")
    user_info = ObjectProperty(UserInfo, title="User Info", default=UserInfo())

    def process_signals(self, signals):
        for signal in signals:
            if self.user_info().email(signal) or self.user_info().id(signal):
                response = self._request(body={
                    "name": self.tag_name(signal),
                    "users": [
                        {"email": self.user_info().email(signal)}
                    ]
                    if self.user_info().email(signal) else [
                        {"id": self.user_info().id(signal)}
                    ]
                })
                if response.status_code != 200:
                    raise Exception
            else:
                self.logger.error("No user info configured")
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
