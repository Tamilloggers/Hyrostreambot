# Code optimized by fyaz05
# Code from SpringsFern

from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from WebStreamer import config_dict

class Language:
    def __new__(cls, message: Message):
        user_language = getattr(message.from_user, 'language_code', 'en')
        if user_language in cls.available:
            return getattr(cls, user_language, cls.en)
        return cls.en

    available = ['en', 'language_code']

    class en:
        START_TEXT: str = """
👋 <i>Hey,</i> {}\n
<i>I'm your friendly Telegram Files Streaming Bot & Direct Links Generator.</i>\n
<i>Click on Help to get more information.</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.
        """

        HELP_TEXT: str = """
📁 <i>Send me any file or media from Telegram.</i>\n
🔗 <i>I will provide an external direct download & streaming link!</i>\n
🚀 <i>Download Link With the Fastest Speed</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.\n
👨‍💻 <i>Contact the developer or report bugs:</i> <b><a href='https://t.me/{}'>[ CLICK HERE ]</a></b>
        """

        ABOUT_TEXT: str = """
📕 <b>My Name:</b> File To Link Generator | File Streamer\n
🔹 <b>Check Commands for more details</b>
        """

        STREAM_MSG_TEXT: str = """
<i><u>Your Link is Generated!</u></i> 🎉\n
📂 <b>File Name:</b> <i>{}</i>\n
💾 <b>File Size:</b> <i>{}</i>\n
⬇️ <b>Download:</b> <i>{}</i>\n
📺 <b>Watch:</b> <i>{}</i>\n
🔗 <b>Link Generated Using:</b> <a href='https://t.me/{}'>{}</a>
        """

        BAN_TEXT: str = """
🚫 <b>Sorry, you are banned from using me.</b>\n
👨‍💻 <i>Contact the developer for help:</i> <b><a href='tg://user?id={}'>{}</a></b>
        """

        LINK_LIMIT_EXCEEDED: str = """
🚫 <b>You have exceeded the number of links you can generate.</b>\n
👨‍💻 <i>Contact the developer for help:</i> <b><a href='tg://user?id={}'>{}</a></b>
        """

        INFO_TEXT: str = """
ℹ️ <b>User ID:</b> <code>{}</code>\n
🚀 <b>Plan:</b> <code>{}</code>\n
🔗 <b>Links Used:</b> <code>{}</code>\n
🔗 <b>Links Left:</b> <code>{}</code>
        """

    class language_code:
        START_TEXT: str = """
👋 <i>Hey,</i> {}\n
<i>I'm your friendly Telegram Files Streaming Bot & Direct Links Generator.</i>\n
<i>Click on Help to get more information.</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.
        """

        HELP_TEXT: str = """
📁 <i>Send me any file or media from Telegram.</i>\n
🔗 <i>I will provide an external direct download link!</i>\n
🚀 <i>Download Link With the Fastest Speed</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.\n
👨‍💻 <i>Contact the developer or report bugs:</i> <b><a href='https://t.me/{}'>[ CLICK HERE ]</a></b>
        """

        ABOUT_TEXT: str = """
📕 <b>My Name:</b> File To Link Generator | File Streamer\n
🔹 <b>Check Commands for more details</b>
        """

        STREAM_MSG_TEXT: str = """
<i><u>Your Link is Generated!</u></i> 🎉\n
📂 <b>File Name:</b> <i>{}</i>\n
💾 <b>File Size:</b> <i>{}</i>\n
⬇️ <b>Download:</b> <i>{}</i>\n
📺 <b>Watch:</b> <i>{}</i>
        """

        BAN_TEXT: str = """
🚫 <b>Sorry, you are banned from using me.</b>\n
👨‍💻 <i>Contact the developer for help:</i> <b><a href='tg://user?id={}'>{}</a></b>
        """



default_desp = {
    'MULTI_CLIENT': 'If you Added Multi Client Make It True Else Be False,',
    'API_ID': 'This is to authenticate your Telegram account for downloading Telegram files. You can get this from https://my.telegram.org.',
    'API_HASH': 'This is to authenticate your Telegram account for downloading Telegram files. You can get this from https://my.telegram.org.',
    'BOT_TOKEN': 'The token for your Telegram bot. You can get this from the BotFather on Telegram.',
    'SLEEP_THRESHOLD': 'Time in seconds the bot will wait between operations to avoid hitting API limits. Default is 60 seconds.',
    'WORKERS': 'Number of workers to handle commands concurrently. Default is 6 workers.',
    'BIN_CHANNEL': 'Channel ID where files will be posted. Required if using MULTI_CLIENT.',
    'PORT': 'Port number for the web server. Default is 8080.',
    'BIND_ADDRESS': 'Address to which the web server will bind. Default is "0.0.0.0" to accept connections from any IP.',
    'PING_INTERVAL': 'Interval in seconds for pinging the server to keep the connection alive. Default is 1200 seconds (20 minutes).',
    'HAS_SSL': 'Whether to use SSL for HTTPS connections. Set to True if using SSL, False otherwise.',
    'NO_PORT': 'Whether to omit the port in the URL. Set to True if not using a port, False otherwise.',
    'FQDN': 'Fully Qualified Domain Name for the server. Defaults to BIND_ADDRESS if not provided.',
    'URL': 'Base URL for the server, including the protocol (http/https) and port if applicable.',
    'DATABASE_URL': 'Connection URL for the MongoDB database.',
    'UPDATES_CHANNEL': 'Channel name for updates. Default is "Telegram".',
    'OWNER_ID': 'Telegram user ID of the bot owner.',
    'SESSION_NAME': 'Name for the bot session. Default is "hydroBot".',
    'FORCE_UPDATES_CHANNEL': 'Force the bot to use updates from a specific channel. Set to True if required, False otherwise.',
    'ALLOWED_USERS': 'List of allowed user IDs for the bot, comma-separated. Any user not in this list will be denied access.',
    'KEEP_ALIVE': 'Whether to keep the bot running continuously. Set to True to keep alive, False otherwise.',
    'IMAGE_FILEID': 'URL of the image used as the bot’s profile picture or default image.',
    'TOS': 'URL of the Terms of Service document. If provided, it will be fetched and used.',
    'MODE': 'Operational mode of the bot. Defaults to "primary". Set to "secondary" if operating in secondary mode.',
    'SECONDARY': 'Whether the bot is running in secondary mode. True if MODE is "secondary", False otherwise.',
    'LINK_LIMIT': 'Maximum number of files a user can link. If not set, there is no limit.'
}


class BUTTON(object):
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('📄 About', callback_data='about'),
            InlineKeyboardButton('❌ Close', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{config_dict['UPDATES_CHANNEL']}')]
    ])

    HELP_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('📄 About', callback_data='about'),
            InlineKeyboardButton('❌ Close', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{config_dict['UPDATES_CHANNEL']}')]
    ])

    ABOUT_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('❌ Close', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{config_dict['UPDATES_CHANNEL']}')]
    ])