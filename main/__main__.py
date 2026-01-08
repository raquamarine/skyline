import yaml
import os
import logging
try:
    from .utils.lua import init  # for python -m main
except ImportError:
    from utils.lua import init   # for python __main__.py (or when lauching directly via an IDE)

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
  with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

  token = config['discord']['token']
  prefix = config.get('discord', {}).get('prefix', '!')
  bot = init(token, prefix)
  bot.run(token)
