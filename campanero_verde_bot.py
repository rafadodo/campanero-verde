"""
Bot de Telegram que puede ser comandado para devolver el canje de dólar CCL a MEP mediante el módulo
campanero_verde. Lee de archivos \'.env\' tanto el token del bot como las credenciales para el
campanero.
"""
import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import campanero_verde as campanero

CREDENTIALS_FILENAME = 'bnz_credentials.env'
TOKEN_FILENAME = 'telegram_bot_token.env'
load_dotenv(TOKEN_FILENAME)
token = os.environ.get('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = "Buenas, soy el campanero verde.\nNo sirvo para mucho, pero si me mandás el " + \
            "comando \'/contame\' yo te mando el valor del canje de dólar CCL a MEP."
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = start_text
        )

async def contame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_dotenv(CREDENTIALS_FILENAME)
    bnz_username = os.environ.get('BNZ_USER')
    bnz_password = os.environ.get('BNZ_PASS')
    canje_al30, canje_gd30 = campanero.get_canje(bnz_username, bnz_password)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'El canje anda en {}% para AL30 y en {}% para GD30'.format(
                                                                        round(canje_al30, 1),
                                                                        round(canje_gd30, 1)))

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    contame_handler = CommandHandler('contame', contame)

    application.add_handler(start_handler)
    application.add_handler(contame_handler)
    
    application.run_polling()