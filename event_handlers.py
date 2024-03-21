from openai_client import generate_response

async def on_ready():
    print(f'Logged in as {client.user}')

async def on_message(message):
    if message.author == client.user or message.channel.name != 'general':
        return

    prompt = f"Speak like Nic: {message.content}"
    response_content = generate_response(prompt)
    await message.channel.send(response_content)
