import logging
from logging import info, error
from os import path, environ
from subprocess import run
from requests import get
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from config.env
load_dotenv('config.env', override=True)

# Get BOT_TOKEN from environment
BOT_TOKEN = environ.get('BOT_TOKEN', '')
if not BOT_TOKEN:
    logger.error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0]

# Get DATABASE_URL from environment
DATABASE_URL = environ.get('DATABASE_URL', None)

if DATABASE_URL:
    client = MongoClient(DATABASE_URL)
    db = client.hydro
    old_config = db.settings.deployConfig.find_one({'_id': bot_id})
    config_dict = db.settings.config.find_one({'_id': bot_id})

    if old_config:
        del old_config['_id']

    if (old_config is None or old_config == dict(dotenv_values('config.env'))) and config_dict:
        environ['UPSTREAM_REPO'] = config_dict['UPSTREAM_REPO']
        environ['UPSTREAM_BRANCH'] = config_dict['UPSTREAM_BRANCH']
    
    client.close()

# Set UPSTREAM_REPO and UPSTREAM_BRANCH with defaults if not provided
UPSTREAM_REPO = environ.get('UPSTREAM_REPO', 'https://github.com/Tamilloggers/Hyrostreambot')
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'master')

# Update the repository if UPSTREAM_REPO is set
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

    repo = UPSTREAM_REPO.split('/')
    UPSTREAM_REPO = f"https://github.com/{repo[-2]}/{repo[-1]}"
    if update.returncode == 0:
        info('Successfully updated with latest commits !!')
    else:
        error('Something went Wrong ! Retry or Ask Support !')
    info(f'UPSTREAM_REPO: {UPSTREAM_REPO} | UPSTREAM_BRANCH: {UPSTREAM_BRANCH}')
