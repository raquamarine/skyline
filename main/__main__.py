import discord
import yaml
from pathlib import Path
import logging
from main.utils.lua_scripting import lua_init
bot = discord.Bot()


def loadextensions(*args):
  for item in args:
    logging.info(f"Loading: {item}")
    bot.load_extension(item)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                      force=True)

  #reading cfg
  parent_directory = Path(__file__).resolve().parent.parent
  yaml_file = parent_directory / 'config.yaml'
  try:
    with open(yaml_file, 'r') as f:
      config = yaml.safe_load(f)
  except:
    logging.error("No config file found!")

  # yaml config values
  discord_token = config['discord']["token"]
  lua_enabled = config['bot']["lua_enabled"]
  customstatus = config['discord']["status"]


  cogs = ["main.moderation.ban",
          "main.moderation.kick",
          "main.moderation.mute",
          "main.moderation.warn",
          "main.commands.animals",
          "main.commands.sstv",
          "main.commands.weather",
          "main.commands.tf2"]

  loadextensions(*cogs)

  if lua_enabled:
    lua_init(bot)


  @bot.event
  async def on_ready():
    logging.info(f"logged in as {bot.user}")

    if customstatus:
      logging.info(f"Setting presence to: {customstatus}")
      await bot.change_presence(activity=discord.CustomActivity(name=customstatus))


  bot.run(discord_token)



