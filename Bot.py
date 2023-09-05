from pycoingecko import CoinGeckoAPI
import telebot
from tokens import TOKEN_BOT
import pandas as pd

api = CoinGeckoAPI()
bot = telebot.TeleBot(TOKEN_BOT)
currency_convert_in = 'usd'
coin_market = api.get_coins_markets(vs_currency='usd')
top = api.get_search_trending(id='binance')


@bot.message_handler(commands=['start'])
def greeting_user(message):
    bot.send_message(message.chat.id,
                     'Привет я Ostin твой криптобот.\nВведите команду или откройте список команд (/help).')


@bot.message_handler(commands=['help'])
def command_doc(message):
    bot.send_message(message.chat.id,
                     '/help - Список команд\n'
                     '/get_spot_price - Получить спотовую цену по названию монеты\n'
                     '/coins10_list - Список первых 10 криптовалют(их цена, высшая и низшая за 24 часа)')


@bot.message_handler(commands=['coins10_list'])
def get_coin_list(message):
    df_market = pd.DataFrame(coin_market, columns=['symbol', 'id', 'current_price'])
    df_market.set_index('symbol')
    pd.options.display.float_format = '{:.2f}'.format
    coins = df_market.head(10)
    bot.send_message(message.from_user.id, coins.to_string())


@bot.message_handler(commands=['get_spot_price'])
def get_price(message):
    token = bot.send_message(message.from_user.id, 'Введите полное название монеты')
    bot.register_next_step_handler(token, get_crypto_price)


def get_crypto_price(message):
    cripto_id = message.text.lower()
    price = api.get_price(ids=cripto_id, vs_currencies="usd")

    if price:
        price = price[cripto_id][currency_convert_in]
    else:
        bot.send_message(message.chat.id, 'Такой криптовалюты нет')
        return

    bot.send_message(message.chat.id, "Спотовая цена {0} = {1}$".format(cripto_id, price))


@bot.message_handler(content_types=['text'])
def ckeck_text(message):
    if (message.text != "/help"
            or message.text != "/get_spot_price"
            or message.text != "coins10_list"):
        bot.send_message(message.from_user.id, 'Введите команду или откройте список команд (/help)')


bot.polling()
