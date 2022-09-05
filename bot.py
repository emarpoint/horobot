import os
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup as BS

from datetime import datetime
import time
from http import HTTPStatus
from telegram import TelegramError
from dotenv import load_dotenv
load_dotenv()


logger = logging.getLogger(__name__)
secret_token = os.getenv('TOKEN')
bot = Bot(token = secret_token)

dp = Dispatcher(bot)
dt_obj = datetime.now()
dt_string = dt_obj.strftime("%d %b")
URL = "https://moigoroskop.org/goroskop/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept':'*/*'}
RETRY_TIME = 600

logging.basicConfig(level=logging.INFO)

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
    html = get_html(url)
    return get_content(html.text)

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
    """Проверка доступности переменных окружения."""
    if secret_token is None or len(secret_token) == 0:
        return False
    else:
        return True

def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
   
    if current_timestamp is None:
        current_timestamp = int(time.time())
    params = {'from_date': current_timestamp}
       
    try:
        homework_status = requests.get(
            URL,
            headers=HEADERS,
            params=params)
        # logger.debug(f'Получен код : {homework_status.status_code}')
        if homework_status.status_code != HTTPStatus.OK:
            raise Exception("Сайт не отвечает.")
        # logging.debug(f'Код : {homework_status.status_code}')
        return homework_status
    except ConnectionError:
        logging.error('Сайт не отвечает.')
        return {}

def send_message(message, bot):
    """Отправляет сообщение в Telegram чат о статусе проверенной работы."""
    logging.info(f'Сообщение: {message}')
    try:
        bot.send_message(message.from_user.id, text=message)
    except TelegramError:
        logging.error("Ошибка отправки сообщения")



def main():
    """Основная логика работы бота."""
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    logger.debug('Бот работает!')
    current_timestamp = int(0)
    check_tokens()
    try:
        response = get_api_answer(current_timestamp)
        
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