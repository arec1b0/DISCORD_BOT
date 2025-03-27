# Discord To-Do Bot

A lightweight, production-ready Discord bot designed to streamline task management directly within your Discord server. This bot empowers teams and individuals to manage tasks efficiently through a set of intuitive commands.

---

## Project Overview

The Discord To-Do Bot simplifies task management by allowing users to add, list, complete, and remove tasks via Discord commands. Built with modularity in mind, the bot employs a cog-based architecture and leverages SQLite for persistent task storage.

### Key Features
- **Task Management:** Seamlessly add, complete, and remove tasks.
- **Task Listing:** Display tasks with clear status indicators.
- **Modular Design:** Easy-to-extend cog-based structure for future enhancements.
- **Lightweight & Efficient:** Built using Python and SQLite to maintain performance in small-to-medium deployments.

---

## Installation & Setup

### Cloning the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/krinzhanovskyi/discord-todo-bot.git
cd discord-todo-bot
```

### Setting Up the Environment on Debian

1. **Update Your System:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. **Install Python and pip (if not already installed):**
   ```bash
   sudo apt install python3 python3-pip -y
   ```
3. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Setting Up the Environment on Windows

1. **Ensure Python is Installed:**
   - Download and install Python from the [official website](https://www.python.org/downloads/).  
   - Make sure to check the option to add Python to your PATH during installation.

2. **Open Command Prompt or PowerShell:**
   - Navigate to the repository folder.

3. **Create and Activate a Virtual Environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
   *Note: Use `.\venv\Scripts\activate` if you are using PowerShell.*

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### Setting Up the .env File Securely

1. **Create a `.env` file** in the root directory.
2. **Add the required environment variables.** Ensure that the file is kept secure and is included in `.gitignore` to avoid accidental commits of sensitive data.

**Example .env File:**
```env
# Discord Bot Token (keep this secret!)
DISCORD_TOKEN=your_discord_bot_token_here

# Command prefix for the bot
COMMAND_PREFIX=!

# Path to the SQLite database file (default: tasks.db)
DB_PATH=tasks.db

# Enable or disable debug mode (true/false)
DEBUG_MODE=false
```

---

## Usage Guide

Start the bot with the following command:
```bash
python bot.py
```

### Bot Commands

- **`!addtask [task description]`**  
  *Adds a new task.*  
  **Expected Output:**  
  `✅ Task added with ID <task_id>.`

- **`!removetask [task ID]`**  
  *Removes an existing task.*  
  **Expected Output:**  
  `🗑️ Task <task_id> removed.` or `❌ No task found.`

- **`!complete [task ID]`**  
  *Marks a task as completed.*  
  **Expected Output:**  
  `✅ Task <task_id> marked as completed.` or `❌ No task found.`

- **`!listtasks`**  
  *Lists all current tasks along with their completion status.*  
  **Expected Output:**  
  A formatted list displaying each task with an identifier, description, and a status indicator (✅/❌).

---

## Development & Contribution

### Code Structure Overview

- **`cogs/`**  
  Contains command modules (e.g., task-related commands).

- **`utils/`**  
  Includes utility modules such as the `TaskManager` for database operations.

- **`bot.py`**  
  The entry point for the bot, responsible for configuration and loading cogs.

- **`config.py`**  
  Centralized configuration handling for environment variables and settings.

### Guidelines for Adding New Features

- **Maintain Modularity:**  
  Develop new features as separate cogs or modules to ensure scalability and ease of maintenance.

- **Embrace Asynchronous Practices:**  
  Future enhancements should leverage asynchronous operations to prevent blocking the event loop, especially when integrating with Discord's API.

- **Testing:**  
  Ensure all new features include appropriate unit tests and integrate smoothly with existing functionalities.

- **Peer Reviews:**  
  All contributions must undergo thorough code reviews focusing on security, performance, and maintainability.

---

## Error Handling & Troubleshooting

### Common Issues

- **Missing Discord Token:**  
  If the bot fails to start, verify that the `DISCORD_TOKEN` is correctly set in your `.env` file.

- **Dependency Conflicts:**  
  Ensure that you're using the correct Python version and that your virtual environment is active. Check for version mismatches in `requirements.txt`.

### Debugging Tips

- **Enable Debug Mode:**  
  Set `DEBUG_MODE=true` in your `.env` file to receive detailed logs.

- **Review Logs:**  
  Monitor terminal outputs for error messages to pinpoint issues.

- **Community Support:**  
  Engage with GitHub issues or relevant Discord developer communities if you encounter persistent problems.

---

## License & Credits

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributors
- **Oleksandr Krizhanovskyi** – Project Lead & Primary Developer
- **Key Contributors:**  
  - [Daniil](github.com/dkrizhanovskyi) - Technical Advisor
