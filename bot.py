import discord
import asyncio
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import json
import os
import traceback
import sys

# load config
with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['token']
PREFIX = config['prefix']
COGS_DIR = "cogs"

# define bot
intents = discord.Intents().all()
client = commands.Bot(command_prefix=PREFIX, intents=intents)

# events
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="a CTF!"))
    print(f"Logged in as {client.user.name} ({client.user.id})")

@client.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)

    ignored = (commands.CommandNotFound, )
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f"{ctx.command} has been disabled.")

    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: {error.param}")

    elif isinstance(error, commands.ChannelNotFound):
        await ctx.send(f"Channel or Category not found: {error.argument}")

    else:
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
