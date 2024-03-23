import os
import time
from dotenv import load_dotenv
from functools import wraps
import discord
import openai

class NicBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.custom_prompt = self.load_custom_prompt()

        # Initialize last_api_call_time
        self.last_api_call_time = 0

        # Initialize Discord client
        openai.api_key = self.openai_api_key
        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True
        self.client = discord.Client(intents=intents)

        # Register event handlers
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    @staticmethod
    def rate_limited_api_call(min_interval=1):
        """
        Decorator to rate-limit functions making API calls to OpenAI.
        Ensures that at least `min_interval` seconds have passed between calls.
        """

        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                current_time = time.time()
                if current_time - self.last_api_call_time < min_interval:
                    raise Exception("API call rate limit exceeded. Please wait before making another call.")
                result = await func(self, *args, **kwargs)
                self.last_api_call_time = time.time()
                return result
            return wrapper
        return decorator

    def load_custom_prompt(self):
        try:
            with open("custom_prompt.txt", "r") as file:
                custom_prompt = file.read().strip()
            return custom_prompt
        except FileNotFoundError:
            print("custom_prompt.txt not found. Using default prompt.")
            default_prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
            return  default_prompt

    async def on_ready(self):
        print(f"Bot is ready. Logged in as {self.client.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

        # Bot should respond only if it is mentioned by a user (and not by itself)
        bot_mentioned = self.client.user in message.mentions
        is_bot = message.author == self.client.user
        if bot_mentioned and not is_bot:
            print(f"I was mentioned by {message.author}!")
            await self.respond_to_mention(message)

    @rate_limited_api_call(min_interval=1)
    async def respond_to_mention(self, message):
        try:
            prompt = self.get_full_prompt(message)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            chatbot_response = response.choices[0].message["content"]
            print(f"Chatbot response: {chatbot_response}")
            await message.channel.send(chatbot_response)
        except Exception as e:
            print(f"Error while generating response: {e}")
            await message.channel.send("Sorry, I encountered an issue while generating a response.")

    def get_full_prompt(self, incoming_message):
        return f"{self.custom_prompt} (by {incoming_message.author.display_name}): {incoming_message.content}"

    def run(self):
        self.client.run(self.discord_bot_token)

if __name__ == "__main__":
    bot = NicBot()
    bot.run()
