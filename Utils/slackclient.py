from slack import WebClient


class Slack:
    """
    Class to connect and post messages to Slack, if a token isn't provided
    then it will authorise as a bot
    """
    def __init__(self, channel, token=None):
        self.webclient = WebClient(token if token else 'xoxb-3442381301-3212766763911-EskLnjIW9BAoclU4ml959Xpw')
        self.channel = channel

    def post_message(self, message: str, mention: str = None, attachments: list = None, thread: int = None) -> dict:
        """Posts message to specified channel, optional mention"""
        return self.webclient.chat_postMessage(
            channel=self.channel,
            link_names=1 if mention else 0,
            text=f"<@{mention}> {message}" if mention else message,
            attachments=attachments,
            thread_ts=thread
        )

    def upload_file(self, filepath: str, title: str, thread: int = None) -> dict:
        """Upload file to the channel"""
        return self.webclient.files_upload(
            file=filepath,
            channels=self.channel,
            title=title,
            thread_ts=thread
        )

    def post_blocks(self, blocks: list, thread: int = None) -> dict:
        """Post blocks to specified Slack channel"""
        return self.webclient.chat_postMessage(
            channel=self.channel,
            blocks=blocks,
            thread_ts=thread
        )


class BlockMaker:
    """Creates blocks to post messages in the new style for Slack"""
    @staticmethod
    def create_text_block(text: str, fields: list = None) -> dict:
        """Creates block with simple text, fields can be added as an array of strings"""
        block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }

        if fields:
            block['fields'] = []
            for field in fields:
                block['fields'].append(
                    {
                        'type': 'mrkdwn',
                        'text': field
                    }
                )
        return block

    @staticmethod
    def create_context_block(text: str) -> dict:
        """Creates small context block with text provided"""
        return {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": text
                }
            ]
        }

    @staticmethod
    def create_header_block(text: str) -> dict:
        """Creates a header block with text provided"""
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": True
            }
        }

    @staticmethod
    def get_divider() -> dict:
        """Divider block"""
        return {"type": "divider"}

    @staticmethod
    def split(blocks: list) -> list:
        """Splits the blocks up so we don't go over the Slack limit"""
        block_sets = []
        tmp_set = []
        for block in blocks:
            if len(tmp_set) + len(block) > 50:
                block_sets.append(tmp_set)
                tmp_set = []
            tmp_set.extend(block)
        block_sets.append(tmp_set)
        return block_sets
