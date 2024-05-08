import logging

from telegram import *
from telegram.ext import *
from datetime import timedelta
from cSRC.chain import *
from cSRC.inf import env as ENV
from cSRC.solana_scan import *
from solders.signature import Signature
from cSRC.db import Contract as cdb
from datetime import datetime
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


usernames = {'usernames':[]}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usernames['usernames'].append(update.message.from_user.username)
    usernames['usernames'].append(f'{update.message.from_user.first_name} {update.message.from_user.last_name}')
    save_json(usernames,'usernames.json')    
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

    if not update.message.chat.type == 'private':
        if update.message.from_user.id in ENV.ADMINS:
            chat_id = update.message.chat_id
            ENV.GROUPS.append(chat_id)
            await update.message.reply_text("Your group have been added")
        else :
            await update.message.reply_text("Please login first useing /login password")
    pass

async def add_channel1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not update.message.chat.type == 'private':
        if update.message.from_user.id in ENV.ADMINS:
            chat_id = update.message.chat_id
            ENV.CHANNEL_ONE.append(chat_id)
            await update.message.reply_text("Your group have been added")
        else :
            await update.message.reply_text("Please login first useing /login password")
    pass

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usernames['usernames'].append(update.message.from_user.username)
    usernames['usernames'].append(f'{update.message.from_user.first_name} {update.message.from_user.last_name}')
    save_json(usernames,'usernames.json')
    if update.message.chat.type == 'private':
        password = update.message.text.split()[1]
        if password == ENV.password:
            ENV.ADMINS.append(update.message.from_user.id)
            await update.message.reply_text("You have successfully logged in the account")

        else:
            await update.message.reply_text("Wrong Password Please login again")

    else:
        await update.message.reply_text(f'Please open the<a href="https://t.me/{context.bot.username}"> private chat </a>',parse_mode='HTML')




async def updater_via_time(context: ContextTypes.DEFAULT_TYPE) -> None:

    print('pooling')

    block = get_latest_block(public_key)
    print(block)
    tx = get_tx(Signature.from_string(block['signature']))
    save_json(tx,'data.json')
    analyze = analyze_tx(tx)
    for token in analyze:
        try:
            first_ping = False
            c_data = cdb.query_database('contract',token)
            if len(c_data)>=1:
                c_data = c_data[0]
            else:
                c_data = cdb(len(cdb.get_all_users()),contract=token,date_created=datetime.now())
                c_data.create()
                c_data.save()
                first_ping = True

            c_data.total_calls+=1
            c_data.latest_block = int(tx['result']['slot'])
            c_data.save()
            token_info  = terminal_get_token(token)
            save_json(token_info,'token_info.json')
            get_sol_usd = terminal_get_token("So11111111111111111111111111111111111111112")['data']['attributes']['price_usd']
            symbol = token_info['data']['attributes']['symbol']

            diluted_volume = token_info['data']['attributes']['fdv_usd']
            buys_ing_24h = token_info['included'][0]['attributes']['transactions']['h24']['buys']
            buys_ing_5m = token_info['included'][0]['attributes']['transactions']['m5']['buys']
            exchange_rate = token_info['data']['attributes']['price_usd']

            pool_id = token_info['included'][0]['attributes']['address']
            print('pool_id ',pool_id)
            get_dex = requests.get(f'https://api.dexscreener.com/latest/dex/pairs/solana/{pool_id},').json()
            mc = get_dex['pairs'][0]['fdv']
            liqui = get_dex['pairs'][0]['liquidity']['usd']

            # try:
            #     market_cap , market_rank , exchange_rate = market_data(token)
            # except:
            #     market_cap , market_rank , exchange_rate = None , None ,None
            # print(symbol , liquidity , diluted_volume)
            # save_json( market_data('E775oRnkLxStuPHeDca9rxNUaByJtwareyg9DvX6P4GU'),'data_json.json')

            if first_ping:
                for i in ENV.CHANNEL_ONE:

                    
                    if not symbol == 'USDC' and not symbol=="USDT" and int(buys_ing_24h)<150:
                        await context.bot.send_message(chat_id=i,text=f"""

📌 Coin Name ({symbol})

💲  Exchange Rate USDC: $ {exchange_rate}
💎 Market Cap : $ {round(float(mc),2) if mc else 0.0}
⏳ Pings :       {c_data.total_calls}
📊 Buys in last 24 Hours:     {buys_ing_24h}
🔸 Chain: SOL | ⚖️ Age: null
🌿 Mint: No ✅ 
💎 Liquidity: 🔥 ${liqui:00.2f}
🔸 FDV ${diluted_volume}
Exchange Rate SOL / {symbol}  {float(float(exchange_rate)/float(get_sol_usd)) if exchange_rate and get_sol_usd else 'null'} Sol
Contract Address <b>{token}</b>
<a href='https://dexscreener.com/solana/{token}'>Dexscreener</a> | <a href='https://birdeye.so/token/{token}?chain=solana'>Birdeye</a>
<a href='https://photon-sol.tinyastro.io'>Photon</a> | <a href='https://t.me/bonkbot_bot/?start={token}'>Bonkbot</a>
<a href='https://t.me/BananaGunSolana_bot?start={token}'>BananaGunBot</a> 
<a href='https://www.dextools.io/app/en/solana/pair-explorer/{token}'>Dextools</a> 
    """,parse_mode='HTML')
        
            for i in ENV.GROUPS:

                
                if not symbol == 'USDC' and not symbol=="USDT":
                    await context.bot.send_message(chat_id=i,text=f"""

📌 Coin Name ({symbol})

💲  Exchange Rate USDC: $ {exchange_rate}
💎 Market Cap : $ {round(float(mc),2) if mc else 0.0}
⏳ Pings :       {c_data.total_calls}
📊 Buys in last 5 Minutes:     {buys_ing_5m}
🔸 Chain: SOL | ⚖️ Age: null
🌿 Mint: No ✅ 
💎 Liquidity: 🔥 ${liqui:00.2f}

Exchange Rate SOL / {symbol}  {float(float(exchange_rate)/float(get_sol_usd)) if exchange_rate and get_sol_usd else 'null'} Sol
Contract Address <b>{token}</b>
<a href='https://dexscreener.com/solana/{token}'>Dexscreener</a> | <a href='https://birdeye.so/token/{token}?chain=solana'>Birdeye</a>
<a href='https://photon-sol.tinyastro.io'>Photon</a> | <a href='https://t.me/bonkbot_bot/?start={token}'>Bonkbot</a>
<a href='https://t.me/BananaGunSolana_bot?start={token}'>BananaGunBot</a> 
<a href='https://www.dextools.io/app/en/solana/pair-explorer/{token}'>Dextools</a> 
""",parse_mode='HTML')
        
        
        except Exception as e:
            print(e)
            pass
    pass


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usernames['usernames'].append(update.message.from_user.username)
    usernames['usernames'].append(f'{update.message.from_user.first_name} {update.message.from_user.last_name}')
    save_json(usernames,'usernames.json')
    pass




     











def main() -> None:
    application = Application.builder().token(ENV.API_KEY).build()
    try:
        application.job_queue.run_repeating(updater_via_time,timedelta(seconds=3))
    except:
        pass    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("add_group", add_new_group))
    application.add_handler(CommandHandler("add_channel1", add_channel1))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()