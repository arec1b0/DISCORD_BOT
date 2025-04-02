import logging
from ..config.settings import BotConfig

class LoggingManager:
    """Менеджер логирования."""

    @staticmethod
    def setup(config: BotConfig) -> logging.Logger:
        """Настройка логирования."""
        logging.basicConfig(
            level=config.log_level,
            format=config.log_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(config.log_file),
            ]
        )
        
        # Отключение шумных логгеров
        logging.getLogger('discord').setLevel(logging.WARNING)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        
        return logging.getLogger('discord_bot') 