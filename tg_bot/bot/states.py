from telebot.handler_backends import State, StatesGroup


class HH(StatesGroup):
    wait_name_cv = State()
    wait_description_cv = State()
    wait_click_on_cv_name = State()
