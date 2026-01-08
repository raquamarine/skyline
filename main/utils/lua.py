import discord
from discord.ext import commands
from lupa import LuaRuntime
import asyncio
import os
from io import BytesIO
import logging
lua = LuaRuntime(unpack_returned_tuples=True)
lua_commands = {}
bot = None

try:
  from . import animals

  animals_available = True
except ImportError:
  animals_available = False


def create_discord_lib(interaction):
  def send(message):
    asyncio.create_task(interaction.response.send_message(message))

  def reply(message):
    asyncio.create_task(interaction.response.send_message(message))

  async def send_bunny_async():
    if not animals_available:
      await interaction.followup.send("animals module not available")
      logging.error("animals module not available")
      return
    image = animals.get_bunny_image()
    file = discord.File(image, filename="bunny.png")
    await interaction.followup.send(file=file)

  async def send_dog_async():
    if not animals_available:
      await interaction.followup.send("animals module not available")
      logging.error("animals module not available")
      return
    image = animals.get_dog_image()
    file = discord.File(image, filename="dog.png")
    await interaction.followup.send(file=file)

  async def send_cat_async():
    if not animals_available:
      await interaction.followup.send("animals module not available")
      logging.error("animals module not available")
      return
    image = animals.get_cat_image()
    file = discord.File(image, filename="cat.png")
    await interaction.followup.send(file=file)

  async def send_duck_async():
    if not animals_available:
      await interaction.followup.send("animals module not available")
      logging.error("animals module not available")
      return
    image = animals.get_duck_image()
    file = discord.File(image, filename="duck.png")
    await interaction.followup.send(file=file)

  async def send_fox_async():
    if not animals_available:
      await interaction.followup.send("animals module not available")
      logging.error("animals module not available")
      return
    image = animals.get_fox_image()
    file = discord.File(image, filename="fox.png")
    await interaction.followup.send(file=file)

  def send_bunny():
    asyncio.create_task(send_bunny_async())
    logging.info("sending bunny image")

  def send_dog():
    asyncio.create_task(send_dog_async())
    logging.info("sending dog image")

  def send_cat():
    asyncio.create_task(send_cat_async())
    logging.info("sending cat image")

  def send_duck():
    asyncio.create_task(send_duck_async())
    logging.info("sending duck image")

  def send_fox():
    asyncio.create_task(send_fox_async())
    logging.info("sending fox image")

  def get_author_name():
    return str(interaction.user.name)

  def get_author_id():
    return str(interaction.user.id)

  def get_channel_name():
    return str(interaction.channel.name)

  def get_guild_name():
    return str(interaction.guild.name) if interaction.guild else "DM"

  def add_reaction(emoji):
    asyncio.create_task(interaction.message.add_reaction(emoji))

  def get_message_content():
    return ""

  return lua.table(
    send=send,
    reply=reply,
    send_bunny=send_bunny,
    send_dog=send_dog,
    send_cat=send_cat,
    send_duck=send_duck,
    send_fox=send_fox,
    get_author_name=get_author_name,
    get_author_id=get_author_id,
    get_channel_name=get_channel_name,
    get_guild_name=get_guild_name,
    add_reaction=add_reaction,
    get_message_content=get_message_content
  )


def register_lua_command(name, lua_function):
  async def command_wrapper(interaction: discord.Interaction, args: str = ""):
    await interaction.response.defer()

    discord_lib = create_discord_lib(interaction)
    lua.globals().discord = discord_lib
    lua.globals().args = args

    try:
      lua_function(args)
    except Exception as e:
      await interaction.followup.send(f"error in lua command: {e}")

  command_wrapper.__name__ = name
  bot.tree.command(name=name)(command_wrapper)
  lua_commands[name] = lua_function


def load_lua_file(filepath):
  with open(filepath, 'r') as f:
    code = f.read()

  lua.globals().register_command = register_lua_command
  lua.execute(code)


def load_all_lua_scripts():
  lua_scripts_path = os.path.join(os.path.dirname(__file__), '..', 'lua_scripts')

  if not os.path.exists(lua_scripts_path):
    logging.error("lua scripts folder not found")
    return

  for filename in os.listdir(lua_scripts_path):
    if filename.endswith('.lua'):
      filepath = os.path.join(lua_scripts_path, filename)
      load_lua_file(filepath)

  logging.info(f'loaded {len(lua_commands)} lua commands')


def init(token, prefix, guild_id=None):
  global bot

  intents = discord.Intents.default()
  intents.message_content = True
  bot = commands.Bot(command_prefix=prefix, intents=intents)

  @bot.event
  async def on_ready():
    if guild_id:
      guild = discord.Object(id=guild_id)
      bot.tree.copy_global_to(guild=guild)
      await bot.tree.sync(guild=guild)
      logging.info(f'{bot.user} is ready')
      logging.info(f'slash commands synced to guild {guild_id}')
    else:
      await bot.tree.sync()
      logging.info(f'{bot.user} is ready')
      logging.info('slash commands synced globally')

  load_all_lua_scripts()

  return bot
