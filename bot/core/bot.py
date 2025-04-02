import discord
from discord.ext import commands
import asyncio
import signal
from typing import Optional

from ..config.settings import BotConfig
from ..database.base import DatabaseManager
from .logging import LoggingManager
from ..commands.task import TaskCommandHandler
from ..commands.help import HelpCommandHandler
from ..commands.base import CommandContext

class BotManager:
    """Менеджер бота."""

    def __init__(self, config: BotConfig):
        self.config = config
        self.logger = LoggingManager.setup(config)
        self.bot: Optional[commands.Bot] = None
        self.db: Optional[DatabaseManager] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.task_handler: Optional[TaskCommandHandler] = None
        self.help_handler: Optional[HelpCommandHandler] = None

    async def initialize(self) -> None:
        """Инициализация бота."""
        self.logger.info("Starting bot initialization")
        
        # Настройка интентов
        intents = discord.Intents.default()
        intents.guilds = True
        intents.message_content = True  # Это привилегированный интент!
        
        # Сообщение с инструкцией по включению интентов
        self.privileged_intents_instructions = """
ОШИБКА: Для работы бота требуются привилегированные интенты Discord!

Чтобы исправить ошибку, выполните следующие шаги:
1. Перейдите на https://discord.com/developers/applications
2. Выберите вашего бота
3. Перейдите в раздел "Bot" на левой панели
4. Прокрутите вниз до раздела "Privileged Gateway Intents"
5. Включите опцию "MESSAGE CONTENT INTENT"
6. Нажмите "Save Changes"
7. Перезапустите бота

Альтернативно, если вы не хотите включать привилегированные интенты,
отредактируйте файл bot/core/bot.py и установите intents.message_content = False
"""
        
        # Создание экземпляров
        self.bot = commands.Bot(command_prefix=self.config.prefix, intents=intents, help_command=None)
        self.loop = asyncio.get_event_loop()

    async def setup_signal_handlers(self) -> None:
        """Настройка обработчиков сигналов."""
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.loop.add_signal_handler(
                sig, 
                lambda sig=sig: asyncio.create_task(self.shutdown(sig))
            )

    async def setup_bot_events(self) -> None:
        """Настройка событий бота."""
        @self.bot.event
        async def on_ready():
            """Обработка успешного запуска бота."""
            self.logger.info(f"Bot connected as {self.bot.user}")
            self.logger.info(f"Connected to {len(self.bot.guilds)} guilds")
            await self.bot.change_presence(
                activity=discord.Game(name=f"Type {self.config.prefix}help")
            )

        @self.bot.event
        async def on_command_error(ctx, error):
            """Обработка ошибок команд."""
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"⏱️ Подождите! Попробуйте снова через {error.retry_after:.1f} секунд.")
                self.logger.warning(f"User {ctx.author.id} hit cooldown for {ctx.command}")
            else:
                await ctx.send("❌ Произошла ошибка при обработке команды.")
                self.logger.error(f"Command error: {error}")

    async def setup_commands(self) -> None:
        """Настройка команд бота."""
        from ..config.settings import CommandConstants
        
        @self.bot.command()
        @commands.cooldown(CommandConstants.COOLDOWN_RATE, CommandConstants.COOLDOWN_SECONDS, commands.BucketType.user)
        async def add(ctx, *, task_desc):
            """Добавление новой задачи."""
            command_ctx = CommandContext(ctx.author.id, ctx.channel, ctx.send, self.logger)
            await self.task_handler.add_task(command_ctx, task_desc)

        @self.bot.command()
        @commands.cooldown(CommandConstants.COOLDOWN_RATE, CommandConstants.COOLDOWN_SECONDS, commands.BucketType.user)
        async def list(ctx, page: int = 1):
            """Вывод списка задач с пагинацией."""
            command_ctx = CommandContext(ctx.author.id, ctx.channel, ctx.send, self.logger)
            await self.task_handler.list_tasks(command_ctx, page)

        @self.bot.command()
        @commands.cooldown(CommandConstants.COOLDOWN_RATE, CommandConstants.COOLDOWN_SECONDS, commands.BucketType.user)
        async def done(ctx, task_id: str):
            """Отметить задачу как выполненную."""
            command_ctx = CommandContext(ctx.author.id, ctx.channel, ctx.send, self.logger)
            await self.task_handler.mark_task_status(command_ctx, task_id, True)

        @self.bot.command()
        @commands.cooldown(CommandConstants.COOLDOWN_RATE, CommandConstants.COOLDOWN_SECONDS, commands.BucketType.user)
        async def undone(ctx, task_id: str):
            """Отметить задачу как не выполненную."""
            command_ctx = CommandContext(ctx.author.id, ctx.channel, ctx.send, self.logger)
            await self.task_handler.mark_task_status(command_ctx, task_id, False)

        @self.bot.command()
        @commands.cooldown(CommandConstants.COOLDOWN_RATE, CommandConstants.COOLDOWN_SECONDS, commands.BucketType.user)
        async def delete(ctx, task_id: str):
            """Удаление задачи."""
            command_ctx = CommandContext(ctx.author.id, ctx.channel, ctx.send, self.logger)
            await self.task_handler.delete_task(command_ctx, task_id)

        @self.bot.command()
        @commands.cooldown(CommandConstants.COOLDOWN_RATE, CommandConstants.COOLDOWN_SECONDS, commands.BucketType.user)
        async def help(ctx):
            """Показать справку по командам."""
            command_ctx = CommandContext(ctx.author.id, ctx.channel, ctx.send, self.logger)
            await self.help_handler.show_help(command_ctx)

    async def cleanup(self) -> None:
        """Очистка ресурсов."""
        if self.bot and not self.bot.is_closed():
            await self.bot.close()
            self.logger.info("Bot connection closed")
        
        if self.db:
            await self.db.close()
            self.logger.info("Database connection closed")

    async def shutdown(self, sig: signal.Signals) -> None:
        """Обработка graceful shutdown."""
        self.logger.info(f"Received shutdown signal {sig.name}, cleaning up...")
        
        tasks = [task for task in asyncio.all_tasks() 
                if task is not asyncio.current_task()]
        
        await self.cleanup()
        
        # Отмена отложенных задач
        for task in tasks:
            task.cancel()
        
        await asyncio.gather(*tasks, return_exceptions=True)
        self.logger.info("All tasks have been cancelled")
        
        self.loop.stop()

    async def run(self) -> int:
        """Запуск бота."""
        try:
            await self.initialize()
            await self.setup_signal_handlers()
            await self.setup_bot_events()
            await self.setup_commands()
            
            self.logger.info("Bot starting...")
            try:
                await self.bot.start(self.config.token)
                return 0
            except discord.errors.PrivilegedIntentsRequired:
                # Вывод информативного сообщения при ошибке с привилегированными интентами
                print(self.privileged_intents_instructions)
                self.logger.critical("Bot requires privileged intents that are not enabled in Discord Developer Portal")
                return 1
            
        except Exception as e:
            self.logger.critical(f"Failed to start bot: {e}")
            return 1
        finally:
            await self.cleanup() 