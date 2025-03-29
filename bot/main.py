import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from bot.commands import setup_commands
from bot.db import DB  # Import DB class
import asyncio
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Error: DISCORD_TOKEN environment variable is missing. Make sure .env contains DISCORD_TOKEN=<your_token>.")

# Define necessary intents
intents = discord.Intents.default()
intents.guilds = True   # Sufficient for working with guilds
intents.message_content = True  # Necessary access to message content

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    logging.info(f"Bot started as {bot.user}")
    logging.info(f"Connected to {len(bot.guilds)} guilds")
    logging.info(f"By 4|_E><")

async def main():
    db = DB()  # Create a database instance
    await db.init()   # Initialize the database

    await setup_commands(bot, db)  # Pass db to setup_commands
    await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Shutting down the bot gracefully.")
