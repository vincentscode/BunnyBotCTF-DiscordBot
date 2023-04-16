import discord
import datetime
from discord.ext import commands
from discord.utils import find


class Archive(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Archive a category")
    async def archive(
        self,
        ctx: commands.Context,
        category: discord.Option(discord.CategoryChannel, name="category", description="Category to archive", required=True),
        delete: discord.Option(bool, name="delete", description="Should the category be deleted?", required=False, default=False)
    ):
        await ctx.respond("Archiving...")

        guild: discord.Guild = ctx.guild
        archive_category: discord.CategoryChannel = find(lambda c: c.name.lower() == "archive", guild.categories)
        archive_channel: discord.TextChannel = await guild.create_text_channel(name=category.name,
                                                                               category=archive_category,
                                                                               reason="archive")

        await archive_channel.send(f"Archived at {datetime.datetime.now()}")

        e = discord.Embed()
        e.title = f'Archived {category.name} ({category.id})'
        e.description = "```"
        for t in category.text_channels[::-1]:
            print(" > ", t.name)
            t_thread: discord.Thread = await archive_channel.create_thread(name=t.name,
                                                                           type=discord.ChannelType.public_thread,
                                                                           reason="archive")
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

                try:
                    await t_thread.send(embed=msg_embed, files=files)
                except Exception as ex:
                    await t_thread.send("Failed to archive message:\n" + str(ex))
            e.description += f" - {t.name} ({t.id}) => {len(t_history)} messages\n"

            if delete:
                await t.delete(reason="archive")
        e.description += "```"

        if delete:
            await category.delete(reason="archive")

        await ctx.respond(embed=e)


def setup(client):
    client.add_cog(Archive(client))
