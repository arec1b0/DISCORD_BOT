from discord.ext import commands
from .db import DB

async def setup_commands(bot, db):
    #Register commands and uses the passed DB instance
    
    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def add(ctx, *, task_desc):
        await db.add_task(ctx.author.id, task_desc)
        await ctx.send(f"Task added: {task_desc}")

    @bot.command()
    async def list(ctx):
        tasks = await db.get_tasks(ctx.author.id)
        if not tasks:
            await ctx.send("You have no tasks!")
            return
        response = '\n'.join([f"{t[0]}: {t[2]} ({'✓' if t[3] else '✗'})" for t in tasks])
        await ctx.send(response)

    @bot.command()
    async def done(ctx, task_id: str):
        if not task_id.isdigit():
            await ctx.send("Error: The task ID must be an integer.")
            return
        task_id = int(task_id)
        if await db.update_task_status(ctx.author.id, task_id, True):
            await ctx.send(f"Task {task_id} is complete!")
        else:
            await ctx.send(f"Error: Task {task_id} was not found.")

    @bot.command()
    async def delete(ctx, task_id: str):
        if not task_id.isdigit():
            await ctx.send("Error: The task ID must be an integer.")
            return
        task_id = int(task_id)
        if await db.delete_task(ctx.author.id, task_id):
            await ctx.send(f"Task {task_id} has been deleted!")
        else:
            await ctx.send(f"Error: Task {task_id} was not found.")

    @bot.command()
    async def help(ctx):
        help_text = (
            "**Available commands:**\n"
            "`'!add description' - add new task.`\n"
            "`'!list' - show all tasks.`\n"
            "`'!done <number>' - mark task as done.`\n"
            "`'!delete <number>' - delete task.`\n"
            "`'!help' - show list of commands.`"
        )
        await ctx.send(help_text)
