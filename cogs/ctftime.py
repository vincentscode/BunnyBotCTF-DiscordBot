from typing import List, Dict

import discord
from discord import InteractionType
from discord.ext import commands
import requests
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CTFTimeEvent:
    """Class describing an CTFTime event"""
    title: str
    description: str
    challenge_format: str
    restrictions: str
    organizer_list: List[Dict[str, str | int]]
    start_date: datetime
    end_date: datetime
    logo: str
    weight: int
    url: str
    ctftime_url: str


class CTFTime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("CTFinfo")
    async def ctf_info(self, ctx: commands.Context,
                       event_id_or_url: int | str):

        event_id = extract_id(event_id_or_url)

        if event_id > 0:
            ce = retrieve_ctftime_event(event_id)

            e = discord.Embed()
            e.title = f"**{ce.title}** ({ce.weight}) by {', '.join([o.get('name') for o in ce.organizer_list])}"
            e.description = f"{ce.description}"
            e.set_thumbnail(url=ce.logo)
            e.add_field(name="website", value=ce.url, inline=True)
            e.add_field(name="restrictions", value=ce.restrictions, inline=True)
            e.add_field(name="format", value=ce.challenge_format)
            e.add_field(name="start", value=f"{ce.start_date}\n{ce.start_date.tzinfo}")
            e.add_field(name="end", value=f"{ce.end_date}\n{ce.end_date.tzinfo}")
            e.add_field(name="length", value=ce.end_date - ce.start_date, inline=True)
            await ctx.send(embed=e)
        else:
            await ctx.send("oops something went wrong")

    @commands.command("CTFregister")
    async def register_ctf(self, ctx: commands.Context, event_id_or_url: int | str):
        event_id = extract_id(event_id_or_url)
        if event_id > 0:
            ce = retrieve_ctftime_event(event_id)
            f: discord.ScheduledEvent
            event = discord.utils.find(lambda e: e.name == ce.title, ctx.guild.scheduled_events)
            if not event:
                # TODO check if event begin/end is before now and do stuff because of that
                await ctx.guild.create_scheduled_event(name=ce.title,
                                                       description=ce.description,
                                                       start_time=ce.start_date,
                                                       end_time=ce.end_date,
                                                       location=ce.url)
            else:
                await ctx.send("event already exists")

        else:
            await ctx.send("oops something went wrong")


def retrieve_ctftime_event(event_id: int) -> CTFTimeEvent:
    api_url = f"https://ctftime.org/api/v1/events/{event_id}/"

    response = requests.get(api_url, headers={"User-Agent": "BunnyBotCTF-DiscordBot"})
    data = response.json()
    start_date_str = data.get('start')
    end_date_str = data.get('finish')

    return CTFTimeEvent(
        title=data.get('title', "unknown title"),
        description=data.get("description", "no description"),
        challenge_format=data.get("format", "unknown"),
        restrictions=data.get('restrictions', 'Open probably'),
        organizer_list=data.get('organizers', [{"id": -1, "name": "unknown"}]),
        start_date=datetime.fromisoformat(start_date_str),
        end_date=datetime.fromisoformat(end_date_str),
        logo=data.get("logo"),
        weight=data.get('weight', 0),
        ctftime_url=data.get("ctftime_url", api_url),
        url=data.get("url", api_url)
    )


def extract_id(event_id_or_url: int | str) -> int:
    match event_id_or_url:
        case str():
            print(event_id_or_url.split("/")[-1])
            event_id = int(event_id_or_url.split("/")[-1])
        case int():
            event_id = event_id_or_url

    return event_id


# TODO either implement or remove
def get_discord_link(url: str) -> str | None:
    response = requests.get(url)


def setup(client):
    client.add_cog(CTFTime(client))