# This file is a part of FileStreamBot


from .. import config_dict
from hydrogram import Client

if config_dict['SECONDARY']:
    plugins=None
    no_updates=True
else:    
    plugins={"root": "WebStreamer/bot/plugins"}
    no_updates=None

StreamBot = Client(
    name="WebStreamer",
    api_id=config_dict['API_ID'],
    api_hash=config_dict['API_HASH'],
    workdir="WebStreamer",
    plugins=plugins,
    bot_token=config_dict['BOT_TOKEN'],
    sleep_threshold=config_dict['SLEEP_THRESHOLD'],
    workers=config_dict['WORKERS'],
    no_updates=no_updates
)


