import os
import logging.config
import requests
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup as BS

from datetime import datetime
import time
from http import HTTPStatus
from dotenv import load_dotenv
load_dotenv()
from logger_config import config



logging.config.dictConfig(config)
logger = logging.getLogger('app_logger')

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='{asctime} - {name} - {levelname} - {message}', style='{',
#     filename='main.log',
#     filemode='a')

# handler = logging.StreamHandler(sys.stdout)
# logger.addHandler(handler)
# # logger.disabled = False
logger.debug('Loging started')
# logging.getLogger('urllib3').setLevel('CRITICAL')
# logging.getLogger('asyncio').setLevel('CRITICAL')
# logging.getLogger('aiogram').setLevel('CRITICAL')

# Добавляем файловый лог
# fileHandler = logging.FileHandler('main.log', encoding='utf-8')
# for key in logging.Logger.manager.loggerDict:
#     print(key)



secret_token = os.getenv('TOKEN')
bot = Bot(token = secret_token)

dp = Dispatcher(bot)
dt_obj = datetime.now()
dt_string = dt_obj.strftime("%d %b")

URL = os.getenv('URL')
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept':'*/*'}
RETRY_TIME = 6


oven = URL + "oven/"
telets = URL + "telets/"
bliznetsy = URL + "bliznetsy/"
rak = URL + "rak/"
lev = URL + "lev/"
deva = URL + "deva/"
vesy = URL + "vesy/"
skorpion = URL + "skorpion/"
strelets = URL + "strelets/"
kozerog = URL + "kozerog/"
vodolei = URL + "vodolei/"
ryby = URL + "ryby/"

btn = KeyboardButton("/start")
btn1 = KeyboardButton("♈ Овен")
btn2 = KeyboardButton("♉ Телец")
btn3 = KeyboardButton("♊ Близнецы")
btn4 = KeyboardButton("♋ Рак")
btn5 = KeyboardButton("♌ Лев")
btn6 = KeyboardButton("♍ Дева")
btn7 = KeyboardButton("♎ Весы")
btn8 = KeyboardButton("♏ Скорпион")
btn9 = KeyboardButton("♐ Стрелец")
btn10 = KeyboardButton("♑ Козерог")
btn11 = KeyboardButton("♒ Водолей")
btn12 = KeyboardButton("♓ Рыбы")


@dp.message_handler(content_types=['new_chat_members'])
async def greeting(message: types.Message):
    await message.reply( text='hello')
    
@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    markup = ReplyKeyboardMarkup()
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
    await message.answer(f"Привет, {message.from_user.first_name}! Cегодня " +str(dt_string)+ ", выбери свой знак зодиака".format(message.from_user), reply_markup=markup)



@dp.message_handler(content_types=['text'])
async def get_name(message: types.Message):
    name = message.text;
    if name == "♈ Овен":
        await message.answer(parse(oven));
    elif name == "♉ Телец":
        await message.answer(parse(telets));
    elif name == "♊ Близнецы":
        await message.answer(parse(bliznetsy));
    elif name == "♋ Рак":
        await message.answer(parse(rak));
    elif name == "♌ Лев":
        await message.answer(parse(lev));
    elif name == "♍ Дева":
        await message.answer(parse(deva));
    elif name == "♎ Весы":
        await message.answer(parse(vesy));
    elif name == "♏ Скорпион":
        await message.answer(parse(skorpion));
    elif name == "♐ Стрелец":
        await message.answer(parse(strelets));
    elif name == "♑ Козерог":
        await message.answer(parse(kozerog));
    elif name == "♒ Водолей":
        await message.answer(parse(vodolei));
    elif name == "♓ Рыбы":
        await message.answer(parse(ryby));
    else:
        markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        markup.add(btn)
        time_2 = datetime.now()
        a = time.mktime(dt_obj.timetuple())
        b = time.mktime(time_2.timetuple())
        time_interval = b - a
        if time_interval < 20.0 or time_interval > 86400.0:
            await message.answer(f"Извени, {message.from_user.first_name}! Ничего не понял, нажми на кнопку /start".format(message.from_user), reply_markup=markup)
        else:
            await message.answer(f"{message.from_user.first_name}, выбери свой знак зодиака".format(message.from_user), reply_markup=markup)



def parse(url):
    try:
        html = get_html(url)
        return get_content(html.text)
    except AttributeError:
        logging.error('Нет данных или нет связи с сайтом.')

        
def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response

def get_content(html):
    soup = BS(html, "html.parser")
    items = soup.find_all(class_='col-md-9')
    for item in items:
        a = ({
            'text' : item.find('p').get_text(strip = True) #strip - убирает концевые пробелы
        })
    s = a['text']
    return s

def check_tokens():
    if secret_token is None or len(secret_token) == 0:
        return False
    else:
        return True

def get_api_answer(current_timestamp):
   
    if current_timestamp is None:
        current_timestamp = int(time.time())
    params = {'from_date': current_timestamp}
     
    try:
        homework_status = requests.head(
            URL,
            headers=HEADERS,
            params=params)
        if homework_status.status_code != HTTPStatus.OK:
            raise Exception("Сайт не отвечает.")
        return homework_status
    except ConnectionError:
        logging.error('Сайт не отвечает.')
        return {}

def main():
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    current_timestamp = int(0)
    check_tokens()
    try:
        get_api_answer(current_timestamp)
    except Exception as error:
        logging.exception(f'Бот столкнулся с ошибкой: {error}')



if __name__ == "__main__":
    main()
    
    # Запуск бота
    while True:#Здесь делаем бесконечный цикл для запуска бота
        try:
            executor.start_polling(dp, skip_updates=True)
        except(BaseException):
            pass