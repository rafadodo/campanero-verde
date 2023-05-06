"""
Bot de Telegram que puede ser comandado para devolver el canje de dólar CCL a MEP mediante el módulo
campanero_verde.
"""

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import campanero_verde as campanero

TOKEN = '5920867007:AAGzJbuiIFOIo4Aomb6dCESH9LtMdj3Q_qw'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def vamo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Se rompen unos bonitos?")
    
async def contame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    canje = campanero.get_canje()
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'El canje anda en {}%'.format(round(canje, 1)))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    vamo_handler = CommandHandler('vamo', vamo)
    contame_handler = CommandHandler('contame', contame)

    application.add_handler(vamo_handler)
    application.add_handler(contame_handler)
    
    application.run_polling()