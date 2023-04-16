import random
from typing import List, Dict, Optional

import discord
from discord.ext import commands
import requests
import datetime as dt
from dataclasses import dataclass
import pytz


class infoFlags(commands.FlagConverter):
    id: Optional[int]
    url: Optional[str]
    discord: Optional[str] = "unknown"
    password: Optional[str]
    timezone: Optional[str] = "CET"


@dataclass
class CTFTimeEvent:
    """Class describing an CTFTime event"""
    title: str
    description: str
    challenge_format: str
    restrictions: str
    organizer_list: List[Dict[str, str | int]]
    start_date: dt.datetime
    end_date: dt.datetime
    logo: str
    weight: int
    url: str
    ctftime_url: str


class CTFTime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.slash_command(description="Get info about a CTFtime event")
    async def ctf_info(self, ctx: commands.Context, *, flags: infoFlags):

        if not flags.url and not flags.id:
            await ctx.send("give at least the url or id")
            return

        if flags.url and not flags.id:
            flags.id = extract_id(flags.url)
        if flags.id and not flags.url:
            flags.url = "https://ctftime.org/event/" + str(flags.id)

        if flags.id > 0:
            ce = retrieve_ctftime_event(flags.id)

            try:
                tz_object = pytz.timezone(flags.timezone)
            except pytz.UnknownTimeZoneError:
                await ctx.send("unknown timezone")
                tz_object = pytz.timezone("UTC")

            ce.start_date = ce.start_date.astimezone(tz_object)
            ce.end_date = ce.end_date.astimezone(tz_object)

            e = discord.Embed()
            e.title = f"**{ce.title}** ({ce.weight}) by {', '.join([o.get('name') for o in ce.organizer_list])}"
            e.description = f"{ce.description}"
            e.set_thumbnail(url=ce.logo)
            e.add_field(name="website", value=ce.url, inline=True)
            e.add_field(name="discord", value=flags.discord, inline=True)
            e.add_field(name="CTFtime", value=flags.url, inline=True)
            e.add_field(name="start", value=f"{ce.start_date}\n{ce.start_date.tzinfo}")
            e.add_field(name="end", value=f"{ce.end_date}\n{ce.end_date.tzinfo}")
            e.add_field(name="length", value=ce.end_date - ce.start_date, inline=True)
            e.add_field(name="group password",
                        value=flags.password if flags.password else generate_password(),
                        inline=True)
            await ctx.send(embed=e)
        else:
            await ctx.send("unknown CTFtime id")

    @commands.command("CTFregister")
    async def register_ctf(self, ctx: commands.Context, event_id_or_url: int | str):
        event_id = extract_id(event_id_or_url)
        if event_id > 0:
            ce = retrieve_ctftime_event(event_id)
            f: discord.ScheduledEvent
            event = discord.utils.find(lambda e: e.name == ce.title, ctx.guild.scheduled_events)
            if not event:

                # safety checks
                now = dt.datetime.now().astimezone(dt.datetime.now().astimezone().tzinfo)
                if now > ce.start_date:
                    ce.start_date = round_to_next_15_minutes(now) + dt.timedelta(minutes=15)
                if now > ce.end_date:
                    await ctx.send("event is already over")
                    return

                await ctx.guild.create_scheduled_event(name=ce.title,
                                                       description=ce.description if len(
                                                           ce.description) < 1000 else ce.description[:997] + '...',
                                                       start_time=round_to_next_15_minutes(ce.start_date),
                                                       end_time=round_to_next_15_minutes(ce.end_date),
                                                       location=ce.url)
                await ctx.send("event created")
            else:
                await ctx.send("event already exists")

        else:
            await ctx.send("oops something went wrong")


def round_to_next_15_minutes(t: dt.datetime) -> dt.datetime:
    return t.replace(microsecond=0, second=0, minute=(t.minute // 15) * 15)


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
        start_date=dt.datetime.fromisoformat(start_date_str),
        end_date=dt.datetime.fromisoformat(end_date_str),
        logo=data.get("logo"),
        weight=data.get('weight', 0),
        ctftime_url=data.get("ctftime_url", api_url),
        url=data.get("url", api_url)
    )


def extract_id(event_id_or_url: int | str) -> int:
    match event_id_or_url:
        case str():
            event_id = int(event_id_or_url.split("/")[-1])
        case int():
            event_id = event_id_or_url
        case _:
            event_id = -1

    return event_id


def generate_password(length: int = 20) -> str:
    chr_start = 33
    chr_end = 126
    password = ''
    for _ in range(length):
        rand_int = random.randint(chr_start, chr_end)
        password += (chr(rand_int))
    return password


def setup(client):
    client.add_cog(CTFTime(client))
