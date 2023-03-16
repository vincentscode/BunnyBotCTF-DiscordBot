import discord
import datetime
from discord.ext import commands
from discord.utils import find


class Done(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def done(self, ctx: commands.Context):
        if '✅' in ctx.channel.name:
            await ctx.send("This channel has been marked as completed already.")
            return

        await ctx.channel.edit(name = ctx.channel.name + '✅')

        e = discord.Embed()
        e.title = f'✅ Challenge completed'
        e.timestamp = datetime.datetime.now()
        e.set_author(name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}")

        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Done(client))
