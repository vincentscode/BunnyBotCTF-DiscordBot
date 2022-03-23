import os
import discord
import datetime
from discord.ext import commands
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
        archive_channel: discord.TextChannel = await guild.create_text_channel(category.name,
                                                                               category=archive_category,
                                                                               reason="archive")

        await archive_channel.send(f"Archived at {datetime.datetime.now()}")

        e = discord.Embed()
        e.title = f'Archived {category.name} ({category.id})'
        e.description = "```"
        for t in category.text_channels[::-1]:
            print(" > ", t.name)
            t_thread: discord.Thread = await archive_channel.create_thread(name=t.name,
                                                                           auto_archive_duration=60,
                                                                           type=discord.ChannelType.public_thread,
                                                                           reason="archive")
            t_history = [message async for message in t.history(limit=None)]

            msg: discord.Message
            for msg in t_history[::-1]:
                msg_embed = discord.Embed()
                msg_embed.set_author(name=f"{msg.author.name}#{msg.author.discriminator}")
                msg_embed.description = msg.content
                msg_embed.timestamp = msg.created_at

                files = []
                for at in msg.attachments:
                    attachment_path = os.path.join("./cache/", at.filename)
                    await at.save(fp=attachment_path)
                    files.append(discord.File(attachment_path, filename=at.filename))

                await t_thread.send(embed=msg_embed, files=files)
            e.description += f" - {t.name} ({t.id}) => {len(t_history)} messages\n"

            if delete:
                await t.delete(reason="archive")
        e.description += "```"

        if delete:
            await category.delete(reason="archive")

        await ctx.send(embed=e)


async def setup(client):
    await client.add_cog(Archive(client))
