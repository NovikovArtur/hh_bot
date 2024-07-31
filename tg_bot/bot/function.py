from telebot import types
from ..models import *
from .texts import *


def main_menu_keyboard(callback):
    keyboard_main_menu = types.InlineKeyboardMarkup()
    keyboard_main_menu.add(types.InlineKeyboardButton(text="Работа с резюме",
                                                      callback_data="Работа с резюме"))
    keyboard_main_menu.add(types.InlineKeyboardButton(text="Работа с проектами",
                                                      callback_data="Работа с проектами"))
    projects = ProjectModel.objects.filter(user_id__user_id=callback.from_user.id)
    projects_text = [project.project_name for project in projects]
    if projects_text != []:
        ProjectModel.objects.filter(user_id__user_id=callback.from_user.id)
        keyboard_main_menu.add(types.InlineKeyboardButton(text="Добавить вакансии в проект",
                                                          callback_data="Добавить вакансии в проект"))
    keyboard_main_menu.add(types.InlineKeyboardButton(text="Об авторах",
                                                      callback_data="Об авторах"))
    return keyboard_main_menu


def smth_bull(callback, from_where):
    if from_where in TEXT.cv_read_update_delite:
        cvs = CvModel.objects.filter(user_id__user_id=callback.from_user.id)
        cvs_name = [cv.cv_name for cv in cvs]
        if cvs_name != []:
            return 1
        else:
            return 0
    elif from_where in TEXT.project_read_update_delite:
        projects = ProjectModel.objects.filter(user_id__user_id=callback.from_user.id)
        projects_name = [project.project_name for project in projects]
        if projects_name != []:
            return 1
        else:
            return 0
