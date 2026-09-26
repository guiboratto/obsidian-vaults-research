# Hermes Bot Setup Guide

**Goal:** Deploy Telegram bot that uses the Obsidian knowledge base.

---

## Prerequisites

### 1. Install Dependencies

```bash
# Python packages
pip install python-telegram-bot langchain langchain-community langchain-ollama chromadb

# Required packages
pip install python-dotenv pyyaml
```

### 2. Telegram Bot Token

1. Create a bot via [@BotFather](https://t.me/BotFather)
2. Get your bot token
3. Save to `.env` file:

```bash
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook
EOF
```

### 3. Ollama Running

Ensure Ollama is running:

```bash
# On the PC (LarkBox)
ollama serve

# Or on the phone (if using local inference)
ollama serve
```

### 4. Verify ChromaDB Setup

```bash
python scripts/setup-chromadb.py
```

---

## Bot Implementation

### 1. Create Bot File

Create `hermes_bot.py`:

```python
#!/usr/bin/env python3
"""
Hermes Telegram Bot - Obsidian Knowledge Base Interface

This bot:
1. Receives questions from Telegram
2. Routes them to the appropriate domain
3. Loads relevant context from ChromaDB
4. Activates the appropriate agent
5. Returns the response
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

try:
    from telegram import Update
    from telegram.ext import (
        ApplicationBuilder,
        CommandHandler,
        MessageHandler,
        filters,
        ContextTypes
    )
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error importing required packages: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Import orchestrator
sys.path.append(str(Path(__file__).parent))
from orchestrator import ObsidianOrchestrator


class HermesBot:
    """Hermes Telegram bot using Obsidian knowledge base."""
    
    def __init__(self, token: str, vault_path: str = "./unified-brain", chroma_path: str = "./chromadb"):
        self.token = token
        self.vault_path = vault_path
        self.chroma_path = chroma_path
        self.orchestrator = None
        
        self._initialize_bot()
    
    def _initialize_bot(self):
        """Initialize the Telegram bot and orchestrator."""
        print("Initializing Hermes Bot...")
        
        # Initialize orchestrator
        self.orchestrator = ObsidianOrchestrator(
            vault_path=self.vault_path,
            chroma_path=self.chroma_path
        )
        
        print("✓ Hermes Bot initialized")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """👋 Привіт! Я твоій Obsidian-мозок.

Я можу допомогти з:
• Плануванням проектів та ініціатив
• Підготовкою до зустрічей
• Аналізом рішень
• Пошуком інформації у твоїй базі знань
• Джерелінгом та створенням контенту

Запитай щось!"""

        await update.message.reply_text(welcome_message)
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = """📋 Доступні команди:

/start - Початок роботи
/help - Ця довідка
/reset - Очистити контекст

Типові питання:
• "Що мені потрібно робити сьогодні?"
• "Підготуйся до зустрічі з командою"
• "Які ідеї є для нового проекту?"
• "Поради для налаштування звичок?"
• "Підсумок за тиждень"

Я використовую твою Obsidian базу знань для відповідей!"""

        await update.message.reply_text(help_message)
    
    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reset command."""
        await update.message.reply_text("Контекст очищено. Готовий до нових питань! 🔄")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        question = update.message.text
        
        if not question:
            return
        
        try:
            # Get answer from orchestrator
            result = self.orchestrator.answer(question)
            
            # Send response
            response = result["response"]
            await update.message.reply_text(response)
            
            # Optional: send sources
            if result["context_count"] > 0:
                sources = f"📚 Джерела: {result['context_count']} документів"
                await update.message.reply_text(sources)
            
        except Exception as e:
            print(f"Error processing question: {e}")
            import traceback
            traceback.print_exc()
            
            error_message = """❌ Сталася помилка при обробці питання.

Спробуй сформулювати питання інакше або перезапусти бота."""

            await update.message.reply_text(error_message)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        print(f"Error: {context.error}")
    
    def run(self):
        """Run the bot."""
        print("\n🚀 Запуск Hermes бота...")
        print("=" * 60)
        
        # Create application
        app = ApplicationBuilder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help))
        app.add_handler(CommandHandler("reset", self.reset))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        app.add_error_handler(self.error_handler)
        
        # Run bot
        print("Бот запущено! Напиши /start щоб почати.")
        print("Натисни Ctrl+C щоб зупинити")
        print("=" * 60)
        
        app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Hermes Telegram Bot")
    parser.add_argument("--token", help="Telegram bot token (overrides .env)")
    parser.add_argument("--vault", default="./unified-brain", help="Path to vault")
    parser.add_argument("--chroma", default="./chromadb", help="Path to ChromaDB")
    
    args = parser.parse_args()
    
    # Get token from args or environment
    token = args.token or os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        print("Set it via --token or .env file")
        sys.exit(1)
    
    # Create and run bot
    bot = HermesBot(
        token=token,
        vault_path=args.vault,
        chroma_path=args.chroma
    )
    
    bot.run()


if __name__ == "__main__":
    main()
```

---

## Deployment

### 1. Run Bot Locally

```bash
python hermes_bot.py
```

### 2. Run Bot with PM2 (recommended for long-running)

```bash
# Install PM2
npm install -g pm2

# Start bot
pm2 start hermes_bot.py --name hermes-bot

# View logs
pm2 logs hermes-bot

# Stop bot
pm2 stop hermes-bot
```

### 3. Run Bot via Systemd (Linux)

Create `/etc/systemd/system/hermes-bot.service`:

```ini
[Unit]
Description=Hermes Telegram Bot
After=network.target ollama.service

[Service]
Type=simple
User=guiboratto
WorkingDirectory=/home/guiboratto/obsidian-brain
Environment="PATH=/home/guiboratto/obsidian-brain/venv/bin"
ExecStart=/home/guiboratto/obsidian-brain/venv/bin/python hermes_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable hermes-bot
sudo systemctl start hermes-bot
sudo systemctl status hermes-bot
```

---

## Webhook Deployment (Optional)

For production deployment, use webhooks instead of polling:

### 1. Get Ngrok or similar tunneling service:

```bash
# Install ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && \
sudo apt update && sudo apt install ngrok

# Get authtoken from https://dashboard.ngrok.com
ngrok config add-authtoken YOUR_TOKEN
```

### 2. Create Flask app for webhooks:

```python
# webhook_server.py
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Import bot logic (same as hermes_bot.py)
from hermes_bot import HermesBot

# Initialize bot
bot = HermesBot(token=TELEGRAM_BOT_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot.application)
    bot.application.process_update(update)
    return 'OK', 200

if __name__ == '__main__':
    # Set webhook
    webhook_url = f"https://your-ngrok-url.ngrok.io/webhook"
    bot.application.bot.set_webhook(webhook_url)
    
    # Run Flask
    app.run(host='0.0.0.0', port=5000)
```

### 3. Start webhook server:

```bash
python webhook_server.py
```

---

## Testing

### 1. Test with Telegram

1. Send `/start` to your bot
2. Ask a question like:
   - "Що мені потрібно робити сьогодні?"
   - "Підготуйся до зустрічі з командою"
   - "Які ідеї є для нового проекту?"

### 2. Test with Python

```python
from orchestrator import ObsidianOrchestrator

orchestrator = ObsidianOrchestrator()
result = orchestrator.answer("Що мені потрібно робити сьогодні?")
print(result["response"])
```

---

## Troubleshooting

### Bot doesn't respond

1. Check if bot is running:
   ```bash
   pm2 status
   # or
   ps aux | grep hermes_bot
   ```

2. Check logs:
   ```bash
   pm2 logs hermes-bot
   ```

3. Verify token is correct

### ChromaDB errors

1. Rebuild ChromaDB:
   ```bash
   python scripts/setup-chromadb.py
   ```

2. Check vault path is correct

### Ollama not responding

1. Check if Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. Restart Ollama:
   ```bash
   systemctl restart ollama
   # or
   ollama serve
   ```

---

## Maintenance

### Backup ChromaDB

```bash
cp -r ./chromadb ./chromadb.backup.$(date +%Y%m%d)
```

### Backup Vault

```bash
git add .
git commit -m "Backup: $(date)"
git push
```

### Update ChromaDB after vault changes

```bash
# 1. Commit changes to vault
git add .
git commit -m "Update vault"
git push

# 2. Rebuild ChromaDB
python scripts/setup-chromadb.py

# 3. Restart bot
pm2 restart hermes-bot
```

---

**Created:** 2026-09-25
**Author:** Qwen Code + Ivantsi
