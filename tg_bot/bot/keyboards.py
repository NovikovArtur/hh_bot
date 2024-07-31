from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard_start = types.InlineKeyboardMarkup()
keyboard_start.add(types.InlineKeyboardButton(text="Полетели!",
                                              callback_data="Полетели!"))


back_to_menu_total = types.InlineKeyboardMarkup()
back_to_menu_total.add(types.InlineKeyboardButton(text="К главному меню",
                                                  callback_data="К главному меню"))


back_to_menu_cv = types.InlineKeyboardMarkup()
back_to_menu_cv.add(types.InlineKeyboardButton(text="Назад, к работе с резюме",
                                               callback_data="Назад, к работе с резюме"))
back_to_menu_cv.add(types.InlineKeyboardButton(text="К главному меню",
                                               callback_data="К главному меню"))


keyboard_work_with_CV = types.InlineKeyboardMarkup()
keyboard_work_with_CV.add(types.InlineKeyboardButton(text="Добавить резюме",
                                                     callback_data="Добавить резюме"))
keyboard_work_with_CV.add(types.InlineKeyboardButton(text="Редактировать резюме",
                                                     callback_data="Редактировать резюме"))
keyboard_work_with_CV.add(types.InlineKeyboardButton(text="Удалить резюме",
                                                     callback_data="Удалить резюме"))
keyboard_work_with_CV.add(types.InlineKeyboardButton(text="Посмотреть свои резюме",
                                                     callback_data="Посмотреть свои резюме"))
keyboard_work_with_CV.add(types.InlineKeyboardButton(text="К главному меню",
                                                     callback_data="К главному меню"))
