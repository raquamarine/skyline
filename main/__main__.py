import discord
import yaml
import pathlib
from pathlib import Path
import logging
from main.utils.lua_scripting import lua_init
bot = discord.Bot()



if __name__ == "__main__":
  #reading cfg
  parent_directory = Path(__file__).resolve().parent.parent
  yaml_file = parent_directory / 'config.yaml'

  try:
    with open(yaml_file, 'r') as f:
      config = yaml.safe_load(f)
  except:
    print("No config file found!")


  # yaml config things
  discord_token = config['discord']["token"]


  #loads moderation stuff
  bot.load_extension('main.moderation.ban')
  bot.load_extension('main.moderation.kick')
  bot.load_extension('main.moderation.mute')
  bot.load_extension('main.moderation.warn')

  #normal stuff
  bot.load_extension('main.commands.animals')


  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') #logging cfg, TODO: add yaml config to save to a file log
  lua_init(bot)
  @bot.event
  async def on_ready():
    logging.info(f"logged in as {bot.user}")


  bot.run(discord_token)

