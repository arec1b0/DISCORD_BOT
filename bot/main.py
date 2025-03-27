import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from bot.commands import setup_commands
from bot.db import DB  # Import DB class
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Error: DISCORD_TOKEN environment variable is missing. Make sure .env contains DISCORD_TOKEN=<your_token>.")

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable message processing
intents.guilds = True
intents.message_content = True  # Enable access to message content

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Commands: {list(bot.commands)}')  # Output the list of commands

async def main():
    db = DB()  # Create a database instance
    await db.init()  # Initialize the database

    await setup_commands(bot, db)  # Pass db to setup_commands
    await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down the bot gracefully.")
