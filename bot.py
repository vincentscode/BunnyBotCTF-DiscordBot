import discord
from discord import Game
from discord.ext import commands
import json
import os
import traceback
import sys
import random
import logging

# logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# load config
with open('config/config.json', 'r') as f:
    config = json.load(f)

TOKEN = config.get('token', '')
PREFIX = config.get('prefix', '+')
HELLO_CHANNEL = config.get('hello-channel', '')
SEND_HELLO_MSG = config.get('send-startup-message', False)
COGS_DIR = "cogs"

if not TOKEN:
    print("token config is missing")

# define bot
intents = discord.Intents().all()
client = commands.Bot(command_prefix=PREFIX, intents=intents)

# events
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="a CTF!"))
    print(f"Logged in as {client.user.name} ({client.user.id})")
    
    if SEND_HELLO_MSG and HELLO_CHANNEL != '':
        for guild in client.guilds:
            channel = list(filter(lambda c: c.name == HELLO_CHANNEL, guild.channels))
            if len(channel) > 0:
                with open('resources/hello-phrases.txt', 'r') as hello_phrases:
                    phrases = hello_phrases.readlines()
                    rand_phrase = random.choice(phrases)
                    await channel[0].send(rand_phrase)


@client.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)

    match error:
        case commands.CommandNotFound():
            return
        case commands.DisabledCommand():
            await ctx.send(f"{ctx.command} has been disabled.")
        case commands.NoPrivateMessage():
            await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
        case commands.MissingRequiredArgument():
            await ctx.send(f"Missing argument: {error.param}")
        case commands.ChannelNotFound():
            await ctx.send(f"Channel or Category not found: {error.argument}")
        case _:
            print('Unhandled exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


for extension in [f"{COGS_DIR}.{x[:-len('.py')]}" for x in os.listdir(COGS_DIR) if x.endswith(".py")]:
    try:
        client.load_extension(extension)
        print('Loaded extension \"{}\"'.format(extension))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension \"{}\"\n{}'.format(extension, exc))

client.run(TOKEN)
