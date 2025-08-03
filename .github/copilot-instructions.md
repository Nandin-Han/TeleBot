# TeleBot - AI Coding Assistant Instructions

This is a Telegram bot project built with Python 3.13 and python-telegram-bot v22.

## Project Architecture

### Core Structure
- **Entry Point**: `run.py` - Main startup script
- **Bot Core**: `src/bot/main.py` - Application initialization and handler registration
- **Handlers**: `src/bot/handlers/` - Command and message processors
- **Utils**: `src/bot/utils/` - Configuration, logging, and utility functions
- **Config**: Environment variables in `.env` file (copy from `config/.env.example`)

### Key Dependencies
- `python-telegram-bot==22.0` - Telegram Bot API framework (async)
- `python-dotenv==1.0.0` - Environment variable management
- `loguru==0.7.2` - Advanced logging system

## Development Workflows

### Setup Process
1. Copy `config/.env.example` to `.env`
2. Get Bot Token from @BotFather on Telegram
3. Set `TELEGRAM_BOT_TOKEN` in `.env`
4. Install: `pip install -r requirements.txt`
5. Run: `python run.py`

### Bot Token Management
- Obtain from @BotFather: `/newbot` → follow prompts
- Format: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`
- Store in `.env` file (never commit to git)

### Adding New Commands
1. Create handler function in `src/bot/handlers/commands.py`
2. Register in `src/bot/main.py` with `CommandHandler`
3. Use async/await pattern for all handlers

## Project-Specific Patterns

### Handler Structure
```python
async def command_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text("Response")
```

### Configuration Access
- Use `src/bot/utils/config.py` functions
- Environment variables loaded via `python-dotenv`
- Validation in `get_bot_token()` function

### Logging System
- Configured in `src/bot/utils/config.py:setup_logging()`
- Console + file logging with rotation
- Uses `loguru` with structured format

### Error Handling
- Wrap main execution in try/catch in `main.py`
- Log errors with `logger.error()`
- Graceful startup failure messages

## Integration Points

### Telegram API Communication
- All handled through `python-telegram-bot` Application
- Async pattern with `await app.run_polling()`
- Update objects contain user/chat/message data

### External Dependencies
- No database (current simple implementation)
- File logging to `logs/` directory
- Environment-based configuration only

## Testing Strategy
- Test files in `tests/` directory
- Mock Update/Context objects for handler testing
- Use `pytest` with async support

## Common Tasks

### Starting Development
```bash
python run.py  # Start bot with polling
```

### Adding Environment Variables
1. Add to `config/.env.example`
2. Update `config/settings.py` if needed
3. Access via `os.getenv()` in utils

### Extending Functionality
- New handlers → `src/bot/handlers/`
- Utilities → `src/bot/utils/`
- Configuration → `config/settings.py`
- Always maintain async pattern
