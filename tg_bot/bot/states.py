from telebot.handler_backends import State, StatesGroup


class HH(StatesGroup):
    wait_name_smth = State()
    wait_description_smth = State()
    wait_click_on_smth_name = State()
    look_all_smth = State()
    wait_choose_project = State()
    wait_name_vacancy = State()
    wait_description_vacancy = State()
    look_all_vacancy = State()
    wait_click_on_vacancy_name = State()
