import logging
import discord
from discord.ext import commands
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

geolocator = Nominatim(user_agent="skyline_bot", timeout=5)

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def weather(self, ctx, city: str):
        await ctx.defer()

        try:
            location = geolocator.geocode(city, addressdetails=True)
        except (GeocoderTimedOut, GeocoderUnavailable):
            await ctx.respond("Geopy timed out")
            return

        if not location:
            await ctx.respond("Couldnt find that city")
            return

        lat = location.latitude
        lon = location.longitude

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout:
            await ctx.respond("Timed out while fetching weather")
            return
        except requests.exceptions.RequestException:
            await ctx.respond("Failed to fetch data")
            return

        current = data.get("current")
        if not current:
            await ctx.respond("Current weather is not avaliable")
            return

        country = location.raw.get("address", {}).get("country", "Unknown")
        logging.info(f"{ctx.author} requested weather of {city} - {country}")

        await ctx.respond(
            f"Current weather in {city} ({country}):\n"
            f"Temperature: {current['temperature_2m']} °C\n"
            f"Humidity: {current['relative_humidity_2m']}%\n"
            f"Wind speed: {current['wind_speed_10m']} km/h"
        )

def setup(bot):
    bot.add_cog(Weather(bot))
