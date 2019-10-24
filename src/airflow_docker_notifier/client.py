import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

import slackclient

logger = logging.getLogger(__name__)


@dataclass
class SectionItem:
    text: str
    display_name: Optional[str] = None

    @classmethod
    def from_raw(cls, raw):
        try:
            display_name, text = raw
        except ValueError:
            display_name = None
            text = raw[0]

        return cls(text, display_name)

    def generate_link(self):
        if self.display_name:
            return f"<{self.text}|{self.display_name}>"
        return self.text

    def render(self):
        return {"type": "mrkdwn", "text": self.generate_link()}


@dataclass
class TextSection:
    name: str
    items: List[SectionItem]

    def render(self):
        return {
            "type": "context",
            "elements": [
                SectionItem(text=self.name).render(),
                *[item.render() for item in self.items],
            ],
        }


class SlackClient:
    """Wrap the Slack API client to simplify its interface.
    """

    color_wheel = {"success": "#7CD197", "warning": "#ffd574", "failed": "#ff7373"}

    def __init__(self, client, channel):
        self.client = client
        self.channel = channel

    @classmethod
    def from_config(cls, *, api_token, channel):
        client = slackclient.SlackClient(api_token)
        return cls(client=client, channel=channel)

    def post_message(
        self, message, message_type=None, text_sections=None, mentions=None, **kwargs
    ):
        """Emit a message to the channel.

        Args:
            message: The message string to send
            links: An iterable containing links. The iterable can either contain the link directly
                as a string, or 2-tuples containing (the link, display name).
            message_type: The kind of message being emitted. If the string is recognized as a
                hex color or recognized slack color alias, it will change the color around the
                message.
        """
        blocks = [self.generate_message_section(message, mentions=mentions)]

        if text_sections:
            blocks.append({"type": "divider"})

            for text_section in text_sections:
                blocks.append(text_section.render())

        response = self.client.api_call(
            "chat.postMessage",
            channel=self.channel,
            attachments=[
                {"blocks": blocks, **self.generate_color_section(message_type)}
            ],
            fallback=message,
            **kwargs,
        )
        if response["ok"] is not True:
            logger.warning(
                'Failed to send notification for message: "%s". Reason: %s',
                message,
                response,
            )
        return response

    def generate_color_section(self, message_type: str):
        color = self.color_wheel.get(message_type)
        if color:
            return {"color": color}
        return {}

    def generate_message_section(
        self, message: str, mentions: Optional[List[str]] = None
    ) -> Dict:
        """Construct a message from different message components.

        Args:
            message: The base message to send.
            mentions: An optional list of user names (with "@") to call out in the message.

        Returns:
            The fully constructed message section.
        """
        message_components = []

        if mentions:
            message_components.append(" ".join(mentions))

        message_components.append(message)
        full_message = "\n".join(message_components)
        return {"type": "section", "text": {"type": "mrkdwn", "text": full_message}}
