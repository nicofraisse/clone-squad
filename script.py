import discord
import os
import openai
from dotenv import load_dotenv


load_dotenv()

discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

openai.api_key = openai_api_key

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != 'general':
        return

    prompt = f"Speak like Nic: {message.content}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    await message.channel.send(response.choices[0].message['content'])

client.run(discord_bot_token)
