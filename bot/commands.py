from discord.ext import commands
from bot.db import DB

async def setup_commands(bot, db: DB):  # Pass db as a dependency
    await db.init()  # Ensure the database tables exist

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def add(ctx, *, task_desc):
        await db.add_task(ctx.author.id, task_desc)
        await ctx.send(f"✅Task added: {task_desc}")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def list(ctx):
        tasks = await db.get_tasks(ctx.author.id)
        if not tasks:
            await ctx.send("You have no tasks!")
            return
        response = '\n'.join([f"{t[0]}: {t[2]} ({'✓' if t[3] else '✗'})" for t in tasks])
        await ctx.send(response)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def done(ctx, task_id: str):
        if not task_id.isdigit():
            await ctx.send("❌Error: Task ID must be an integer.")
            return
        task_id = int(task_id)
        if await db.mark_task_done(ctx.author.id, task_id, True):
            await ctx.send(f"✅Task {task_id} completed!")
        else:
            await ctx.send(f"❌Error: Task {task_id} not found.")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def delete(ctx, task_id: str):
        if not task_id.isdigit():
            await ctx.send("❌Error: Task ID must be an integer.")
            return
        task_id = int(task_id)
        if await db.delete_task(ctx.author.id, task_id):
            await ctx.send(f"🗑️Task {task_id} deleted!")
        else:
            await ctx.send(f"❌Error: Task {task_id} not found.")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(ctx):
        help_text = (
            ":scroll:**Available Commands:**\n"
            "`!add <description>` — Add a new task.\n"
            "`!list` — Show all tasks.\n"
            "`!done <id>` — Mark a task as completed.\n"
            "`!delete <id>` — Delete a task.\n"
            "`!help` — Show the list of commands."
        )
        await ctx.send(help_text)