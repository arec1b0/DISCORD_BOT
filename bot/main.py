import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from bot.commands import setup_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable specific intents as needed
intents.message_content = True  # Required for reading message content

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

setup_commands(bot)

# Example event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(TOKEN)
