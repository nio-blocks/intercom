from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal
import json
import responses
from ..intercom_tag_users_block import IntercomTagUsers


class TestIntercomTagUsers(NIOBlockTestCase):

    @responses.activate
    def test_tag_user_post_request(self):
        blk = IntercomTagUsers()
        self.configure_block(blk, {
            "access_token": "testToken",
            "tag_name": "{{ $tag }}"
        })
        blk.start()
        responses.add(
            responses.POST,
            "https://api.intercom.io/tags",
            json={
                "name": "testTag",
                "users": [{"email": "test@email.com"}]
            }
        )
        blk.process_signals([Signal({
            "user": "test@email.com",
            "tag": "testTag"
        })])
        blk.stop()
        self.assertEqual(len(responses.calls), 1)
        headers = responses.calls[0].request.headers
        self._assert_header_value(
            headers, "Authorization", "Bearer {}".format(blk.access_token()))
        self._assert_header_value(headers, "Accept", "application/json")
        self._assert_header_value(headers, "Content-Type", "application/json")
        self.assertDictEqual(
            json.loads(responses.calls[0].request.body.decode()), {
                "name": "testTag",
                "users": [{"email": "test@email.com"}],
        })

    def _assert_header_value(self, headers, header, value):
        self.assertEqual(headers[header], value)
