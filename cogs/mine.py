import discord
import datetime
from discord.ext import commands
from collections import namedtuple

StateInfo = namedtuple("StateInfo", ["name", "icon"])

class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Mark a channel as locked")
    async def mine(
        self,
        ctx: commands.Context,
        state: discord.Option(str, description="State of the channel", default="mine", choices=["closed", "mine", "locked", "pls ask", "open"]),
        modify_permissions: discord.Option(bool, name="modify permissions", description="Set permissions for others according to the state", description="Modify permissions", default=False)
    ):
        states = {
            "mine": StateInfo("Locked", "🔒"),
            "locked": StateInfo("Locked", "🔒"),
            "closed": StateInfo("Locked", "🔒"),
            "pls ask": StateInfo("Please ask", "🔐"),
            "open": StateInfo("Open", "🔓")
        }
        
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
                    send_messages = state in ["open", "pls ask"]
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
