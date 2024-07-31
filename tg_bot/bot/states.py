from telebot.handler_backends import State, StatesGroup


class HH(StatesGroup):
    wait_name_smth = State()
    wait_description_smth = State()
    wait_click_on_smth_name = State()
    look_all_smth = State()
