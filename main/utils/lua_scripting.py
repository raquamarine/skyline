# HATE, LET ME TELL YOU HOW MUCH I HATE THIS SCRIPT, IVE REDONE THIS 3 TIMES JUST TO BE ABLE TO READ IT
# (TODO: make it readable without having 300 documentation pages open)

import discord
from discord.ext import commands
from lupa import LuaRuntime
import asyncio
import os
import io
from PIL import Image
import yaml
import logging
from . import animals
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import requests
geolocator = Nominatim(user_agent="skyline_bot", timeout=5)
from main.utils.database import writeinfra
lua = LuaRuntime(unpack_returned_tuples=True)
bot = None
lua_commands = {}


# lua bridge
def create_discord_lib(interaction, command_args):
    def reply(msg):
        asyncio.create_task(interaction.followup.send(msg))  # use asyncio or it just times out i guess?
    
    def _send_animal_image(getter, filename): # wrapper to get the animal image without having to copy and past it 500 times
        image = getter()
        file = discord.File(image, filename=filename)
        asyncio.create_task(interaction.followup.send(file=file))

    def get_arg(name):
      return command_args.get(name, None)

    async def _ban(member_id, reason):
        member = interaction.guild.get_member(int(member_id))
        await member.ban(reason=reason)
        writeinfra(member.id, interaction.guild.id, interaction.user.id, "ban", reason, int(time.time()), None)

    def ban_member(member_id, reason):
        asyncio.create_task(_ban(member_id, reason))

    async def _kick(member_id, reason):
        member = interaction.guild.get_member(int(member_id))
        await member.kick(reason=reason)
        from main.utils.database import writeinfra
        import time
        writeinfra(member.id, interaction.guild.id, interaction.user.id, "kick", reason, int(time.time()), None)

    def kick_member(member_id, reason):
        asyncio.create_task(_kick(member_id, reason))

    async def _mute(member_id, duration):
        from datetime import timedelta
        member = interaction.guild.get_member(int(member_id))
        await member.timeout_for(duration=timedelta(seconds=duration))
        from main.utils.database import writeinfra
        import time
        writeinfra(member.id, interaction.guild.id, interaction.user.id, "mute", None, int(time.time()), duration)

    def mute_member(member_id, duration):
        asyncio.create_task(_mute(member_id, duration))

    async def _warn(member_id, reason):
        from main.utils.database import writeinfra
        import time
        writeinfra(int(member_id), interaction.guild.id, interaction.user.id, "warn", reason, int(time.time()), None)

    def warn_member(member_id, reason):
        asyncio.create_task(_warn(member_id, reason))

    def has_permission():
        return interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.ban_members

    async def _get_weather(city):


        try:
            location = geolocator.geocode(city, addressdetails=True)
            if not location:
                await interaction.followup.send("Couldn't find that city")
                return

            lat = location.latitude
            lon = location.longitude

            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "timezone": "auto"
            }

            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            current = data.get("current")
            country = location.raw.get("address", {}).get("country", "Unknown")

            msg = (f"Weather in {city} ({country}):\n"
                   f"Temperature: {current['temperature_2m']} °C\n"
                   f"Humidity: {current['relative_humidity_2m']}%\n"
                   f"Wind speed: {current['wind_speed_10m']} km/h")

            await interaction.followup.send(msg)
        except:
            await interaction.followup.send("Failed to get weather")

    def get_weather(city):
        asyncio.create_task(_get_weather(city))

    async def _sstv(image_url, mode):
        from pysstv.color import MartinM1, ScottieS1, Robot36
        import requests

        try:
            response = requests.get(image_url)
            img = Image.open(io.BytesIO(response.content))

            if mode == "martin":
                img = img.resize((320, 256), Image.Resampling.LANCZOS)
                sstv = MartinM1(img, 22050, 16)
            elif mode == "scottie":
                img = img.resize((320, 256), Image.Resampling.LANCZOS)
                sstv = ScottieS1(img, 22050, 16)
            elif mode == "robot":
                img = img.resize((320, 240), Image.Resampling.LANCZOS)
                sstv = Robot36(img, 22050, 16)

            audio_buffer = io.BytesIO()
            sstv.write_wav(audio_buffer)
            audio_buffer.seek(0)

            await interaction.followup.send(file=discord.File(audio_buffer, filename="sstv.wav"))
        except:
            await interaction.followup.send("Failed to generate SSTV")

    def generate_sstv(image_url, mode):
        asyncio.create_task(_sstv(image_url, mode))
    def send_bunny():
        _send_animal_image(animals.get_bunny_image, "bunny.png")

    def send_dog():
        _send_animal_image(animals.get_dog_image, "dog.png")

    def send_cat():
        _send_animal_image(animals.get_cat_image, "cat.png")

    def send_duck():
        _send_animal_image(animals.get_duck_image, "duck.png")

    def send_fox():
        _send_animal_image(animals.get_fox_image, "fox.png")

    def author_name():
        return interaction.user.name

    def author_id():
        return str(interaction.user.id)

    def channel_name():
        return interaction.channel.name

    def guild_name():
        return interaction.guild.name if interaction.guild else "DM"

    return lua.table(
        reply=reply,
        has_permission=has_permission,
        ban_member=ban_member,
        kick_member=kick_member,
        mute_member=mute_member,
        warn_member=warn_member,
        send_bunny=send_bunny,
        send_dog=send_dog,
        get_arg=get_arg,
        get_weather=get_weather,
        generate_sstv=generate_sstv,
        send_cat=send_cat,
        send_duck=send_duck,
        send_fox=send_fox,
        author_name=author_name,
        author_id=author_id,
        channel_name=channel_name,
        guild_name=guild_name,
    )


# registsers commands
def register_lua_command(name, description, arguments, lua_function):
    async def command_handler(ctx, **kwargs):
        await ctx.defer()
        lua.globals().discord = create_discord_lib(ctx, kwargs)
        try:
            lua_function()
        except Exception as e:
            await ctx.followup.send(f"Error: {e}")

    command_handler.__name__ = name

    for arg_name in reversed(arguments):
        command_handler = discord.option(
            name=arg_name,
            description=arg_name,
            required=True
        )(command_handler)

    bot.slash_command(name=name, description=description)(command_handler)


# loads all luas
def load_lua_file(path):
    lua.globals().register_command = register_lua_command
    with open(path, "r") as f:
        lua.execute(f.read())


def load_all_lua_scripts():
    base = os.path.join(os.path.dirname(__file__), "..", "lua_scripts")
    if not os.path.isdir(base):
        logging.error("lua_scripts folder not found")
        return

    for file in os.listdir(base):
        if file.endswith(".lua"):
            load_lua_file(os.path.join(base, file))

    logging.info(f"loaded {len(lua_commands)} lua commands")


# bot init
def lua_init(bot_instance: commands.Bot):
    global bot
    bot = bot_instance

    @bot.event
    async def on_ready():
        logging.info("bot ready (slash commands synced)")

    load_all_lua_scripts()