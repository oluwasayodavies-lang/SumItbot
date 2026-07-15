# SumItBot 🤖

A Telegram bot that summarizes text and documents using AI.

## Features ✨

- 📝 Summarize any text message
- 📄 Process documents (PDF, DOCX, TXT, MD, RTF)
- 🎯 Adjustable summary length (short/medium/long)
- 🌐 Multi-language support
- ⚡ Fast and reliable

## Commands 🎮

- `/start` - Welcome message
- `/help` - Show help
- `/about` - About this bot

## Technologies Used 🛠️

- Python 3.9+
- python-telegram-bot
- OpenAI GPT API
- Railway (Hosting)
- GitHub (Version Control)

## Deployment 🚀

This bot is deployed on Railway. To deploy your own:

1. Clone this repository
2. Set up environment variables
3. Deploy to Railway via GitHub

## Environment Variables 🔑

- `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather
- `OPENAI_API_KEY` - Your OpenAI API key

## Local Development 💻

```bash
# Clone the repository
git clone https://github.com/yourusername/SumItBot.git

# Install dependencies
pip install -r requirements.txt

# Create .env file with your tokens
# Run the bot
python bot.py
