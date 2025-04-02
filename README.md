# Discord Task Manager Bot

A lightweight Discord bot designed to help users create, list, complete, and delete tasks. Powered by `discord.py` with a simple SQLite database for seamless task management.

## Overview

This project offers a straightforward approach to to-do list management within a Discord server:

- **Local storage** of tasks via SQLite (no external DB required).
- **Simple command-based interface** for quick and interactive task management.
- **Customizable command prefix** (default: `!`).
- **Object-Oriented Architecture** for better maintainability and extensibility.
- **Comprehensive Test Suite** with unit, integration, and E2E tests.

## Main Features

1. **Add Tasks**  
   Create new tasks tied to your Discord user ID.
2. **List Tasks**  
   Retrieve all tasks you have created, including completed and pending ones.
3. **Mark Tasks as Done**  
   Quickly indicate a task's completion status.
4. **Delete Tasks**  
   Remove tasks entirely when no longer needed.
5. **Customizable Commands**  
   Extend or modify existing commands without tangling with the main bot logic.

## Repository Structure

```text
.
├── bot/
│   ├── __init__.py           # Package initializer
│   ├── config/               # Configuration settings
│   │   ├── __init__.py       
│   │   └── settings.py       # Bot and database settings
│   ├── core/                 # Core functionality
│   │   ├── __init__.py       
│   │   ├── bot.py            # Main bot manager class
│   │   └── logging.py        # Logging configuration
│   ├── database/             # Database management
│   │   ├── __init__.py       
│   │   ├── base.py           # Abstract database interface
│   │   ├── models.py         # Data models
│   │   └── sqlite.py         # SQLite implementation
│   ├── commands/             # Bot commands
│   │   ├── __init__.py       
│   │   ├── base.py           # Base command handler
│   │   ├── task.py           # Task-related commands
│   │   └── help.py           # Help command
│   ├── utils/                # Utilities
│   │   └── __init__.py       
│   └── main.py               # Application entry point
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Common test fixtures
│   ├── unit/                 # Unit tests
│   │   ├── __init__.py
│   │   ├── test_database.py  # Database tests
│   │   └── test_commands.py  # Command tests
│   ├── integration/          # Integration tests
│   │   ├── __init__.py
│   │   └── test_bot_db.py    # Bot-DB integration tests
│   └── e2e/                  # End-to-end tests
│       ├── __init__.py
│       └── test_bot_flow.py  # Complete workflow tests
├── .gitignore                # Ignored files (.env, __pycache__, etc.)
├── AUDIT.md                  # Security audit report and recommendations
├── bandit_report.html        # Bandit static analysis results
└── requirements.txt          # Python dependencies
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

     ```env
     DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
     ```

5. **Run the Bot**  

   ```bash
   python -m bot.main
   ```

   Once the bot connects, you should see a console message indicating it has successfully logged in.

## Usage Examples

Below are the core commands. By default, all commands start with `!`. You can change this prefix through the environment variable `COMMAND_PREFIX`.

1. **Add a Task**

   ```text
   !add Buy groceries
   ```

   Creates a new task with the description "Buy groceries."

2. **List All Tasks**

   ```text
   !list
   ```

   Shows all tasks associated with your user ID. Completed tasks are marked with a `✓`.

3. **Mark a Task as Done**

   ```text
   !done 1
   ```

   Marks task #1 as completed, if it exists.

4. **Mark a Task as Not Done**

   ```text
   !undone 1
   ```

   Marks task #1 as incomplete, if it exists.

5. **Delete a Task**

   ```text
   !delete 1
   ```

   Deletes task #1 entirely, if it exists.

6. **View Available Commands**

   ```text
   !help
   ```

   Displays a list of all commands and their usage.

## Testing

The project includes a comprehensive test suite with unit, integration, and end-to-end tests:

1. **Running All Tests**

   ```bash
   pytest tests/ -v --asyncio-mode=auto
   ```

2. **Running Specific Test Categories**

   ```bash
   # Unit tests only
   pytest tests/unit/ -v --asyncio-mode=auto

   # Integration tests only
   pytest tests/integration/ -v --asyncio-mode=auto

   # End-to-end tests only
   pytest tests/e2e/ -v --asyncio-mode=auto
   ```

3. **Code Coverage**

   ```bash
   pytest tests/ --cov=bot --cov-report=term --cov-report=html --asyncio-mode=auto
   ```

## Security Considerations

- **Token Management**  
  Your Discord bot token is read from a local `.env` file. Ensure you never commit this token to version control.
- **SQL Injection Mitigation**  
  The bot uses parameterized queries and validates all inputs to prevent SQL injection attacks.
- **Bot Permissions**  
  By default, the bot requests `message_content` intent, which may be broader than necessary. Limit permissions whenever possible.
- **Rate Limiting**  
  Commands use Discord's built-in cooldown mechanism to prevent abuse.
- **Error Handling**
  Comprehensive error handling prevents unexpected crashes and potential information leakage.

## Architecture

The bot follows clean code and object-oriented programming principles:

1. **Separation of Concerns**
   - Configuration is separated from logic
   - Database operations are abstracted behind interfaces
   - Commands are encapsulated in their own classes

2. **SOLID Principles**
   - Single Responsibility: Each class has a specific purpose
   - Open/Closed: Extend functionality without modifying existing code
   - Liskov Substitution: Database implementations are interchangeable
   - Interface Segregation: Clean, focused interfaces
   - Dependency Inversion: High-level modules don't depend on low-level modules

3. **Design Patterns**
   - Command Pattern for Discord commands
   - Repository Pattern for database access
   - Dependency Injection for better testability

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with any feature requests or bug fixes. Be sure to adhere to any coding standards and best practices outlined in the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
