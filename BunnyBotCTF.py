import os.path
import sys
import traceback

from discord import Game
from discord.ext import commands


class BunnyBotCTF(commands.Bot):
    async def on_ready(self):
        await self.change_presence(activity=Game(name="a CTF!"))
        print(
            f"Logged in as {self.user.name} ({self.user.id}) answering to '{self.command_prefix}command'")

    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)

        # match is nicer but needs python 3.10
        match error:
            # ignored
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

    async def load_extensions(self, cogs_dir: str):
        for extension in [f"{cogs_dir}.{x[:-len('.py')]}" for x in os.listdir(cogs_dir) if x.endswith(".py")]:
            try:
                await self.load_extension(extension)
                print('Loaded extension \"{}\"'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension \"{}\"\n{}'.format(extension, exc))
