import discord
import yaml
import pathlib
from pathlib import Path
import logging
from utils.lua_scripting import init
bot = discord.Bot()
if __name__ == "__main__":
  #reading cfg
  parent_directory = Path(__file__).resolve().parent.parent
  yaml_file = parent_directory / 'config.yaml'
  with open(yaml_file, 'r') as f:
    config = yaml.safe_load(f)
  #getting tokens
  discord_token = config['discord']["token"]
  #print(discord_token) DONT UNCOMMENT THIS

  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') #logging cfg, TODO: add yaml config to save to a file log
  init(bot)
  @bot.event
  async def on_ready():
    logging.info(f"logged in as {bot.user}")

  bot.run(discord_token)

