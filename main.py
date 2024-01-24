#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

from flask import Flask, request
from telegram import ForceReply, Update
from telegram.ext import CommandHandler, MessageHandler, filters, Application, ContextTypes
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Create the Application and pass it your bot's token.
application = Application.builder().token("6661039666:AAF-Q55t5r2uvG0tQW-6yLViaFzEce_Nx-s").build()

# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

# Define Flask routes
@app.route("/")
def index():
    return "Hello, this is your Flask app!"

@app.route("/webhook", methods=['POST'])
def webhook():
    json_data = request.get_json()
    update = Update.de_json(json_data, application.bot)
    application.process_update(update)
    return '', 200

# Add handlers to the Application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == "__main__":
    # Start Flask app
    app.run(port=5000, debug=True)
