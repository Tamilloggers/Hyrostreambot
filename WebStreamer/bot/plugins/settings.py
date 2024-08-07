from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from hydrogram.enums import ChatType
from hydrogram.filters import command, regex, create
from hydrogram.handlers import MessageHandler
from aiofiles.os import path as aiopath
from asyncio import sleep,create_subprocess_exec, create_subprocess_shell
from functools import partial
from collections import OrderedDict
from io import BytesIO
from os import environ
from urllib import request
from time import time

from hydrogram import filters, Client

from WebStreamer import config_dict
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.Translation import default_desp

START = 0
handler_dict = {}
STATE = 'view'


default_values = {'WORKERS': 6,
                  'SLEEP_THRESHOLD':60,
                  'SESSION_NAME':'hydrobot',
                  'PING_INTERVAL':1200,}


bool_vars = ['HAS_SSL','NO_PORT','FORCE_UPDATES_CHANNEL','KEEP_ALIVE']


MULTI_CLIENT = False

API_ID = int(environ.get("API_ID", ""))
if API_ID == 0:
    API_ID = ""

API_HASH = str(environ.get("API_HASH", ""))
if len(API_HASH) == 0:
    API_HASH = ""

BOT_TOKEN = str(environ.get("BOT_TOKEN", ""))
if len(BOT_TOKEN) == 0:
    BOT_TOKEN = ""

SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))
if SLEEP_THRESHOLD == 0:
    SLEEP_THRESHOLD = 60

WORKERS = int(environ.get("WORKERS", "6"))
if WORKERS == 0:
    WORKERS = 6

BIN_CHANNEL = int(environ.get("BIN_CHANNEL", ""))
if BIN_CHANNEL == 0:
    BIN_CHANNEL = -1002233287339

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

DATABASE_URL = str(environ.get('DATABASE_URL', ""))
if len(DATABASE_URL) == 0:
    DATABASE_URL = ""

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

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', 'https://github.com/Tamilloggers/Hyrostreambot')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = 'https://github.com/Tamilloggers/Hyrostreambot'

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'master')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'master'

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
    'LINK_LIMIT': LINK_LIMIT,
    'UPSTREAM_REPO': UPSTREAM_REPO,
    'UPSTREAM_BRANCH': UPSTREAM_BRANCH,
})
if DATABASE_URL:
    await Database().update_config(config_dict)


async def get_list(key=None, edit_type=None,edit_mode=None, mess=None):
    keyboard=[]
    if key is None:
        keyboard.append([InlineKeyboardButton("Config Variables",callback_data="botset var")])
        keyboard.append([InlineKeyboardButton("Close",callback_data="botset close")])
        msg = "Bot Settings:"
    elif key == 'var':
        for k in list(OrderedDict(sorted(config_dict.items())).keys())[START:10+START]:
            keyboard.append([InlineKeyboardButton(k,callback_data=f"botset editvar {k}")])
        keyboard.append([InlineKeyboardButton("Back",callback_data="botset back")])
        keyboard.append([InlineKeyboardButton("Close",callback_data="botset close")])
        for x in range(0, len(config_dict)-1, 10):
            keyboard.append([InlineKeyboardButton(f'{int(x/10)}', callback_data=f"botset start var {x}")])
        msg = f'Config Variables | Page: {int(START/10)}'
    elif edit_type == 'editvar':
        msg = f'<b>Variable:</b> <code>{key}</code>\n\n'
        msg += f'<b>Description:</b> {default_desp.get(key, "No Description Provided")}\n\n'
        if mess.chat.type == ChatType.PRIVATE:
            msg += f'<b>Value:</b> <spoiler> {config_dict.get(key, "None")} </spoiler>\n\n'
        else:
            keyboard.append([InlineKeyboardButton('View Var Value',callback_data=f"botset showvar {key}")])
        keyboard.append([InlineKeyboardButton('Back', callback_data="botset back var")])
        if key not in bool_vars:
            if not edit_mode:
                keyboard.append([InlineKeyboardButton('Edit Value', callback_data=f"botset editvar {key} edit")])
            else:
                keyboard.append([InlineKeyboardButton('Stop Edit', callback_data=f"botset editvar {key}")])
        if key not in ['API_ID','API_HASH','BOT_TOKEN','OWNER_ID']  and key not in bool_vars:
            keyboard.append([InlineKeyboardButton('Reset', callback_data=f"botset resetvar {key}")])
        keyboard.append([InlineKeyboardButton('Close', callback_data="botset close")])
        if edit_mode and key in ['ALLOWED_USERS','KEEP_ALIVE','IMAGE_FILEID','MODE','LINK_LIMIT','NO_PORT','FQDN','PORT','BIN_CHANNEL']:
            msg += '<b>Note:</b> Restart required for this edit to take effect!\n\n'
        if edit_mode and key not in bool_vars:
            msg += '<i>Send a valid value for the above config_dict </i> <b>Timeout:</b> 60 sec'
        if key in bool_vars:
            msg += '<i>Choose a valid value for the above Var</i>'
            keyboard.append([InlineKeyboardButton('True', callback_data=f"botset boolvar {key} on")])
            keyboard.append([InlineKeyboardButton('False', callback_data=f"botset boolvar {key} off")])

    return msg, keyboard

async def update_buttons(message, key=None, edit_type=None, edit_mode=None):
    msg, button = await get_list(key, edit_type, edit_mode, message)
    await message.edit(message, msg, button)


async def edit_variable(_, message, pre_message, key):
    handler_dict[message.chat.id] = False
    value = message.text
    if key in ['SLEEP_THRESHOLD','WORKERS','BIN_CHANNEL','PORT',]:
        value = int(value)
    config_dict[key] = value
    await update_buttons(pre_message, key, 'editvar', False)
    await message.delete()
    if DATABASE_URL:
        await Database().update_config({key: value})




async def event_handler(client, query, pfunc, rfunc, document=False):
    chat_id = query.message.chat.id
    handler_dict[chat_id] = True
    start_time = time()

    async def event_filter(_, __, event):
        user = event.from_user or event.sender_chat
        return bool(user.id == query.from_user.id and event.chat.id == chat_id and (event.text or event.document and document))
    handler = client.add_handler(MessageHandler(
        pfunc, filters=create(event_filter)), group=-1)
    while handler_dict[chat_id]:
        await sleep(0.5)
        if time() - start_time > 60:
            handler_dict[chat_id] = False
            await rfunc()
    client.remove_handler(*handler)

@StreamBot.on_message(filters=regex("^botset") & filters.user(config_dict['OWNER_ID']))
async def edit_bot_settings(client, query):
    data = query.data.split()
    message = query.message
    if data[1] == 'close':
        handler_dict[message.chat.id] = False
        await query.answer()
        await message.delete()
        await message.reply_to_message.delete()
    elif data[1] == 'back':
        handler_dict[message.chat.id] = False
        await query.answer()
        key = data[2] if len(data) == 3 else None
        if key is None:
            globals()['START'] = 0
        await update_buttons(message, key)
    elif data[1] in ['var']:
        await query.answer()
        await update_buttons(message, data[1])
    elif data[1] == 'resetvar':
        handler_dict[message.chat.id] = False
        await query.answer('Reset Done!', show_alert=True)
        value = ''
        if data[2] in default_values:
            value = default_values[data[2]]
    elif data[1] == 'boolvar':
        handler_dict[message.chat.id] = False
        value = data[3] == "on"
        await query.answer(f'Successfully Var changed to {value}!', show_alert=True)
        config_dict[data[2]] = value
        await update_buttons(message, data[2], 'editvar', False)
        if DATABASE_URL:
            await Database().update_config({data[2]: value})

    elif data[1] == 'editvar':
        handler_dict[message.chat.id] = False
        await query.answer()
        edit_mode = len(data) == 4
        await update_buttons(message, data[2], data[1], edit_mode)
        if data[2] in bool_vars or not edit_mode:
            return
        pfunc = partial(edit_variable, pre_message=message, key=data[2])
        rfunc = partial(update_buttons, message, data[2], data[1], edit_mode)
        await event_handler(client, query, pfunc, rfunc)
    elif data[1] == 'showvar':
        value = config_dict[data[2]]
        if len(str(value)) > 200:
            await query.answer()
            with BytesIO(str.encode(value)) as out_file:
                out_file.name = f"{data[2]}.txt"
                await client.send_document(message, out_file)
            return
        elif value == '':
            value = None
        await query.answer(f'{value}', show_alert=True)

    elif data[1] == 'edit':
        await query.answer()
        globals()['STATE'] = 'edit'
        await update_buttons(message, data[2])
    elif data[1] == 'view':
        await query.answer()
        globals()['STATE'] = 'view'
        await update_buttons(message, data[2])
    elif data[1] == 'start':
        await query.answer()
        if START != int(data[3]):
            globals()['START'] = int(data[3])
            await update_buttons(message, data[2])

    elif data[1] == 'push':
        await query.answer()
        filename = data[2].rsplit('.zip', 1)[0]
        if await aiopath.exists(filename):
            await (await create_subprocess_shell(f"git add -f {filename} \
                                                   && git commit -sm botsettings -q \
                                                   && git push origin {config_dict['UPSTREAM_BRANCH']} -qf")).wait()
        else:
            await (await create_subprocess_shell(f"git rm -r --cached {filename} \
                                                   && git commit -sm botsettings -q \
                                                   && git push origin {config_dict['UPSTREAM_BRANCH']} -qf")).wait()
        await message.delete()
        await message.reply_to_message.delete()

@StreamBot.on_message(filters.command("settings") & filters.user(config_dict['OWNER_ID']))
async def bot_settings(client, message):
    msg, button = await get_list()
    globals()['START'] = 0
    await client.send_message(message, msg, button)
