IntercomNewMessages
===================

Publishes a signal for each new conversation created in Intercom. When the block starts up, it creates a local web server and endpoint to receive the messages from nio. It also creates a webhook in Intercom that is configured to send to your callback url. When the block stops, it delete the webhook from Intercom.

Properties
----------
- **callback_url**(string): Your publicly accessible url that Intercom can POST notifications to.
- **access_token**(string): Your Intercom Access Token. You will need to request an [extended scope](https://developers.intercom.com/docs/personal-access-tokens#section-extended-scopes) token from Intercom.
- **web_server**(object): Host, Port and Endpoint to launch your webserver where Intercom will POST notifications to.

Dependencies
------------
requests

Output
------

```
{'delivery_attempts': 1, 'type': 'notification_event', 'created_at': 1499900215, 'links': {}, 'id': 'notif_66fdce40-6755-11e7-bd38-bdda4aa19f1b', 'topic': 'conversation.user.created', 'delivered_at': 0, 'delivery_status': 'pending', 'app_id': 'mz6gs2p0', 'first_sent_at': 1499900215, 'self': None, 'data': {'type': 'notification_event_data', 'item': {'user': {'type': 'user', 'name': 'Chris Brackert', 'email': 'cbrackert@n.io', 'user_id': '109570106748577333422', 'id': '554028790f941a3cb3000ddf'}, 'read': True, 'type': 'conversation', 'metadata': {}, 'links': {'conversation_web': 'https://app.intercom.io/a/apps/mz6gs2p0/inbox/all/conversations/10768842031'}, 'id': '10768842031', 'created_at': 1499900215, 'updated_at': 1499900215, 'open': True, 'assignee': {'type': 'nobody_admin', 'id': None}, 'conversation_message': {'attachments': [], 'body': "<p>Chris, it's me again. One more test.</p>", 'subject': '', 'type': 'conversation_message', 'author': {'type': 'user', 'id': '554028790f941a3cb3000ddf'}, 'id': '114942241'}, 'tags': {'type': 'tag.list', 'tags': []}, 'conversation_parts': {'type': 'conversation_part.list', 'total_count': 0, 'conversation_parts': []}}}}
```
