from aiogram.dispatcher.filters.state import StatesGroup, State


class MultiDialog(StatesGroup):
    menu = State()
    practices = State()
    tests = State()
    test_weariness = State()
    test_stress = State()
    test_selfefficacy = State()
    test_control = State()
    test_typeperson = State()
    test_motivation = State()
    habits = State()
    sleep_habit = State()
    reading_habit = State()
    water_habit = State()
    body_habit = State()
    courses = State()
    course_anxiety = State()
    specialist = State()


class HabitSleep(StatesGroup):
    none = State()
    choose_action = State()
    choose_bedtime = State()
    choose_wakeup = State()


class Admin(StatesGroup):
    mailing_all = State()
