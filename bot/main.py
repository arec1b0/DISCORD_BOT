import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from bot.commands import setup_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Ошибка: переменная окружения DISCORD_TOKEN отсутствует. Убедитесь, что .env cодержит DISCORD_TOKEN=<ваш_токен>.")

# Define intents
intents = discord.Intents.default()
intents.messages = False  # Disable unnecessary permissions
intents.guilds = True  # Enable guild-related events

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

setup_commands(bot)

# Example event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
                     
bot.run(TOKEN)
