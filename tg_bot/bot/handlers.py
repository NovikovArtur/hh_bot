from .commands import *
from .function import *
from .states import *

hideBoard = types.ReplyKeyboardRemove()


@bot.callback_query_handler(lambda callback: callback.data in ['К главному меню', 'Полетели!'])
def main_menu(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    try:
        UserModel.objects.get(user_id=callback.from_user.id)
    except:
        user = UserModel()
        user.user_id = callback.from_user.id
        user.username = callback.from_user.username
        user.save()
    keyboard_main_menu = main_menu_keyboard(callback)
    bot.send_message(callback.message.chat.id,
                     "Приветствую тебя в главном меню!\nЗдесь ты можешь "
                     "выбрать различные варианты взаимодействия с ботом",
                     reply_markup=keyboard_main_menu)


@bot.callback_query_handler(lambda callback: callback.data in ['Работа с резюме', 'Назад, к работе с резюме'])
def work_with_cv(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    bot.send_message(callback.message.chat.id,
                     "В этом разделе ты можешь сделать различные вещи с твоим резюме "
                     "или добавить новое",
                     reply_markup=keyboard_work_with_CV)


@bot.callback_query_handler(lambda callback: callback.data in ['Добавить резюме'])
def cv_create(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    bot.send_message(callback.message.chat.id,
                     "Введите название резюме.\n\nВАЖНО: по названию резюме будет осуществляться "
                     "поиск подходящих вам вакансий в проектах, поэтому стоит писать название профессии.",
                     reply_markup=back_to_menu_cv)
    bot.set_state(callback.from_user.id, HH.wait_name_cv, callback.message.chat.id)


@bot.message_handler(state=HH.wait_name_cv)
def wait_name_cv(message: types.Message):
    answer = str(message.text)
    user = UserModel.objects.get(user_id=message.from_user.id)
    user.answer = answer
    user.save()
    bot.send_message(message.chat.id,
                     f"Название резюме: {answer}\nВведите текст вашего резюме.")
    bot.set_state(message.from_user.id, HH.wait_description_cv, message.chat.id)


@bot.message_handler(state=HH.wait_description_cv)
def wait_description_cv(message: types.Message):
    name_cv = UserModel.objects.get(user_id=message.from_user.id).answer
    text_cv = str(message.text)
    cv = CvModel()
    cv.user_id = UserModel.objects.get(user_id=message.from_user.id)
    cv.cv_name = name_cv
    cv.cv_text = text_cv
    cv.save()
    bot.send_message(message.chat.id,
                     f"Название резюме: {name_cv}\nРезюме: {text_cv}\n\nСохранено!",
                     reply_markup=back_to_menu_cv)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(lambda callback: callback.data in ['Посмотреть свои резюме'])
def cv_read(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    bull = cv_bull(callback)
    if bull:
        keyboard_cv_read = types.InlineKeyboardMarkup()
        names_cv = CvModel.objects.filter(user_id__user_id=callback.from_user.id)
        names_cv_name = [name_cv.cv_name for name_cv in names_cv]
        for name_cv in names_cv_name:
            keyboard_cv_read.add(types.InlineKeyboardButton(text=name_cv,
                                                            callback_data=name_cv))
        keyboard_cv_read.add(types.InlineKeyboardButton(text="Назад, к работе с резюме",
                                                        callback_data="Назад, к работе с резюме"))
        keyboard_cv_read.add(types.InlineKeyboardButton(text="К главному меню",
                                                        callback_data="К главному меню"))
        bot.send_message(callback.message.chat.id,
                         "Ваши резюме:",
                         reply_markup=keyboard_cv_read)
        bot.set_state(callback.from_user.id, HH.wait_click_on_cv_name, callback.message.chat.id)
    else:
        bot.send_message(callback.message.chat.id,
                         "У вас пока нет резюме.",
                         reply_markup=back_to_menu_cv)


# @bot.callback_query_handler(lambda callback: callback.data == 'Добавить новый доход или расход')
# def create_new(callback: types.CallbackQuery):
#     bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
#                                   message_id=callback.message.message_id,
#                                   reply_markup=None)
#     bot.send_message(callback.message.chat.id,
#                      "Введите описание дохода/расхода")
#     bot.set_state(callback.from_user.id, COSTS.add_description, callback.message.chat.id)
#
#
# @bot.message_handler(state=COSTS.add_description)
# def add_description(message: types.Message):
#     answer = str(message.text)
#     user = UserModel.objects.get(user_id=message.from_user.id)
#     user.answer = answer
#     user.save()
#     bot.send_message(message.chat.id,
#                      f"Ваше описание: {answer}\nВведите сколько вы потратили/получили с этого (если "
#                      f"вы на это тратили, напишите со знаком -)")
#     bot.set_state(message.from_user.id, COSTS.add_price, message.chat.id)
#
#
# @bot.message_handler(state=COSTS.add_price)
# def add_price(message: types.Message):
#     user = UserModel.objects.get(user_id=message.from_user.id)
#     description = user.answer
#     price = str(message.text)
#     note = NotesModel()
#     note.user_id = message.from_user.id
#     note.name = description
#     try:
#         note.costs = price
#         note.save()
#         bot.send_message(message.chat.id,
#                          f"Сохранили ваш доход/расход",
#                          reply_markup=back_to_menu)
#         bot.delete_state(message.from_user.id, message.chat.id)
#     except ValueError:
#         bot.send_message(message.chat.id,
#                          f"Произошла ошибка, проверьте ввод",
#                          reply_markup=back_to_menu)
#         bot.delete_state(message.from_user.id, message.chat.id)
#
#
# @bot.callback_query_handler(lambda callback: callback.data == 'Посмотреть расходы')
# def see_expenses(callback: types.CallbackQuery):
#     bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
#                                   message_id=callback.message.message_id,
#                                   reply_markup=None)
#     costs = NotesModel.objects.filter(user_id=callback.from_user.id)
#     text = 'Ваши расходы:\n'
#     for i in costs:
#         if i.costs < 0:
#             text += f"{i.name}   {i.costs}\n"
#     bot.send_message(callback.message.chat.id,
#                      text,
#                      reply_markup=back_to_menu)
#
#
# @bot.callback_query_handler(lambda callback: callback.data == 'Посмотреть доходы')
# def see_incoming(callback: types.CallbackQuery):
#     bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
#                                   message_id=callback.message.message_id,
#                                   reply_markup=None)
#     costs = NotesModel.objects.filter(user_id=callback.from_user.id)
#     text = 'Ваши доходы:\n'
#     for i in costs:
#         if i.costs >= 0:
#             text += f"{i.name}   {i.costs}\n"
#     bot.send_message(callback.message.chat.id,
#                      text,
#                      reply_markup=back_to_menu)
#
#
# @bot.callback_query_handler(lambda callback: callback.data == 'Краткая сводка')
# def see_results(callback: types.CallbackQuery):
#     bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
#                                   message_id=callback.message.message_id,
#                                   reply_markup=None)
#     costs = NotesModel.objects.filter(user_id=callback.from_user.id)
#     expenses = 0
#     incoming = 0
#     for i in costs:
#         if i.costs < 0:
#             expenses += i.costs
#         else:
#             incoming += i.costs
#     text = f"Сумма ваших доходов: {incoming}\n"
#     text += f"Сумма ваших расходов: {expenses}\n"
#     text += "Итого:\n"
#     result = expenses + incoming
#     text += f"{result}"
#     bot.send_message(callback.message.chat.id,
#                      text,
#                      reply_markup=back_to_menu)
