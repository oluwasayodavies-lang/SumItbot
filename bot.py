import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from handlers import summary_handlers
from config import Config

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /start is issued."""
    welcome_text = """
🤖 Welcome to SumItBot!
I can summarize any text or document you send me.

📝 How to use:
• Send me any text message
• Send me a document (.txt, .pdf, .docx)
• Use /help for more options

⚡ Quick commands:
/start - Show this message
/help - Show help
/about - About this bot
"""
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /help is issued."""
    help_text = """
📚 SumItBot Help

I summarize text using AI! Here's what I can do:

✅ Text Summarization
   Send any text (up to 5000 characters)
   
✅ Document Processing
   Supported formats: .txt, .pdf, .docx, .md
   
✅ Customization
   /summary [length] - Set summary length (short/medium/long)
   /language [lang] - Choose output language

🔧 Commands:
/start - Welcome message
/help - This help menu
/about - About this bot
/summary - Set summary length
/language - Choose language
/cancel - Cancel current operation
"""
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /about is issued."""
    about_text = """
ℹ️ About SumItBot

Version: 1.0.0
Developer: Your Name
GitHub: https://github.com/yourusername/SumItBot

🧠 Powered by:
• OpenAI GPT API for summarization
• Python Telegram Bot Library
• Deployed on Railway

📈 Features:
• AI-powered summaries
• Multi-language support
• Document processing
• Customizable length
• Fast & reliable
"""
    await update.message.reply_text(about_text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.warning(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Sorry, something went wrong. Please try again later."
        )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # Register message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, summary_handlers.handle_text))
    application.add_handler(MessageHandler(filters.Document.ALL, summary_handlers.handle_document))
    
    # Register error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
