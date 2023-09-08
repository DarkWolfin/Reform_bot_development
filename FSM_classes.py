from aiogram.dispatcher.filters.state import StatesGroup, State


class MultiDialog(StatesGroup):
    quick_help = State()
    getToken = State()
    setToken = State()
    menu = State()
    practices = State()
    tests = State()
    test_weariness = State()
    test_stress = State()
    test_selfefficacy = State()
    test_control = State()
    test_typeperson = State()
    habits = State()
    sleep_habit = State()
    water_habit = State()
    reading_habit = State()
    body_habit = State()
    courses = State()
    course_anxiety = State()
    specialist = State()
    tech_support = State()


class HabitSleep(StatesGroup):
    none = State()
    choose_action = State()
    choose_bedtime = State()
    choose_wakeup = State()


class HabitWater(StatesGroup):
    none = State()
    choose_action = State()
    choose_amount_of_portion = State()
    choose_schedule = State()


class Admin(StatesGroup):
    mailing_all = State()
    smart_mailing = State()
    send_to_user_id =State()
    send_to_user_message = State()


class Feedback(StatesGroup):
    answer_1_yn = State()
    answer_2_choose = State()
    answer_3_choose = State()
    answer_4 = State()
    answer_5 = State()
    answer_6 = State()
    answer_extra = State()


class FB_marathon(StatesGroup):
    answer_1 = State()
    answer_2 = State()
    answer_3 = State()
    answer_4 = State()
    answer_5 = State()
    answer_6 = State()
    answer_7 =State()


class adminCommands(StatesGroup):
    getUserReportPassword = State()
    getUserReport = State()
    getUserReportId = State()
    getUserReportDate = State()
    getUserActionPassword = State()
    getUserActionId = State()
    getUserActionDate = State()
    getUserActionShortPassword = State()
    getUserActionShortId = State()
    getUserActionShortDate = State()
    getUserReportGraphDate = State()
    receiving_feedback_password = State()
    FB_marathon_password = State()
