# Code optimized by fyaz05
# Code from SpringsFern
import os
import sys
import math
from WebStreamer import __version__
from WebStreamer.bot import StreamBot
from WebStreamer.server.exceptions import FileNotFound
from WebStreamer.utils.bot_utils import is_user_accepted_tos, validate_user
from WebStreamer import config_dict
from WebStreamer.utils.database import Database
from WebStreamer.utils.Translation import Language, BUTTON
from hydrogram import filters, Client
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from hydrogram.enums.parse_mode import ParseMode

db = Database()

@StreamBot.on_message(filters.command('start') & filters.private)
async def start(bot: Client, message: Message):
    lang = Language(message)
    if not await validate_user(message, lang):
        return
    await message.reply_text(
        text=lang.START_TEXT.format(message.from_user.mention),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=BUTTON.START_BUTTONS
    )

@StreamBot.on_message(filters.command("about") & filters.private)
async def about(bot, message):
    lang = Language(message)
    if not await validate_user(message, lang):
        return
    await message.reply_text(
        text=lang.ABOUT_TEXT.format(__version__),
        disable_web_page_preview=True,
        reply_markup=BUTTON.ABOUT_BUTTONS
    )

@StreamBot.on_message((filters.command('help')) & filters.private)
async def help_handler(bot, message):
    lang = Language(message)
    if not await validate_user(message, lang):
        return
    await message.reply_text(
        text=lang.HELP_TEXT.format(config_dict['UPDATES_CHANNEL']),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=BUTTON.HELP_BUTTONS
    )

# ---------------------------------------------------------------------------------------------------

@StreamBot.on_message(filters.command('myfiles') & filters.private)
async def my_files(bot: Client, message: Message):
    if not await validate_user(message):
        return
    user_files, total_files = await db.find_files(message.from_user.id, [1, 10])
    file_list = []

    async for x in user_files:
        file_list.append([InlineKeyboardButton(x["file_name"], callback_data=f"myfile_{x['_id']}_1")])

    if total_files > 10:
        file_list.append([
            InlineKeyboardButton("<<", callback_data="N/A"),
            InlineKeyboardButton(f"1/{math.ceil(total_files / 10)}", callback_data="N/A"),
            InlineKeyboardButton(">>", callback_data="userfiles_2")
        ])
    
    if not file_list:
        file_list.append([InlineKeyboardButton("Empty", callback_data="N/A")])
    
    await message.reply_photo(
        photo=config_dict['IMAGE_FILEID'],
        caption="Total files: {}".format(total_files),
        reply_markup=InlineKeyboardMarkup(file_list)
    )

@StreamBot.on_message(filters.command('tos') & filters.private)
async def tos_handler(bot: Client, message: Message):
    if not config_dict['TOS']:
        await message.reply_text("This bot does not have any terms of service.")
        return
    if await is_user_accepted_tos(message):
        await message.reply_text(
            config_dict['TOS'],
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ I accepted the TOS", callback_data="N/A")]])
        )

@StreamBot.on_message(filters.command('info') & filters.private)
async def info_handler(bot: Client, message: Message):
    lang = Language(message)
    if not await validate_user(message, lang):
        return
    i_cmd = message.text.split()
    if (message.from_user.id == config_dict['OWNER_ID']) and (len(i_cmd) > 1):
        message.from_user.id = int(i_cmd[1])
    user = await db.get_user(message.from_user.id)
    files = await db.total_files(message.from_user.id)
    links = "N/A"
    if (user.get("Plan") == "Free") and (config_dict['LINK_LIMIT']):
        links = config_dict['LINK_LIMIT'] - files
    await message.reply_text(lang.INFO_TEXT.format(message.from_user.id, user.get("Plan"), files, links))

@StreamBot.on_message(filters.command('getfile') & filters.private & filters.user(config_dict['OWNER_ID']))
async def getfile(bot: Client, message: Message):
    if not await validate_user(message):
        return
    usr_cmd = message.text.split()
    if len(usr_cmd) < 2:
        return await message.reply_text("Invalid Format\nUsage: `/getfile _id`")
    for x in usr_cmd[1:]:
        try:
            myfile = await db.get_file(x)
            await message.reply_cached_media(myfile['file_id'])
        except FileNotFound:
            await message.reply_text(f"{x} :File Not Found")

@StreamBot.on_message(filters.command('restart') & filters.user(config_dict['OWNER_ID']))
async def restart(client, message):
    reply = await message.reply_text('Restarting...')
    try:
        textx = "Done Restart...✅"
        await reply.edit_text(textx)
       
        os.execl(sys.executable, sys.executable, "-m", "WebStreamer")
    except Exception as e:
        await reply.edit_text(f"Failed to restart: {e}")
        logging.error(f"Failed to restart: {traceback.format_exc()}")
