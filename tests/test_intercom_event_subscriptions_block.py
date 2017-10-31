import json
from unittest.mock import MagicMock, patch

import responses

from nio.testing.block_test_case import NIOBlockTestCase
from ..intercom_event_subscriptions_block import \
    IntercomEventSubscriptions, BuildSignal


class TestBuildSignal(NIOBlockTestCase):

    def test_web_handler_post_dict(self):
        notify_signals = MagicMock()
        handler = BuildSignal(endpoint='',
                              notify_signals=notify_signals,
                              logger=MagicMock())
        request = MagicMock()
        request.get_body.return_value = {"I'm a": "dictionary"}
        handler.on_post(request, MagicMock())
        self.assertDictEqual(
            notify_signals.call_args[0][0][0].to_dict(),
            {"I'm a": "dictionary"})


class TestIntercomNewMessages(NIOBlockTestCase):

    @responses.activate
    def test_block_propertes_are_passed_to_web_engine_and_handler(self):
        blk = IntercomEventSubscriptions()
        responses.add(
            responses.POST,
            'https://api.intercom.io/subscriptions',
            json={"id": "id"},
        )
        module = IntercomEventSubscriptions.__module__
        with patch("{}.WebEngine".format(module)) as engine:
            with patch("{}.BuildSignal".format(module)) as handler:
                self.configure_block(blk, {})
                engine.add_server.assert_called_once_with(
                    blk.web_server().port(),
                    blk.web_server().host(),
                )
                handler.assert_called_once_with(
                    blk.web_server().endpoint(),
                    blk.notify_signals,
                    blk.logger,
                )

    @responses.activate
    def test_subscriptions_are_created_and_destroyed(self):
        blk = IntercomEventSubscriptions()
        callback_url = "callback"
        responses.add(
            responses.POST,
            'https://api.intercom.io/subscriptions',
            json={"id": "id"},
        )
        responses.add(
            responses.DELETE,
            'https://api.intercom.io/subscriptions/id',
            json={"id": "id"},
        )
        module = IntercomEventSubscriptions.__module__
        with patch("{}.WebEngine".format(module)):
            with patch("{}.BuildSignal".format(module)):
                self.configure_block(blk, {
                    "callback_url": callback_url,
                })
        self.assertEqual(len(responses.calls), 1)
        self.assertDictEqual(
            json.loads(responses.calls[0].request.body.decode()), {
                "service_type": "web",
                "topics": ["conversation.user.created"],
                "url": blk.callback_url(),
            }
        )
        headers = responses.calls[0].request.headers
        self._assert_header_value(
            headers, "Authorization", "Bearer {}".format(blk.access_token()))
        self._assert_header_value(headers, "Accept", "application/json")
        self._assert_header_value(headers, "Content-Type", "application/json")
        blk.stop()
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_subscription_config(self):
        blk = IntercomEventSubscriptions()
        callback_url = "callback"
        topics = ['topic_a', 'topic_b']
        responses.add(
            responses.POST,
            'https://api.intercom.io/subscriptions',
            json={"id": "id"},
        )
        responses.add(
            responses.DELETE,
            'https://api.intercom.io/subscriptions/id',
            json={"id": "id"},
        )
        module = IntercomEventSubscriptions.__module__
        with patch("{}.WebEngine".format(module)):
            with patch("{}.BuildSignal".format(module)):
                self.configure_block(blk, {
                    "callback_url": callback_url,
                    "topics": topics
                })
        self.assertEqual(len(responses.calls), 1)
        self.assertDictEqual(
            json.loads(responses.calls[0].request.body.decode()), {
                "service_type": "web",
                "topics": topics,
                "url": blk.callback_url(),
            }
        )

    def _assert_header_value(self, headers, header, value):
        self.assertEqual(headers[header], value)
