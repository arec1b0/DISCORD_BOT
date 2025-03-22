# Discord Task Manager Bot

A lightweight Discord bot designed to help users create, list, complete, and delete tasks. Powered by `discord.py` with a simple SQLite database for seamless task management.

## Overview

This project offers a straightforward approach to to-do list management within a Discord server:
- **Local storage** of tasks via SQLite (no external DB required).
- **Simple command-based interface** for quick and interactive task management.
- **Customizable command prefix** (default: `!`).
- **Modular structure** split into distinct files for clarity and maintainability.

## Main Features

1. **Add Tasks**  
   Create new tasks tied to your Discord user ID.
2. **List Tasks**  
   Retrieve all tasks you have created, including completed and pending ones.
3. **Mark Tasks as Done**  
   Quickly indicate a task’s completion status.
4. **Delete Tasks**  
   Remove tasks entirely when no longer needed.
5. **Customizable Commands**  
   Extend or modify existing commands without tangling with the main bot logic.

## Repository Structure

```
.
├── bot/
│   ├── commands.py     # Defines and registers all bot commands
│   ├── db.py           # SQLite database handling
│   └── main.py         # Bot entry point, Discord event handling
├── .gitignore          # Ignored files (.env, __pycache__, etc.)
├── AUDIT.md            # Security audit report and recommendations
├── bandit_report.html  # Bandit static analysis results
└── requirements.txt    # Python dependencies
```

## Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/krinzhanovskyi/DISCORD_BOT.git
   cd DISCORD_BOT
   ```
   
2. **Create a Virtual Environment (Optional but Recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix-like systems
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**  
   - Create a `.env` file in the project root.
   - Add your Discord bot token:
     ```
     DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
     ```
   - (Optional) Adjust other environment variables as needed.

5. **Run the Bot**  
   ```bash
   python -m bot.main
   ```
   Once the bot connects, you should see a console message indicating it has successfully logged in.

## Usage Examples

Below are the core commands. By default, all commands start with `!`. You can change this prefix in `main.py`.

1. **Add a Task**
   ```
   !add Buy groceries
   ```
   Creates a new task with the description “Buy groceries.”

2. **List All Tasks**
   ```
   !list
   ```
   Shows all tasks associated with your user ID. Completed tasks are marked with a `✓`.

3. **Mark a Task as Done**
   ```
   !done 1
   ```
   Marks task #1 as completed, if it exists.

4. **Delete a Task**
   ```
   !delete 1
   ```
   Deletes task #1 entirely, if it exists.

5. **View Available Commands**
   ```
   !help
   ```
   Displays a list of all commands and their usage.

## Security Considerations

- **Token Management**  
  Your Discord bot token is read from a local `.env` file. Ensure you never commit this token to version control.
- **SQL Injection Mitigation**  
  The bot uses parameterized queries, but always double-check user inputs (especially `task_id`) for validity.
- **Bot Permissions**  
  By default, the bot requests `message_content` intent, which may be broader than necessary. Limit permissions whenever possible.
- **Rate Limiting**  
  Currently, commands can be spammed. Consider implementing [Discord cooldowns](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=cooldown#discord.ext.commands.cooldown) or other throttling mechanisms.

## Further Improvements

- **Automate Security Checks**  
  The included `AUDIT.md` and `bandit_report.html` detail potential vulnerabilities and best practices. Regularly run tools like `bandit`, `safety`, or `pip-audit` in a CI/CD pipeline.
- **Add More Commands or Features**  
  For instance, a “due date” or “priority” field to tasks.
- **Deploy on a Cloud Service**  
  Consider running the bot continuously on platforms like Heroku, AWS, or other Docker-based services.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with any feature requests or bug fixes. Be sure to adhere to any coding standards and best practices outlined in the project.
