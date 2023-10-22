# from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from scripts.utils_google import get_links, get_text_content, get_summary
from scripts.utils_yt import get_audio_file, extract_text_from_mp3
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to FlashFeedAIBot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I collect the latest news on topics you enter")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I collect the latest news on topics you enter")

def handle_response(text: str) -> str:
    links = get_links(query=text)
    texts = get_text_content(links=links)
    summarized_texts = get_summary(texts=texts)
    ans = ""
    
    for i, (link, summarized_text) in enumerate(summarized_texts.items()):
        ans += f"News {i+1}:\n"
        ans += summarized_text + "\n" + "Source link: " + link + "\n\n"
    return ans


async def handle_message(update: Update,
                         context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f"User ({update.message.chat.id}) in {message_type}: {text}")

    if message_type=="group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)
    
    print("Bot ", response)
    await update.message.reply_text(response)

async def error(update: Update,
                context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":

    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=5)