from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class BotConfig:
    """Конфигурация бота."""
    token: str
    prefix: str
    log_level: int
    log_format: str
    log_file: str

class BotConstants:
    """Константы бота."""
    DEFAULT_PREFIX: str = '!'
    LOG_LEVEL: int = 20  # logging.INFO
    LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    LOG_FILE: str = "discord_bot.log"

class DatabaseConstants:
    """Константы базы данных."""
    DEFAULT_TASK_LIMIT: int = 10
    MAX_DESCRIPTION_LENGTH: int = 500
    DB_PATH: str = 'tasks.db'

class CommandConstants:
    """Константы команд."""
    COOLDOWN_SECONDS: int = 5
    COOLDOWN_RATE: int = 1
    TASKS_PER_PAGE: int = 10

def create_config() -> BotConfig:
    """Создание конфигурации бота."""
    load_dotenv()
    
    token = os.getenv("DISCORD_TOKEN")
    if not token or token == "YOUR_DISCORD_BOT_TOKEN_HERE":
        raise ValueError(
            "DISCORD_TOKEN environment variable is missing or invalid.\n"
            "Please set a valid Discord bot token in your .env file:\n"
            "1. Create or edit your .env file in the project root directory\n"
            "2. Add the line: DISCORD_TOKEN=your_token_here\n"
            "3. Get your bot token from https://discord.com/developers/applications"
        )
        
    return BotConfig(
        token=token,
        prefix=os.getenv("COMMAND_PREFIX", BotConstants.DEFAULT_PREFIX),
        log_level=BotConstants.LOG_LEVEL,
        log_format=BotConstants.LOG_FORMAT,
        log_file=BotConstants.LOG_FILE
    ) 