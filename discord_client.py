import discord
from config import DISCORD_BOT_TOKEN

def get_discord_client(intents=None):
    if intents is None:
        intents = discord.Intents.default()
        intents.messages = True
    client = discord.Client(intents=intents)
    return client
