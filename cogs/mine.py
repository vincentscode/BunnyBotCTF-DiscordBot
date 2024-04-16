import discord
import datetime
from discord.ext import commands
from collections import namedtuple

StateInfo = namedtuple("StateInfo", ["name", "icon"])
states = {
    "mine": StateInfo("Locked", "🔒"),
    "locked": StateInfo("Locked", "🔒"),
    "closed": StateInfo("Locked", "🔒"),
    "hints welcome": StateInfo("Hints Welcome", "👀"),
    "pls ask": StateInfo("Please Ask", "🔐"),
    "open": StateInfo("Open", "🔓"),
    "none": StateInfo("Unmarked", ""),
}

class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Mark a channel or thread as locked")
    async def mine(
        self,
        ctx: discord.ApplicationContext,
        state: discord.Option(str, description="State of the channel", default="mine", choices=list(states.keys()))
    ):
        global states
        
        if '✅' in ctx.channel.name:
            await ctx.respond("This channel has been marked as completed already.")
            return
        
        is_thread = isinstance(ctx.channel, discord.Thread)

        new_name = ctx.channel.name
        new_name = new_name.replace("🔒", "")
        new_name = new_name.replace("🔓", "")
        new_name = new_name.replace("🔐", "")
        new_name = new_name.replace("👀", "")
        new_name = states[state].icon + new_name
        
        new_topic = f"State: {states[state].icon} {states[state].name}"

        reason = f"Channel state changed by {ctx.author.name}"

        if not is_thread:
            await ctx.channel.edit(
                name = new_name,
                topic = new_topic,
                reason = reason
            )
        else:
            await ctx.channel.edit(
                name = new_name,
                reason = reason
            )

        e = discord.Embed()
        e.title = f'{states[state].icon} Channel marked as {states[state].name}'
        if state == "mine":
            e.set_image(url="https://media.tenor.com/Q8ioGKtuU0oAAAAC/mine-finding-nemo.gif")
        e.timestamp = datetime.datetime.now()
        e.set_author(name=f"@{ctx.author.name}")
        await ctx.respond(embed=e)


def setup(client):
    client.add_cog(Mine(client))
