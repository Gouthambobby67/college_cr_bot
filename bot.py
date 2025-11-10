TOKEN="8560319193:AAFXsjL5n6td-HnG_nzqZ2WF_NmZWYi7hXs"
#export TELEGRAM_BOT_TOKEN="8560319193:AAFXsjL5n6td-HnG_nzqZ2WF_NmZWYi7hXs"

import logging
from main import exam_timetable
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Fetching exam timetable...")
    notice= exam_timetable()
    msg="\n\n".join(notice[:10])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
      
if __name__ == '__main__':
    application = ApplicationBuilder().token("8560319193:AAFXsjL5n6td-HnG_nzqZ2WF_NmZWYi7hXs").build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    check_handler = CommandHandler('check', check)
    application.add_handler(check_handler)
    application.run_polling()