import discord
import asyncio
import json
import time
from discord.ext import commands
from discord.ext.commands import Bot

class Archive(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def archive(self, ctx, category: discord.CategoryChannel):
        await ctx.send(f'Archiving {category} ({category.id})')

def setup(client):
    client.add_cog(Archive(client))
