import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from bot.commands import setup_commands
from bot.db import DB   # import the DB class
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Ошибка: переменная окружения DISCORD_TOKEN отсутствует. Убедитесь, что .env cодержит DISCORD_TOKEN=<ваш_токен>.")

# Define intents
intents = discord.Intents.default()
intents.messages = False  # Disable unnecessary permissions
intents.guilds = True
intents.message_content = True  # Enable guild-related events

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    # Initialize the database tables
    db = DB()
    await db.init()

    await setup_commands(bot)
    await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down the bot gracefully.")