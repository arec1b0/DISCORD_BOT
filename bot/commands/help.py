import discord
from typing import List, Tuple
from .base import BaseCommandHandler, CommandContext

class HelpCommandHandler(BaseCommandHandler):
    """Обработчик команды help."""

    def __init__(self, logger=None):
        super().__init__(db=None, logger=logger)
        self.commands: List[Tuple[str, str]] = [
            ("!add <описание>", "Добавить новую задачу"),
            ("!list [страница]", "Показать ваши задачи (с опциональной пагинацией)"),
            ("!done <id>", "Отметить задачу как выполненную"),
            ("!undone <id>", "Отметить задачу как не выполненную"),
            ("!delete <id>", "Удалить задачу"),
            ("!help", "Показать эту справку")
        ]

    async def handle(self, ctx: CommandContext, *args, **kwargs) -> None:
        """Основной метод обработки команды помощи."""
        await self.show_help(ctx)

    async def show_help(self, ctx: CommandContext) -> None:
        """Показать справку по командам."""
        embed = discord.Embed(
            title="📚 Справка по командам Task Manager Bot",
            description="Список доступных команд для управления задачами:",
            color=discord.Color.blue()
        )
        
        for command, description in self.commands:
            embed.add_field(name=command, value=description, inline=False)
        
        embed.set_footer(text="Для получения дополнительной информации обратитесь к документации")
        
        await ctx.send(embed=embed)
        self.logger.info(f"Пользователь {ctx.user_id} запросил справку по командам")