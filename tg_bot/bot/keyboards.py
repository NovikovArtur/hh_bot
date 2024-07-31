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


back_to_menu_project = types.InlineKeyboardMarkup()
back_to_menu_project.add(types.InlineKeyboardButton(text="Назад, к работе с проектами",
                                                    callback_data="Назад, к работе с проектами"))
back_to_menu_project.add(types.InlineKeyboardButton(text="К главному меню",
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


keyboard_work_with_project = types.InlineKeyboardMarkup()
keyboard_work_with_project.add(types.InlineKeyboardButton(text="Добавить проект",
                                                          callback_data="Добавить проект"))
keyboard_work_with_project.add(types.InlineKeyboardButton(text="Редактировать проект",
                                                          callback_data="Редактировать проект"))
keyboard_work_with_project.add(types.InlineKeyboardButton(text="Удалить проект",
                                                          callback_data="Удалить проект"))
keyboard_work_with_project.add(types.InlineKeyboardButton(text="Посмотреть свои проекты",
                                                          callback_data="Посмотреть свои проекты"))
keyboard_work_with_project.add(types.InlineKeyboardButton(text="К главному меню",
                                                          callback_data="К главному меню"))


keyboard_work_with_vacancy = types.InlineKeyboardMarkup()
keyboard_work_with_vacancy.add(types.InlineKeyboardButton(text="Добавить вакансию",
                                                          callback_data="Добавить вакансию"))
keyboard_work_with_vacancy.add(types.InlineKeyboardButton(text="Редактировать вакансию",
                                                          callback_data="Редактировать вакансию"))
keyboard_work_with_vacancy.add(types.InlineKeyboardButton(text="Удалить вакансию",
                                                          callback_data="Удалить вакансию"))
keyboard_work_with_vacancy.add(types.InlineKeyboardButton(text="Посмотреть свои вакансии",
                                                          callback_data="Посмотреть свои вакансии"))
keyboard_work_with_vacancy.add(types.InlineKeyboardButton(text="К главному меню",
                                                          callback_data="К главному меню"))
