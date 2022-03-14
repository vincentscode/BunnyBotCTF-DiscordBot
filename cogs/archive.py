import discord
import asyncio
import json
import time
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

class Archive(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def archive(self, ctx: commands.Context, category: discord.CategoryChannel):
        print("archive")
        await ctx.send("Archiving...")

        guild: discord.Guild = ctx.guild
        archive_category: discord.CategoryChannel = await get(guild.categories, name="Archive")
        archive_channel: discord.TextChannel = await guild.create_text_channel(category.name, category=archive_category, reason="archive")
        
        await archive_channel.send(f"Archived at {datetime.datetime.now()}")

        e = discord.Embed()
        e.title = f'Archived {category.name} ({category.id})'
        e.description = "```"
        for t in category.text_channels:
            print(" > ", t.name)
            t_thread: discord.Thread = await archive_channel.create_thread(t.name, type=discord.ChannelType.public_thread, reason="archive")
            t_history = await t.history(limit=None).flatten()
            
            msg: discord.Message
            for msg in t_history:
                msg_embed = discord.Embed()
                msg_embed.set_author(name=f"{msg.author.name}#{msg.author.discriminator}")
                msg_embed.description = msg.content
                await t_thread.send(embed=msg_embed)
            e.description += f" - {t.name} ({t.id}) => {len(t_history)} messages\n"
        e.description += "```"   
        await ctx.send(embed=e)
        

async def setup(client):
    await client.add_cog(Archive(client))
