import telebot

TOKEN = '1685201828:AAEEpPTyerjCY4VUGkPnwycFnE3rNeBtMY4'
URL = 'https://sledoktv.ru/telegram/'
bot = telebot.TeleBot(TOKEN, parse_mode=None)
TEST = False
fields = {'username': None, 'password': None, 'chat_id': None, 'telegram_username': None}
import requests


def _get_username(values: list) -> str:
    for value in values:
        if not value.isdigit():
            return value


def _get_password(values: list) -> str:
    for value in values:
        if value.isdigit():
            return value


def validate(pas: str, usr: str, values: list) -> bool:
    if pas and usr and len(values) == 2 and len(pas) == 4:
        return True
    else:
        return False


def get_username_and_password(message: str):
    list_values = message.split()
    username = _get_username(list_values)
    password = _get_password(list_values)
    if validate(password, username, list_values):
        return username, password
    else:
        return None, None


def request_sledoktv(payload, test: bool) -> str:
    if test is True:
        return 'OK'

    res = requests.get(url=URL, params=payload)
    return res.text


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте! Вы активировали seldoktv_bot, для того чтобы начать получать оповещения "
                          "введите через пробел ваш логин с сайта sledoktv.ru и четырёхзначный "
                          "код отправленный вам по email.")


@bot.message_handler(content_types=['text'])
def auth_user(message):
    msg = message.text
    username, password = get_username_and_password(msg)
    if username and password:  # данные введенные пользователем прошли проверку
        chat_id = message.from_user.id

        fields['chat_id'] = chat_id
        fields['telegram_username'] = str(message.from_user.username)
        fields['username'] = username
        fields['password'] = password

        res = request_sledoktv(fields, test=TEST)
        if res == 'OK':  # c сайта пришёл положительный ответ
            bot.send_message(chat_id, 'Вы успешно настроили оповещения.')
        else:  # ошибка на сервере
            bot.send_message(message.from_user.id,'Перепроверьте ваш логин и числовой код.')
    else:  # данные введённые пользователем не прошли проверку
        bot.send_message(message.from_user.id,
                         'Неправельно введён логин или (и) числовой код. Вводите данные через пробел '
                         'попробуйте еще.')


bot.polling()

if __name__ == '__main__':
    assert get_username_and_password('hello 1234') == ('hello', '1234',)
    assert get_username_and_password('hello hello') == (None, None)
    assert get_username_and_password('hello 12345') == (None, None)
    assert get_username_and_password('medikos sjsjsj sjjsj') == (None, None)
