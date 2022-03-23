import asyncio
import logging
from logging.handlers import RotatingFileHandler
from os.path import exists
import discord
import json

from BunnyBotCTF import BunnyBotCTF

logger = logging.getLogger('discord')
logger.setLevel(level=logging.INFO)
handler = RotatingFileHandler(filename='weird-birb.log', mode='a', maxBytes=1024 * 1024 * 5, backupCount=2,
                              encoding='utf-8')
# logging pattern:  "^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3})\s(\S*)\s*(\w*)\s*(.*)$"
# time pattern:     "yyyy-MM-dd HH:mm:ss,SSS"
# line pattern:     "^\d"
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(name)-15s %(message)s'))
logger.addHandler(handler)

config_path = './config.json'

if not exists(config_path):
    print("no config.json file")
    logger.log(logging.ERROR, "no config.json file")
    exit(1)

# load config
with open(config_path, 'r') as f:
    config = json.load(f)

TOKEN = config['token']
PREFIX = config['prefix']
COGS_DIR = "cogs"

# define bot
intents = discord.Intents().all()
bot_client = BunnyBotCTF(command_prefix=PREFIX, intents=intents)


async def main():
    async with bot_client:
        await bot_client.load_extensions(COGS_DIR)
        await bot_client.start(TOKEN)


asyncio.run(main())
