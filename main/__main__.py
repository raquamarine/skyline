import discord
import yaml
import pathlib
from pathlib import Path
import logging
from main.utils.lua_scripting import lua_init
bot = discord.Bot()
readable_json = False
if __name__ == "__main__":
  #reading cfg
  parent_directory = Path(__file__).resolve().parent.parent
  yaml_file = parent_directory / 'config.yaml'
  with open(yaml_file, 'r') as f:
    config = yaml.safe_load(f)
  # yaml config things

  discord_token = config['discord']["token"]
  #readable_json = config['db']['readable_db'] # WIP DONT UNCOMMENT
  #loads moderation
  bot.load_extension('main.moderation.ban')


  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') #logging cfg, TODO: add yaml config to save to a file log
  lua_init(bot)
  @bot.event
  async def on_ready():
    logging.info(f"logged in as {bot.user}")


  bot.run(discord_token)

