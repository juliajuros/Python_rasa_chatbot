import discord
import requests
import asyncio
from discord.ext import commands

DISCORD_TOKEN = "MTMxODU1MDI2NjgxNDkyMjkxMg.GTkmTJ.y_I0agGOHUjDD1hQR-8E32n_gD6y9uKth0F9cI"

RASA_WEBHOOK_URL = "http://localhost:5005/webhooks/rest/webhook"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} jest gotowy do działania!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_message = message.content
    rasa_response = requests.post(
        RASA_WEBHOOK_URL,
        json={"sender": str(message.author), "message": user_message}
    )

    if rasa_response.status_code == 200:
        responses = rasa_response.json()
        for response in responses:
            await message.channel.send(response.get("text"))
    else:
        await message.channel.send("Sorry, I couldn't connect to the server!")

bot.run(DISCORD_TOKEN)