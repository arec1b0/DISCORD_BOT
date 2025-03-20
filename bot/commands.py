from .db import DB


def setup_commands(bot):
    db = DB()

    @bot.command()
    async def add(ctx, *, task_desc):
        db.add_task(ctx.author.id, task_desc)
        await ctx.send(f"Задача добавлена: {task_desc}")

    @bot.command()
    async def list(ctx):
        tasks = db.get_tasks(ctx.author.id)
        if not tasks:
            await ctx.send("У вас нет задач!")
            return
        response = '\n'.join([f"{t[0]}: {t[2]} ({'✓' if t[3] else '✗'})" for t in tasks])
        await ctx.send(response)

    @bot.command()
    async def done(ctx, task_id: int):
        db.update_task_status(ctx.author.id, task_id, True)
        await ctx.send(f"Задача {task_id} выполнена!")

    @bot.command()
    async def delete(ctx, task_id: int):
        db.delete_task(ctx.author.id, task_id)
        await ctx.send(f"Задача {task_id} удалена!")

    @bot.command()
    async def help(ctx):
        help_text = (
            "**Доступные команды:**\n"
            "`!add <описание>` — добавить новую задачу.\n"
            "`!list` — показать все задачи.\n"
            "`!done <номер>` — отметить задачу как выполненную.\n"
            "`!delete <номер>` — удалить задачу.\n"
            "`!help` — показать список команд."
        )
        await ctx.send(help_text)