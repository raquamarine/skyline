# HATE, LET ME TELL YOU HOW MUCH I HATE THIS SCRIPT, IVE REDONE THIS 3 TIMES JUST TO BE ABLE TO READ IT
# (TODO: make it readable without having 300 documentation pages open)

import discord
from discord.ext import commands
from lupa import LuaRuntime
import asyncio
import os
import logging
from . import animals

lua = LuaRuntime(unpack_returned_tuples=True)
bot = None
lua_commands = {}


# lua bridge
def create_discord_lib(interaction):
    def reply(msg):
        asyncio.create_task(interaction.followup.send(msg))  # use asyncio or it just times out i guess?

    def _send_image(getter, filename): # wrapper to get the animal image without having to copy and past it 500 times
        image = getter()
        file = discord.File(image, filename=filename)
        asyncio.create_task(interaction.followup.send(file=file))

    def send_bunny():
        _send_image(animals.get_bunny_image, "bunny.png")

    def send_dog():
        _send_image(animals.get_dog_image, "dog.png")

    def send_cat():
        _send_image(animals.get_cat_image, "cat.png")

    def send_duck():
        _send_image(animals.get_duck_image, "duck.png")

    def send_fox():
        _send_image(animals.get_fox_image, "fox.png")

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
        send_bunny=send_bunny,
        send_dog=send_dog,
        send_cat=send_cat,
        send_duck=send_duck,
        send_fox=send_fox,
        author_name=author_name,
        author_id=author_id,
        channel_name=channel_name,
        guild_name=guild_name,
    )


# registsers commands
def register_lua_command(name, lua_fn):
    async def handler(ctx):
        await ctx.defer()
        lua.globals().discord = create_discord_lib(ctx)

        try:
            lua_fn()
        except Exception as e:
            await ctx.followup.send(f"lua error: {e}")

    handler.__name__ = name
    bot.slash_command(name=name, description=f"Lua command: {name}")(handler)
    lua_commands[name] = lua_fn


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