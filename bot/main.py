import sys
import asyncio
import logging

from .config.settings import create_config
from .core.bot import BotManager
from .database.sqlite import SQLiteDatabaseManager
from .commands.task import TaskCommandHandler
from .commands.help import HelpCommandHandler

async def main() -> int:
    """Точка входа в приложение."""
    try:
        # Пробуем загрузить конфигурацию
        try:
            config = create_config()
        except ValueError as config_error:
            # Если произошла ошибка конфигурации, выводим понятное сообщение
            print(f"Fatal error: {config_error}")
            return 1
            
        # Инициализируем бот-менеджер
        bot_manager = BotManager(config)
        
        # Настраиваем базу данных
        bot_manager.db = SQLiteDatabaseManager()
        await bot_manager.db.init()
        
        # Настраиваем обработчики команд
        bot_manager.task_handler = TaskCommandHandler(bot_manager.db, bot_manager.logger)
        bot_manager.help_handler = HelpCommandHandler(logger=bot_manager.logger)
        
        # Запускаем бота
        return await bot_manager.run()
        
    except Exception as e:
        # Обрабатываем другие ошибки
        logger = logging.getLogger('discord_bot')
        logger.critical(f"Fatal error: {e}")
        print(f"Произошла ошибка при запуске бота: {e}")
        return 1

if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)