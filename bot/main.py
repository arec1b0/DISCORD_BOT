import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from bot.commands import setup_commands
from bot.db import DB
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Error: The DISCORD_TOKEN environment variable is missing. Make sure that .env contains DISCORD_TOKEN=<your_token>.")

intents = discord.Intents.all()
intents.messages = True  
intents.guilds = True
intents.message_content = True  # Enable guild-related events

# Create an instance of the bot
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Create a database instance
db = DB()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Commands: {list(bot.commands)}')  # Output the list of commands


async def main():
    await db.init()  # Initialize the base before starting the bot
    await setup_commands(bot, db)  # Pass the same database instance to the commands
    await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down the bot gracefully.")
