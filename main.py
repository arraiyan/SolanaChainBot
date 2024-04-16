import logging

from telegram import *
from telegram.ext import *
from datetime import timedelta
from cSRC.chain import *
from cSRC.inf import env as ENV
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    ENV.GROUPS.append(update.message.chat_id)
    await update.message.reply_html(
        rf"""
Hi {user.mention_html()}!
Welcome to the SOLANA Bot.
""",
        reply_markup=ForceReply(selective=True),
    )


async def get_coin_info(context: ContextTypes.DEFAULT_TYPE) -> None:
    market_cap , market_rank , exchange_rate , name = market_data('DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263')
    addr = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
    message = f"""
📌 Coin Name ({name})

💲  Echange Rate USDC: $ {float(exchange_rate)}
💎 Market Cap : $ {market_cap}
🏹 Market Rank : {market_rank}
🔸 Chain: SOL | ⚖️ Age: null
🌿 Mint: No ✅ | Liq: 🔥
Contract Address <b>DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263</b>
<a href='https://dexscreener.com/solana/{addr}'>Dexscreene</a> | <a href='https://birdeye.so/token/{addr}?chain=solana'>Birdeye</a>
<a href='https://photon-sol.tinyastro.io'>Photon</a> | <a href='https://t.me/bonkbot_bot'>Bonkbot</a>
Banana : @BananaGunSolana_bot
"""
    for i in ENV.GROUPS:
        await context.bot.send_message(chat_id=i,text= message,parse_mode='HTML')

async def add_new_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    ENV.GROUPS.append(chat_id)
    pass

async def updater_via_time(context: ContextTypes.DEFAULT_TYPE) -> None:

    print('pooling')
    pass


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.chat_id)
    pass




     











def main() -> None:
    application = Application.builder().token(ENV.API_KEY).build()
    try:
        application.job_queue.run_repeating(updater_via_time,timedelta(seconds=20))
    except:
        pass    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()