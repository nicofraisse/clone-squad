import discord
import os
from dotenv import load_dotenv
import openai
from discord import utils
import time


class NicBot:
    def __init__(self):

        load_dotenv()
        self.discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.custom_prompt = self.load_custom_prompt()



        openai.api_key = self.openai_api_key
        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')

        @self.client.event
        async def on_message(message):
            print(f'Message from {message.author}: {message.content}')


            if self.client.user in message.mentions and message.author != self.client.user:
                print(f'I was mentioned by {message.author}!')

                full_prompt = f"{self.custom_prompt} (by {message.author.display_name}): {message.content}"
                prompt = {
                    'role': 'user',
                    'content': full_prompt
                }

                try:
                    print('will interact...')

                    response = openai.ChatCompletion.create(
                        model = 'gpt-3.5-turbo',
                        messages=[prompt]
                    )
                    time.sleep(1)
                    chatbot_response = response.choices[0].message['content']
                    print(f"Chatbot response: {chatbot_response}")

                    await message.channel.send(chatbot_response)

                except Exception as e:
                    print(f"Error while generating response: {e}")
                    await message.channel.send("Sorry, I encountered an issue while generating a response.")

    def load_custom_prompt(self):
        try:
            with open('custom_prompt.txt', 'r') as file:
                custom_prompt = file.read().strip()
            return custom_prompt
        except FileNotFoundError:
            print('Custom prompt file not found. Using default prompt.')
            return "Respond thoughtfully to the following query:"


    def run(self):
        self.client.run(self.discord_bot_token)

if __name__ == "__main__":
    bot = NicBot()
    bot.run()
