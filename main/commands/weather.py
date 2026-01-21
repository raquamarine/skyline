import logging
import discord
from discord.ext import commands, tasks
import requests
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="skyline_bot")

class Weather(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command()
  async def weather(self, ctx, city):
    await ctx.defer()
    location = geolocator.geocode(city, addressdetails=True)
    if location:
      lat = location.latitude
      lon = location.longitude
      url = f"https://api.open-meteo.com/v1/forecast"
      params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
      }
      response = requests.get(url, params=params)
      data = response.json()
      current = data['current']
      country = location.raw['address'].get('country')
      logging.info(f"{ctx.author} requested weather of {city} - {country}")
      await ctx.respond(f"Current weather in: {city} - {country}: \n"
                        f"Temperature: {current['temperature_2m']} °C \n"
                        f"Humidity: {current['relative_humidity_2m']}% \n"
                        f"Wind speed: {current['wind_speed_10m']} km/h")




def setup(bot):
  bot.add_cog(Weather(bot))
