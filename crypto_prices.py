import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv

load_dotenv()
coinGecko = CoinGeckoAPI()
APITOKEN = os.environ.get("APITOKEN")

crypto_currencies = [
    "Bitcoin",
    "Ethereum",
    "Tether",
    "Cardano",
    "binancecoin",
    "Ripple",
    "Dogecoin",
    "Ethereum-Classic",
    "Polkadot",
    "USD-Coin",
    "binance-usd",
    "Bitcoin-Cash",
    "Solana",
    "Dai",
    "Litecoin",
]

myBot = telebot.TeleBot(APITOKEN)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for i in range(0, 14, 3):
        markup.add(
            InlineKeyboardButton(
                crypto_currencies[i], callback_data=crypto_currencies[i]
            ),
            InlineKeyboardButton(
                crypto_currencies[i + 1], callback_data=crypto_currencies[i + 1]
            ),
            InlineKeyboardButton(
                crypto_currencies[i + 2], callback_data=crypto_currencies[i + 2]
            ),
        )
    return markup


@myBot.message_handler(commands=["start", "all"])
def send_welcome(message):
    msg = myBot.send_message(
        message.chat.id,
        "Select a crypto-currency to get price",
        reply_markup=gen_markup(),
    )


@myBot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    try:

        info = coinGecko.get_price(ids=call.data, vs_currencies="usd")

        myBot.send_message(
            call.from_user.id,
            call.data + " Price is\n" + "$ " + str(info[str(call.data).lower()]["usd"]),
        )

    except:
        myBot.send_message(call.from_user.id, "Something went wrong! \nPlease try again later")


myBot.infinity_polling()
