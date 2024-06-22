import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackGame
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from dotenv import load_dotenv
import os
from web3 import Web3

# Configuração do logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
OWNER_ADDRESS = os.getenv("OWNER_ADDRESS")

# Configuração do Web3
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
with open('ETICOIN.abi') as abi_file:
    contract_abi = abi_file.read()
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Função para iniciar o bot
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    game_name = "ETICOIN"  # Nome do jogo configurado no BotFather

    keyboard = [
        [InlineKeyboardButton("Play Game", callback_game=CallbackGame())],
        [InlineKeyboardButton("Follow Comunity", callback_data='help')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id, text="Bem-vindo ao ETICOIN!", reply_markup=reply_markup)

# Função para lidar com os botões
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == 'Follow X':
        await context.bot.answer_callback_query(query.id, text="")
    elif query.game_short_name == 'ETICOIN':
        await context.bot.answer_callback_query(query.id, url="https://t.me/Eticoin_bot")

# Função para lidar com erros
async def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Função principal para iniciar o bot
def main() -> None:
    # Inicializa o bot e o Dispatcher
    application = Application.builder().token(BOT_TOKEN).build()

    # Adiciona o comando /start
    application.add_handler(CommandHandler("start", start))

    # Adiciona os manipuladores de callback para os botões
    application.add_handler(CallbackQueryHandler(button))

    # Adiciona o manipulador de erros
    application.add_error_handler(error)

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()
