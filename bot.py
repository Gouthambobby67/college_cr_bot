
import logging
from examtimetable import exam_timetable
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
async def exam_time_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[
        [InlineKeyboardButton("R20", callback_data='R20')],
        [InlineKeyboardButton("R18", callback_data='R18')],
        [InlineKeyboardButton("R23", callback_data='R23')],
    ]
    reply_markup=InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose Regulation:", reply_markup=reply_markup)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    regulation=query.data
    notice= exam_timetable(regulation)
    msg="\n\n".join(notice[:10])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
      
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    check_handler = CommandHandler('exam_time_table', exam_time_table)
    application.add_handler(check_handler)
    application.add_handler(CommandHandler('button', button))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()
