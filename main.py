from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from scripts.utils import get_links, get_text_content, get_summary

TOKEN : Final = "6302986945:AAF7JfNzf0yae43T1ZdEQKMGxMY1hRWKovA"
BOT_USERNAME : Final = "@test5times_bot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to 5 times")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I talk 5 times")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

def handle_response(text: str) -> str:
    links = get_links(query=text)
    text_content = get_text_content(links=links)
    summarized_text = get_summary(texts=text_content)
    ans = ""
    for i in range(len(summarized_text)):
        ans += f"News {i}:\n"
        ans += summarized_text[i] + "\n\n"
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