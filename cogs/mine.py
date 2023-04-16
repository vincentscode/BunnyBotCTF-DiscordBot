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
    "open": StateInfo("Open", "🔓")
}

class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Mark a channel as locked")
    async def mine(
        self,
        ctx: commands.Context,
        state: discord.Option(str, description="State of the channel", default="mine", choices=list(states.keys())),
        modify_permissions: discord.Option(bool, description="Set permissions for others according to the state", default=False)
    ):
        global states

        if '✅' in ctx.channel.name:
            await ctx.respond("This channel has been marked as completed already.")
            return
        
        new_name = ctx.channel.name
        new_name = new_name.replace("🔒", "")
        new_name = new_name.replace("🔓", "")
        new_name = new_name.replace("🔐", "")
        new_name = states[state].icon + new_name
        
        await ctx.channel.edit(
            name = new_name,
            topic = f"State: {states[state].icon} {states[state].name}",
            reason = f"Channel state changed by {ctx.author.name}#{ctx.author.discriminator}",
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    send_messages = state not in ["mine", "locked", "closed"]
                ),
                ctx.author: discord.PermissionOverwrite(
                    send_messages = True
                )
            } if modify_permissions else None
        )

        e = discord.Embed()
        e.title = f'{states[state].icon} Channel marked as {states[state].name}'
        if state == "mine":
            e.set_image(url="https://media.tenor.com/Q8ioGKtuU0oAAAAC/mine-finding-nemo.gif")
        e.timestamp = datetime.datetime.now()
        e.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}")
        await ctx.respond(embed=e)


def setup(client):
    client.add_cog(Mine(client))
