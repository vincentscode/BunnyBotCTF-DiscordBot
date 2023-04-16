import discord
import datetime
from discord.ext import commands
from discord.utils import find


class Done(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Mark a channel as completed")
    async def done(self, ctx: commands.Context):
        if '✅' in ctx.channel.name:
            await ctx.respond("This channel has been marked as completed already.")
            return

        new_name = ctx.channel.name
        new_name = new_name.replace("🔒", "")
        new_name = new_name.replace("🔓", "")
        new_name = new_name.replace("🔐", "")
        new_name += '✅'
        await ctx.channel.edit(name = new_name)

        e = discord.Embed()
        e.title = f'✅ Challenge completed'
        e.timestamp = datetime.datetime.now()
        e.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}")
        await ctx.respond(embed=e)


def setup(client):
    client.add_cog(Done(client))
