import discord
import requests
import json
from weather import *

token = 'MTA4ODYxNjM0ODk3Mzc5NzQ3Nw.GVYy0P.qbDrGInqhGfR5ggsMNpN_arB4X29GwCoWvKvVQ'
api_key = 'ea97df2c2ec8f25d19496f0663663094'

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

command_prefix = '#'

# Listening to #location~
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='#location~'))

@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(command_prefix):
        if len(message.content.replace(command_prefix, '')) >= 1:
            location = message.content.replace(command_prefix, '').lower()
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main']) # main data
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))

client.run(token)
