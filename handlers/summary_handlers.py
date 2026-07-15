import os
import tempfile
from telegram import Update
from telegram.ext import ContextTypes
from utils.summarizer import summarize_text, summarize_document
from config import Config

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages and summarize them."""
    user_message = update.message.text
    
    # Check if message is too long
    if len(user_message) > Config.MAX_TEXT_LENGTH:
        await update.message.reply_text(
            f"⚠️ Message is too long! Please send text under {Config.MAX_TEXT_LENGTH} characters."
        )
        return
    
    # Send typing indicator
    await update.message.chat.send_action(action="typing")
    
    try:
        # Get summary length from user preference
        length = context.user_data.get('summary_length', Config.DEFAULT_SUMMARY_LENGTH)
        
        # Generate summary
        summary = await summarize_text(user_message, length=length)
        
        # Send response
        response = f"📝 **Summary** ({length} length):\n\n{summary}"
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Failed to summarize text. Error: {str(e)}"
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads and summarize them."""
    document = update.message.document
    
    # Check if file type is supported
    file_extension = os.path.splitext(document.file_name)[1].lower()
    if file_extension not in Config.SUPPORTED_DOCUMENTS:
        await update.message.reply_text(
            f"⚠️ Unsupported file type. Please upload: {', '.join(Config.SUPPORTED_DOCUMENTS)}"
        )
        return
    
    # Send typing indicator
    await update.message.chat.send_action(action="typing")
    
    try:
        # Download file
        file = await document.get_file()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            await file.download_to_drive(tmp_file.name)
            tmp_path = tmp_file.name
        
        # Get summary length
        length = context.user_data.get('summary_length', Config.DEFAULT_SUMMARY_LENGTH)
        
        # Summarize document
        summary = await summarize_document(tmp_path, length=length)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Send response
        response = f"📄 **Document Summary** ({document.file_name})\n\n{summary}"
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Failed to process document. Error: {str(e)}"
        )
