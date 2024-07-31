from .commands import *
from .function import *
from .states import *
from .texts import *

hideBoard = types.ReplyKeyboardRemove()


@bot.callback_query_handler(lambda callback: callback.data in 'Об авторах')
def about_avtors(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    bot.send_message(callback.message.chat.id,
                     "Привет!\nЕсли вы зашли сюда, значит вам действительно понравился мой бот)"
                     "\nЕго разработчиком является Новиков Артур, студент 2-го курса ВШЭ. "
                     "Если вы хотите такого же бота (можно сложнее), то пишите на почту artur.novikov.my@gmail.com",
                     reply_markup=back_to_menu_total)


@bot.callback_query_handler(lambda callback: callback.data in TEXT.main_menu)
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


@bot.callback_query_handler(lambda callback: callback.data in TEXT.work_with_smth)
def work_with_cv(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    if callback.data in TEXT.work_with_cv:
        bot.send_message(callback.message.chat.id,
                         "В этом разделе ты можешь сделать различные вещи с твоим резюме "
                         "или добавить новое",
                         reply_markup=keyboard_work_with_CV)
    elif callback.data in TEXT.work_with_project:
        bot.send_message(callback.message.chat.id,
                         "В этом разделе ты можешь сделать различные вещи с твоим проектом "
                         "или добавить новый",
                         reply_markup=keyboard_work_with_project)
    else:
        bot.send_message(callback.message.chat.id,
                         "В этом разделе ты можешь сделать различные вещи с твоими вакансиями в проектах "
                         "или добавить новые",
                         reply_markup=keyboard_work_with_vacancy)
    bot.set_state(callback.from_user.id, HH.look_all_smth, callback.message.chat.id)


@bot.callback_query_handler(lambda callback: callback.data in TEXT.smth_create, state=HH.look_all_smth)
def smth_create(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    user = UserModel.objects.get(user_id=callback.from_user.id)
    user.from_where = str(callback.data)
    user.save()
    if callback.data == 'Добавить резюме':
        bot.send_message(callback.message.chat.id,
                         "Введите название резюме.\n\nВАЖНО: по названию резюме будет осуществляться "
                         "поиск подходящих вам вакансий в проектах, поэтому стоит писать название профессии.",
                         reply_markup=back_to_menu_cv)
    else:
        bot.send_message(callback.message.chat.id,
                         "Введите название проекта.",
                         reply_markup=back_to_menu_project)
    bot.set_state(callback.from_user.id, HH.wait_name_smth, callback.message.chat.id)


@bot.message_handler(state=HH.wait_name_smth)
def wait_name_smth(message: types.Message):
    from_where = UserModel.objects.get(user_id=message.from_user.id).from_where
    try:
        if from_where == 'Добавить резюме':
            CvModel.objects.get(user_id__user_id=message.from_user.id,
                                cv_name=str(message.text))
            bot.send_message(message.chat.id,
                             f"Название резюме {str(message.text)} уже есть. Пожалуйста, "
                             f"удалите или отредактируйте имеющееся резюме с таким названием, "
                             f"или выберите другое название для резюме.",
                             reply_markup=back_to_menu_cv)
        else:
            ProjectModel.objects.get(user_id__user_id=message.from_user.id,
                                     project_name=str(message.text))
            bot.send_message(message.chat.id,
                             f"Название проекта {str(message.text)} уже есть. Пожалуйста, "
                             f"удалите или отредактируйте имеющийся проект с таким названием, "
                             f"или выберите другое название для проекта.",
                             reply_markup=back_to_menu_project)
        bot.delete_state(message.from_user.id, message.chat.id)
    except:
        answer = str(message.text)
        user = UserModel.objects.get(user_id=message.from_user.id)
        user.answer = answer
        user.save()
        if from_where == 'Добавить резюме':
            bot.send_message(message.chat.id,
                             f"Название резюме: {answer}\nВведите текст вашего резюме.")
        else:
            bot.send_message(message.chat.id,
                             f"Название проекта: {answer}\nВведите описание вашего проекта.")
        bot.set_state(message.from_user.id, HH.wait_description_smth, message.chat.id)


@bot.message_handler(state=HH.wait_description_smth)
def wait_description_smth(message: types.Message):
    name_smth = UserModel.objects.get(user_id=message.from_user.id).answer
    text_smth = str(message.text)
    from_where = UserModel.objects.get(user_id=message.from_user.id).from_where
    if from_where == 'Добавить резюме':
        cv = CvModel()
        cv.user_id = UserModel.objects.get(user_id=message.from_user.id)
        cv.cv_name = name_smth
        cv.cv_text = text_smth
        cv.save()
        bot.send_message(message.chat.id,
                         f"Название резюме: {name_smth}\nРезюме: {text_smth}\n\nСохранено!",
                         reply_markup=back_to_menu_cv)
    else:
        project = ProjectModel()
        project.user_id = UserModel.objects.get(user_id=message.from_user.id)
        project.project_name = name_smth
        project.project_text = text_smth
        project.save()
        bot.send_message(message.chat.id,
                         f"Название проекта: {name_smth}\nОписание: {text_smth}\n\nСохранено!",
                         reply_markup=back_to_menu_project)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(lambda callback: callback.data in TEXT.smth_read_update_delite,
                            state=HH.look_all_smth)
def smth_read_update_delite(callback):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    from_where = str(callback.data)
    user = UserModel.objects.get(user_id=callback.from_user.id)
    user.from_where = from_where
    user.save()
    bull = smth_bull(callback, from_where)
    if bull:
        keyboard_cv_read = types.InlineKeyboardMarkup()
        if from_where in TEXT.cv_read_update_delite:
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
                             "Выберите резюме:",
                             reply_markup=keyboard_cv_read)
        elif from_where in TEXT.project_read_update_delite:
            names_project = ProjectModel.objects.filter(user_id__user_id=callback.from_user.id)
            names_project_name = [name_project.project_name for name_project in names_project]
            for name_project in names_project_name:
                keyboard_cv_read.add(types.InlineKeyboardButton(text=name_project,
                                                                callback_data=name_project))
            keyboard_cv_read.add(types.InlineKeyboardButton(text="Назад, к работе с проектами",
                                                            callback_data="Назад, к работе с проектами"))
            keyboard_cv_read.add(types.InlineKeyboardButton(text="К главному меню",
                                                            callback_data="К главному меню"))
            bot.send_message(callback.message.chat.id,
                             "Выберите проект:",
                             reply_markup=keyboard_cv_read)
        bot.set_state(callback.from_user.id, HH.wait_click_on_smth_name, callback.message.chat.id)
    else:
        if from_where in TEXT.cv_read_update_delite:
            bot.send_message(callback.message.chat.id,
                             "У вас пока нет резюме",
                             reply_markup=back_to_menu_cv)
        elif from_where in TEXT.project_read_update_delite:
            bot.send_message(callback.message.chat.id,
                             "У вас пока нет проекта",
                             reply_markup=back_to_menu_project)


@bot.callback_query_handler(lambda callback: True, state=HH.wait_click_on_smth_name)
def wait_click_on_smth_name(callback: types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    answer = str(callback.data)
    if answer == 'К главному меню':
        main_menu(callback)
    if answer == 'Назад, к работе с резюме':
        work_with_cv(callback)
    else:
        from_where = UserModel.objects.get(user_id=callback.from_user.id).from_where
        if from_where == 'Посмотреть свои резюме':
            cv_description = CvModel.objects.get(user_id__user_id=callback.from_user.id,
                                                 cv_name=answer).cv_text
            bot.send_message(callback.message.chat.id,
                             f"Ваше резюме по вакансии {answer}:\n\n{cv_description}",
                             reply_markup=back_to_menu_cv)
        elif from_where == 'Посмотреть свои проекты':
            project_description = ProjectModel.objects.get(user_id__user_id=callback.from_user.id,
                                                           project_name=answer).project_text
            bot.send_message(callback.message.chat.id,
                             f"Описание вашего проекта {answer}:\n\n{project_description}",
                             reply_markup=back_to_menu_project)
        elif from_where == 'Удалить резюме':
            cv = CvModel.objects.get(user_id__user_id=callback.from_user.id,
                                     cv_name=answer)
            cv.delete()
            bot.send_message(callback.message.chat.id,
                             f"Ваше резюме удалено",
                             reply_markup=back_to_menu_cv)
        elif from_where == 'Удалить проект':
            project = ProjectModel.objects.get(user_id__user_id=callback.from_user.id,
                                               project_name=answer)
            project.delete()
            bot.send_message(callback.message.chat.id,
                             f"Ваше проект удален",
                             reply_markup=back_to_menu_project)
        elif from_where == 'Редактировать резюме':
            user = UserModel.objects.get(user_id=callback.from_user.id)
            user.answer = answer
            user.save()
            cv = CvModel.objects.get(user_id__user_id=callback.from_user.id)
            cv.delete()
            user = UserModel.objects.get(user_id=callback.from_user.id)
            user.from_where = 'Добавить резюме'
            user.save()
            bot.send_message(callback.message.chat.id,
                             f"Введите новый текст для вашего резюме {answer}")
            bot.set_state(callback.from_user.id, HH.wait_description_smth, callback.message.chat.id)
        elif from_where == 'Редактировать проект':
            user = UserModel.objects.get(user_id=callback.from_user.id)
            user.answer = answer
            user.save()
            project = ProjectModel.objects.get(user_id__user_id=callback.from_user.id)
            project.delete()
            user = UserModel.objects.get(user_id=callback.from_user.id)
            user.from_where = 'Добавить проект'
            user.save()
            bot.send_message(callback.message.chat.id,
                             f"Введите новое описание вашего проекта {answer}")
            bot.set_state(callback.from_user.id, HH.wait_description_smth, callback.message.chat.id)
