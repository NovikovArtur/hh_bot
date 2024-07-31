from telebot import types
from ..models import *


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


def cv_bull(callback):
    try:
        CvModel.objects.filter(user_id__user_id=callback.from_user.id)
        return 1
    except:
        return 0
