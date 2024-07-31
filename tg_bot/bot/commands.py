from .main import bot
from ..models import *
from .keyboards import *


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    try:
        UserModel.objects.get(user_id=message.from_user.id)
    except:
        user = UserModel()
        user.user_id = message.from_user.id
        user.username = message.from_user.username
        user.save()
    if message.chat.id < 0:
        bot.send_message(message.chat.id,
                         "Привет, я бот, который поможет найти тебе сотрудника в твой проект. Ну или найти тебе "
                         "работу. Однако, я работаю только в личных сообщениях. Быстрее переходи в переписку со "
                         "мной и жми start")
    else:
        bot.send_message(message.chat.id,
                         "Привет!\nЯ помогу тебе найти сотрудника в твой проект. Ну или найти тебе работу.\n"
                         "Скорее нажимай на кнопку 'полетели', и я тебе все расскажу",
                         reply_markup=keyboard_start)
