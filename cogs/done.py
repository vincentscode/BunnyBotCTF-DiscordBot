import discord
import datetime
from discord.ext import commands
from discord.utils import find


class Done(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Mark a channel as completed")
    async def done(self, ctx: discord.ApplicationContext):
        if '✅' in ctx.channel.name:
            await ctx.respond("This channel has been marked as completed already.")
            return
        
        is_thread = isinstance(ctx.channel, discord.Thread)

        new_name = ctx.channel.name
        new_name = new_name.replace("🔒", "")
        new_name = new_name.replace("🔓", "")
        new_name = new_name.replace("🔐", "")
        new_name = new_name.replace("👀", "")
        new_name = '✅' + new_name

        reason = f"Channel marked as completed by @{ctx.author.name}"

        await ctx.response.defer()
        if not is_thread:
            await ctx.channel.edit(
                name = new_name,
                topic = "",
                reason = reason
            )
        else:
            await ctx.channel.join()
            await ctx.channel.edit(
                name = new_name,
                reason = reason
            )

        
        e = discord.Embed()
        e.title = f'✅ Challenge completed'
        e.timestamp = datetime.datetime.now()
        e.set_author(name=f"@{ctx.author.name}")
        await ctx.followup.send(embed=e)


def setup(client):
    client.add_cog(Done(client))
