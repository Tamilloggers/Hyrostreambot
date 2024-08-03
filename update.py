from logging import error , info 
from os import path , environ
from subprocess import run
from requests import get
from dotenv import load_dotenv, dotenv_values
import motor.motor_asyncio



load_dotenv('config.env', override=True)



BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0]

DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = None

if DATABASE_URL is not None:
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    db = client.hydro
    old_config = db.settings.deployConfig.find_one({'_id': bot_id})
    config_dict = db.settings.config.find_one({'_id': bot_id})
    if old_config is not None:
        del old_config['_id']
    if (old_config is not None and old_config == dict(dotenv_values('config.env')) or old_config is None) \
            and config_dict is not None:
        environ['UPSTREAM_REPO'] = config_dict['UPSTREAM_REPO']
        environ['UPSTREAM_BRANCH'] = config_dict['UPSTREAM_BRANCH']
    client.close()

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', 'https://github.com/Tamilloggers/Hyrostreambot')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = 'https://github.com/Tamilloggers/Hyrostreambot'

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'master')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'master'

if UPSTREAM_REPO is not None:
    if path.exists('.git'):
        run(["rm", "-rf", ".git"])

    update = run([f"git init -q \
                     && git config --global user.email doc.adhikari@gmail.com \
                     && git config --global user.name weebzone \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

    if update.returncode == 0:
        info('Successfully updated with latest commit from UPSTREAM_REPO')
    else:
        error(
            'Something went wrong while updating, check UPSTREAM_REPO if valid or not!')