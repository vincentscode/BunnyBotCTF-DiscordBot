import discord
import asyncio
import json
import time
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import find

class Archive(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def archive(self, ctx: commands.Context, category: discord.CategoryChannel, delete: bool = False):
        print("archive")
        await ctx.send("Archiving...")

        guild: discord.Guild = ctx.guild
        archive_category: discord.CategoryChannel = find(lambda c: c.name.lower() == "archive", guild.categories)
        archive_channel: discord.TextChannel = await guild.create_text_channel(category.name, category=archive_category, reason="archive")
        
        await archive_channel.send(f"Archived at {datetime.datetime.now()}")

        e = discord.Embed()
        e.title = f'Archived {category.name} ({category.id})'
        e.description = "```"
        for t in category.text_channels[::-1]:
            print(" > ", t.name)
            t_thread: discord.Thread = await archive_channel.create_thread(name=t.name, type=discord.ChannelType.public_thread, reason="archive")
            t_history = await t.history(limit=None).flatten()

            msg: discord.Message
            for msg in t_history[::-1]:
                msg_embed = discord.Embed()
                msg_embed.set_author(name=f"{msg.author.name}#{msg.author.discriminator}")
                msg_embed.description = msg.content
                msg_embed.timestamp = msg.created_at

                files = []
                for at in msg.attachments:
                    await at.save(fp="cache/" + at.filename)
                    files.append(discord.File("cache/" + at.filename, filename=at.filename))

                await t_thread.send(embed=msg_embed, files=files)
            e.description += f" - {t.name} ({t.id}) => {len(t_history)} messages\n"

            if delete:
                await t.delete(reason="archive")
        e.description += "```"
        
        if delete:
            await category.delete(reason="archive")

        await ctx.send(embed=e)
        

def setup(client):
    client.add_cog(Archive(client))
