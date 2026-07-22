import discord
import yaml
from pathlib import Path
import logging
from main.utils.lua_scripting import lua_init
from main.moderation.imagecontent import Detect
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)
_original_slash_command = discord.slash_command

def slash_command(*args, **kwargs):

    kwargs.setdefault(
        "integration_types",
        {
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install
        }
    )

    kwargs.setdefault(
        "contexts",
        {
            discord.InteractionContextType.guild,
            discord.InteractionContextType.bot_dm,
            discord.InteractionContextType.private_channel
        }
    )

    return _original_slash_command(*args, **kwargs)

discord.slash_command = slash_command

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
  bannedword_enabled = config['bannedwords']["enabled"]
  bannedword_list = set(config['bannedwords']["list"])
  daily_bunny_channels = config["animals"]["daily_bunny_channels"]

  bot.daily_bunny_channels = daily_bunny_channels


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


  @bot.event
  async def on_message(message):
      await Detect(message=message, bannedwords=bannedword_list)
  bot.run(discord_token)




