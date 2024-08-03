# This file is a part of FileStreamBot


import time
from urllib import request
from os import environ
from dotenv import dotenv_values
from logging import getLogger
import motor.motor_asyncio

__version__ = "2.5.0"
StartTime = time.time()

LOGGER = getLogger(__name__)

multi_clients = {}
work_loads = {}

BOT_TOKEN = str(environ.get("BOT_TOKEN", ""))
if len(BOT_TOKEN) == 0:
    BOT_TOKEN = ""

bot_id = BOT_TOKEN.split(':', 1)[0]


DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = ''

if DATABASE_URL:
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    db = client.hydro
    current_config = dict(dotenv_values('config.env'))
    old_config = db.settings.deployConfig.find_one({'_id': bot_id})
    if old_config is None:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    else:
        del old_config['_id']
    if old_config and old_config != current_config:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    elif config_dict := db.settings.config.find_one({'_id': bot_id}):
        del config_dict['_id']
        for key, value in config_dict.items():
            environ[key] = str(value)
    if pf_dict := db.settings.files.find_one({'_id': bot_id}):
        del pf_dict['_id']
        for key, value in pf_dict.items():
            if value:
                file_ = key.replace('__', '.')
                with open(file_, 'wb+') as f:
                    f.write(value)
    client.close()
    BOT_TOKEN = environ.get('BOT_TOKEN', '')
    bot_id = BOT_TOKEN.split(':', 1)[0]
    DATABASE_URL = environ.get('DATABASE_URL', '')
else:
    config_dict = {}

MULTI_CLIENT = False

API_ID = int(environ.get("API_ID", ""))
if API_ID == 0:
    API_ID = 24826284

API_HASH = str(environ.get("API_HASH", ""))
if len(API_HASH) == 0:
    API_HASH = ""


SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))
if SLEEP_THRESHOLD == 0:
    SLEEP_THRESHOLD = 60

WORKERS = int(environ.get("WORKERS", "6"))
if WORKERS == 0:
    WORKERS = 6

BIN_CHANNEL = int(environ.get("BIN_CHANNEL", ""))
if BIN_CHANNEL == 0:
    BIN_CHANNEL = ""

PORT = int(environ.get("PORT", 8080))
if PORT == 0:
    PORT = 8080

BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
if len(BIND_ADDRESS) == 0:
    BIND_ADDRESS = "0.0.0.0"

PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
if PING_INTERVAL == 0:
    PING_INTERVAL = 1200

HAS_SSL = str(environ.get("HAS_SSL", "0").lower()) in ("1", "true", "t", "yes", "y")
NO_PORT = str(environ.get("NO_PORT", "0").lower()) in ("1", "true", "t", "yes", "y")

FQDN = str(environ.get("FQDN", BIND_ADDRESS))
if len(FQDN) == 0:
    FQDN = BIND_ADDRESS

URL = "http{}://{}{}/".format("s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT))


UPDATES_CHANNEL = str(environ.get('UPDATES_CHANNEL', "Telegram"))
if len(UPDATES_CHANNEL) == 0:
    UPDATES_CHANNEL = "Telegram"

OWNER_ID = int(environ.get('OWNER_ID', ''))
if OWNER_ID == 0:
    OWNER_ID = 7136104373

SESSION_NAME = str(environ.get('SESSION_NAME', 'hydroBot'))
if len(SESSION_NAME) == 0:
    SESSION_NAME = 'hydroBot'

FORCE_UPDATES_CHANNEL = environ.get('FORCE_UPDATES_CHANNEL', False)
FORCE_UPDATES_CHANNEL = True if str(FORCE_UPDATES_CHANNEL).lower() == "true" else False

ALLOWED_USERS = [x.strip("@ ") for x in str(environ.get("ALLOWED_USERS") or "").split(",") if x.strip("@ ")]

KEEP_ALIVE = str(environ.get("KEEP_ALIVE", "0").lower()) in ("1", "true", "t", "yes", "y")

IMAGE_FILEID = environ.get('IMAGE_FILEID', "https://deekshith.eu.org/static/MyFiles.png")
if len(IMAGE_FILEID) == 0:
    IMAGE_FILEID = "https://deekshith.eu.org/static/MyFiles.png"

TOS = environ.get("TOS", None)
if TOS:
    response = request.urlopen(TOS)
    data = response.read().decode('utf-8')
    TOS = data.strip()

MODE = environ.get("MODE", "primary")
SECONDARY = True if MODE.lower() == "secondary" else False

LINK_LIMIT = int(environ.get("LINK_LIMIT")) if "LINK_LIMIT" in environ else None
if LINK_LIMIT is None:
    LINK_LIMIT = None


config_dict=({
    'MULTI_CLIENT': MULTI_CLIENT,
    'API_ID': API_ID,
    'API_HASH': API_HASH,
    'BOT_TOKEN': BOT_TOKEN,
    'SLEEP_THRESHOLD': SLEEP_THRESHOLD,
    'WORKERS': WORKERS,
    'BIN_CHANNEL': BIN_CHANNEL,
    'PORT': PORT,
    'BIND_ADDRESS': BIND_ADDRESS,
    'PING_INTERVAL': PING_INTERVAL,
    'HAS_SSL': HAS_SSL,
    'NO_PORT': NO_PORT,
    'FQDN': FQDN,
    'URL': URL,
    'DATABASE_URL': DATABASE_URL,
    'UPDATES_CHANNEL': UPDATES_CHANNEL,
    'OWNER_ID': OWNER_ID,
    'SESSION_NAME': SESSION_NAME,
    'FORCE_UPDATES_CHANNEL': FORCE_UPDATES_CHANNEL,
    'ALLOWED_USERS': ALLOWED_USERS,
    'KEEP_ALIVE': KEEP_ALIVE,
    'IMAGE_FILEID': IMAGE_FILEID,
    'TOS': TOS,
    'MODE': MODE,
    'SECONDARY': SECONDARY,
    'LINK_LIMIT': LINK_LIMIT
})