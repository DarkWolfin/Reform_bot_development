import sqlite3 as sq
from datetime import datetime, timedelta


async def db_start():
    global db_data, cur_data, db_test_weariness, cur_test_weariness, db_test_selfefficacy, cur_test_selfefficacy, cur_test_stress, db_test_control, cur_test_control, db_test_typeperson, cur_test_typeperson, \
        db_habit_sleep, cur_habit_sleep, db_course_anxiety, cur_course_anxiety, db_user_interactions, db_test_stress, cur_user_interactions, db_test_holms, cur_test_holms, db_helpsystem, cur_helpsystem, db_quiz, cur_quiz

    db_data = sq.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    cur_data.execute(
        "CREATE TABLE IF NOT EXISTS profile(user_id INT PRIMARY KEY, first_name TEXT, username TEXT, active TEXT, token TEXT)")
    db_data.commit()
    cur_data.execute(
        "CREATE TABLE IF NOT EXISTS affirmation(user_id INT PRIMARY KEY, first_name TEXT, username TEXT)")
    db_data.commit()
    cur_data.execute(
        "CREATE TABLE IF NOT EXISTS NEW_affirmation(user_id INT PRIMARY KEY, username TEXT, token TEXT, agree TEXT)")
    db_data.commit()
    cur_data.execute(
        "CREATE TABLE IF NOT EXISTS feedback_2(user_id INT PRIMARY KEY, token TEXT, answer_1 TEXT, answer_2 TEXT, answer_3 TEXT, answer_4 TEXT, answer_5 TEXT, answer_6 TEXT, answer_7 TEXT)")
    db_data.commit()
    cur_data.execute(
        "CREATE TABLE IF NOT EXISTS FB_marathon_3(user_id INT PRIMARY KEY, token TEXT, answer_1 TEXT, answer_2 TEXT, answer_3 TEXT, answer_4 TEXT, answer_5 TEXT, answer_6 TEXT, answer_7 TEXT)")
    db_data.commit()
    db_data.execute("PRAGMA journal_mode=WAL")


    #help system
    db_helpsystem = sq.connect('Databases/Help_system.db')
    cur_helpsystem = db_helpsystem.cursor()
    cur_helpsystem.execute(
        "CREATE TABLE IF NOT EXISTS good(user_id INT PRIMARY KEY, username TEXT, token TEXT, time TEXT, try_practice TEXT)")
    db_helpsystem.commit()
    cur_helpsystem.execute(
        "CREATE TABLE IF NOT EXISTS norm(user_id INT PRIMARY KEY, username TEXT, token TEXT, time TEXT, better TEXT, sport TEXT, cause_sport TEXT, food TEXT, sleep TEXT, marathon TEXT)")
    db_helpsystem.commit()
    cur_helpsystem.execute(
        "CREATE TABLE IF NOT EXISTS bad(user_id INT PRIMARY KEY, username TEXT, token TEXT, time TEXT, type_problem TEXT, p_workplace TEXT, p_food TEXT, p_marathon TEXT,  d_elaboration TEXT, d_circumstance TEXT, d_influence TEXT, d_probability TEXT, d_actions TEXT, d_ruin TEXT, d_correct TEXT, d_thought TEXT, d_close TEXT, d_success TEXT, d_barrier TEXT)")
    db_helpsystem.commit()
    cur_helpsystem.execute(
        "CREATE TABLE IF NOT EXISTS agreement(user_id INT PRIMARY KEY, username TEXT, token TEXT, time TEXT, choice TEXT, state TEXT, subject TEXT)")
    db_helpsystem.commit()
    db_helpsystem.execute("PRAGMA journal_mode=WAL")


    #quiz
    db_quiz = sq.connect('Databases/Quiz.db')
    cur_quiz = db_quiz.cursor()
    cur_quiz.execute(
        "CREATE TABLE IF NOT EXISTS workload(user_id INT PRIMARY KEY, username TEXT, token TEXT, time TEXT, agree TEXT, cause TEXT, answer_1 TEXT, answer_1_details TEXT, answer_2 TEXT, answer_2_details TEXT, answer_3 TEXT, answer_4 TEXT, answer_5 TEXT, answer_6 TEXT, answer_7 TEXT, answer_8 TEXT, answer_9 TEXT)")
    db_quiz.commit()
    db_quiz.close()
    # db_quiz.execute("PRAGMA journal_mode=WAL")


    db_test_weariness = sq.connect('Databases/Result_Tests/PSY_Weariness.db')
    cur_test_weariness = db_test_weariness.cursor()
    # cur_test_weariness.execute("DROP TABLE IF EXISTS answers")
    cur_test_weariness.execute(
        "CREATE TABLE IF NOT EXISTS answers(user_id INT PRIMARY KEY, username TEXT, countOfAnswers INT, answer1 TEXT, answer2 TEXT, answer3 TEXT, answer4 TEXT, answer5 TEXT, answer6 TEXT, "
        "answer7 TEXT, answer8 TEXT, answer9 TEXT, answer10 TEXT, answer11 TEXT, answer12 TEXT, answer13 TEXT, answer14 TEXT, answer15 TEXT, answer16 TEXT, "
        "answer17 TEXT, answer18 TEXT, answer19 TEXT, answer20 TEXT, answer21 TEXT, answer22 TEXT, answer23 TEXT, answer24 TEXT, answer25 TEXT, answer26 TEXT, "
        "answer27 TEXT, answer28 TEXT, answer29 TEXT, answer30 TEXT, answer31 TEXT, answer32 TEXT, answer33 TEXT, answer34 TEXT, answer35 TEXT, answer36 TEXT)")
    db_test_weariness.commit()
    cur_test_weariness.execute(
        "CREATE TABLE IF NOT EXISTS points(user_id INT PRIMARY KEY, username TEXT, count INT, points INT)")
    db_test_weariness.commit()
    db_user_interactions = sq.connect('Databases/user_interactions.db')
    cur_user_interactions = db_user_interactions.cursor()
    cur_user_interactions.execute("CREATE TABLE IF NOT EXISTS users(user_id INT, action TEXT, time INT)")
    db_user_interactions.commit()

    ##################
    db_test_stress = sq.connect('Databases/Result_Tests/PSY_stress.db')
    cur_test_stress = db_test_stress.cursor()
    # cur_test_stress.execute("DROP TABLE IF EXISTS answers")
    cur_test_stress.execute(
        "CREATE TABLE IF NOT EXISTS answers(user_id INT PRIMARY KEY, username TEXT, countOfAnswers INT, answer1 TEXT, answer2 TEXT, answer3 TEXT, answer4 TEXT, answer5 TEXT, answer6 TEXT, "
        "answer7 TEXT, answer8 TEXT, answer9 TEXT, answer10 TEXT, answer11 TEXT, answer12 TEXT, answer13 TEXT, answer14 TEXT, answer15 TEXT, answer16 TEXT, "
        "answer17 TEXT, answer18 TEXT, answer19 TEXT, answer20 TEXT, answer21 TEXT, answer22 TEXT, answer23 TEXT, answer24 TEXT, answer25 TEXT, answer26 TEXT, "
        "answer27 TEXT, answer28 TEXT, answer29 TEXT, answer30 TEXT, answer31 TEXT, answer32 TEXT, answer33 TEXT)")
    db_test_stress.commit()
    cur_test_stress.execute(
        "CREATE TABLE IF NOT EXISTS points(user_id INT PRIMARY KEY, username TEXT, count INT, points INT)")
    db_test_stress.commit()
    ##################

    db_test_selfefficacy = sq.connect('Databases/Result_Tests/PSY_Selfefficacy.db')
    cur_test_selfefficacy = db_test_selfefficacy.cursor()
    cur_test_selfefficacy.execute(
        "CREATE TABLE IF NOT EXISTS points(user_id INT PRIMARY KEY, username TEXT, count INT, points INT)")
    db_test_selfefficacy.commit()

    db_test_control = sq.connect('Databases/Result_Tests/POP_Control.db')
    cur_test_control = db_test_control.cursor()
    cur_test_control.execute(
        "CREATE TABLE IF NOT EXISTS points(user_id INT PRIMARY KEY, username TEXT, count INT, points INT)")
    db_test_control.commit()

    db_test_typeperson = sq.connect('Databases/Result_Tests/POP_Typeperson.db')
    cur_test_typeperson = db_test_typeperson.cursor()
    cur_test_typeperson.execute(
        "CREATE TABLE IF NOT EXISTS points(user_id INT PRIMARY KEY, username TEXT, count INT, points INT)")
    db_test_typeperson.commit()

    db_habit_sleep = sq.connect('Databases/Current_habits.db')
    cur_habit_sleep = db_habit_sleep.cursor()
    cur_habit_sleep.execute(
        "CREATE TABLE IF NOT EXISTS sleep(user_id INT PRIMARY KEY, username TEXT, active TEXT, bedtime TEXT, wakeup TEXT)")
    db_habit_sleep.commit()

    db_habit_water = sq.connect('Databases/Current_habits.db')
    cur_habit_water = db_habit_water.cursor()
    cur_habit_water.execute(
        "CREATE TABLE IF NOT EXISTS water(user_id INT PRIMARY KEY, username TEXT, dayScheduleStart INT, interval INT, dayScheduleEnd INT, amountOfPortions INT, schedule TEXT)")
    db_habit_water.commit()
    cur_habit_water.execute(
        "CREATE TABLE IF NOT EXISTS waterDates(user_id INT PRIMARY KEY)")
    db_habit_water.commit()

    db_course_anxiety = sq.connect('Databases/Courses.db')
    cur_course_anxiety = db_course_anxiety.cursor()
    cur_course_anxiety.execute(
        "CREATE TABLE IF NOT EXISTS anxiety(user_id INT PRIMARY KEY, username TEXT, interested TEXT)")
    db_course_anxiety.commit()

    db_test_holms = sq.connect('Databases/Result_Tests/Holmes-Rahe.db')
    cur_test_holms = db_test_holms.cursor()
    cur_test_holms.execute(
        "CREATE TABLE IF NOT EXISTS answers(user_id INT PRIMARY KEY, username TEXT, countOfAnswers INT, answer1 TEXT, answer2 TEXT, answer3 TEXT, answer4 TEXT, answer5 TEXT, answer6 TEXT, "
        "answer7 TEXT, answer8 TEXT, answer9 TEXT, answer10 TEXT, answer11 TEXT, answer12 TEXT, answer13 TEXT, answer14 TEXT, answer15 TEXT, answer16 TEXT, "
        "answer17 TEXT, answer18 TEXT, answer19 TEXT, answer20 TEXT, answer21 TEXT, answer22 TEXT, answer23 TEXT, answer24 TEXT, answer25 TEXT, answer26 TEXT, "
        "answer27 TEXT, answer28 TEXT, answer29 TEXT, answer30 TEXT, answer31 TEXT, answer32 TEXT, answer33 TEXT, answer34 TEXT, answer35 TEXT, answer36 TEXT, "
        "answer37 TEXT, answer38 TEXT, answer39 TEXT, answer40 TEXT, answer41 TEXT, answer42 TEXT, answer43 TEXT)")
    db_test_holms.commit()
    cur_test_holms.execute(
        "CREATE TABLE IF NOT EXISTS points(user_id INT PRIMARY KEY, username TEXT, count INT, points INT)")
    db_test_holms.commit()


async def data_profile(user_id, first_name, username):
    user = cur_data.execute(
        "SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_data.execute("INSERT INTO profile VALUES(?, ?, ?, ?, '')",
                         (user_id, first_name, username, 'Активен'))
        db_data.commit()
    db_data.close()


async def data_feedback(user_id):
    user = cur_data.execute(
        "SELECT 1 FROM feedback_2 WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_data.execute("INSERT INTO feedback_2 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (user_id, '', '', '', '', '', '', '', ''))
        db_data.commit()
    db_data.close()


async def data_FB_marathon(user_id):
    user = cur_data.execute(
        "SELECT 1 FROM FB_marathon_3 WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_data.execute("INSERT INTO FB_marathon_3 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (user_id, '', '', '', '', '', '', '', ''))
        db_data.commit()
    db_data.close()


async def set_user_token(user_id, token):
    user = cur_data.execute(
        "SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()

    if user:
        cur_data.execute("UPDATE profile SET token = '{token}' WHERE user_id == '{id}'".format(
            token=token, id=user_id))
        db_data.commit()
    db_data.close()


async def NEW_affirmation(user_id, username):
    user = cur_data.execute(
        "SELECT 1 FROM NEW_affirmation WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_data.execute("INSERT INTO NEW_affirmation VALUES(?, ?, ?, ?)",
                         (user_id, username, '', ''))
        db_data.commit()
    db_data.close()


async def help_system_good(user_id):
    user = cur_helpsystem.execute(
        "SELECT 1 FROM good WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        timeNow = datetime.now()
        timeNow = str(timeNow)[:-7]
        cur_helpsystem.execute("INSERT INTO good VALUES(?, ?, ?, ?, ?)",
                         (user_id, str(cur_data.execute('SELECT username FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), str(cur_data.execute('SELECT token FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), timeNow, ''))
        db_helpsystem.commit()
    db_helpsystem.close()


async def help_system_norm(user_id):
    user = cur_helpsystem.execute(
        "SELECT 1 FROM norm WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        timeNow = datetime.now()
        timeNow = str(timeNow)[:-7]
        cur_helpsystem.execute("INSERT INTO norm VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (user_id, str(cur_data.execute('SELECT username FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), str(cur_data.execute('SELECT token FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), timeNow, '', '', '', '', '', ''))
        db_helpsystem.commit()
    db_helpsystem.close()


async def help_system_bad(user_id):
    user = cur_helpsystem.execute(
        "SELECT 1 FROM bad WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        timeNow = datetime.now()
        timeNow = str(timeNow)[:-7]
        cur_helpsystem.execute("INSERT INTO bad VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (user_id, str(cur_data.execute('SELECT username FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), str(cur_data.execute('SELECT token FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), timeNow, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''))
        db_helpsystem.commit()
    db_helpsystem.close()


async def help_system_agreement(user_id):
    user = cur_helpsystem.execute(
        "SELECT 1 FROM agreement WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        timeNow = datetime.now()
        timeNow = str(timeNow)[:-7]
        cur_helpsystem.execute("INSERT INTO agreement VALUES(?, ?, ?, ?, ?, ?, ?)",
                         (user_id, str(cur_data.execute('SELECT username FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), str(cur_data.execute('SELECT token FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), timeNow, '', '', ''))
        db_helpsystem.commit()
    db_helpsystem.close()


async def pre_quiz_workload(user_id):
    db_quiz = sq.connect('Databases/Quiz.db')
    cur_quiz = db_quiz.cursor()
    user = cur_quiz.execute(
        "SELECT 1 FROM workload WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        timeNow = datetime.now()
        timeNow = str(timeNow)[:7]
        cur_quiz.execute("INSERT INTO workload VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (user_id, str(cur_data.execute('SELECT username FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), str(cur_data.execute('SELECT token FROM profile WHERE user_id = ?', (user_id,)).fetchone()[0]), timeNow, '', '', '', '', '', '', '', '', '', '', '', '', ''))
        db_quiz.commit()
    db_quiz.close()


async def get_all_user_ids():
    return cur_data.execute("SELECT user_id FROM profile").fetchall()


async def affirmation(user_id, first_name, username):
    user = cur_data.execute(
        "SELECT 1 FROM affirmation WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_data.execute("INSERT INTO affirmation VALUES(?, ?, ?)",
                         (user_id, first_name, username))
        db_data.commit()


# PSY tests


async def pre_points_test_weariness(user_id, username):
    user = cur_test_weariness.execute(
        "SELECT 1 FROM points WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_weariness.execute("INSERT INTO points VALUES(?, ?, ?, ?)",
                                   (user_id, username, '', ''))
        db_test_weariness.commit()


async def pre_answers_test_weariness(user_id, username):
    user = cur_test_weariness.execute(
        "SELECT 1 FROM answers WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_weariness.execute(
            "INSERT INTO answers VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, 0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''))
        db_test_weariness.commit()


async def points_test_weariness(state, user_id):
    async with state.proxy() as data:
        cur_test_weariness.execute("UPDATE points SET count = '{}', points = '{}' WHERE user_id == '{}'".format(
            data['count'], data['points'], user_id))
        db_test_weariness.commit()


#######################
async def pre_points_test_holms(user_id, username):
    user = cur_test_holms.execute(
        "SELECT 1 FROM points WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_holms.execute("INSERT INTO points VALUES(?, ?, ?, ?)",
                               (user_id, username, '', ''))
        db_test_holms.commit()


async def pre_answers_test_holms(user_id, username):
    user = cur_test_holms.execute(
        "SELECT 1 FROM answers WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_holms.execute(
            "INSERT INTO answers VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, 0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''))
        db_test_holms.commit()


async def points_test_holms(state, user_id):
    async with state.proxy() as data:
        cur_test_holms.execute("UPDATE points SET count = '{}', points = '{}' WHERE user_id == '{}'".format(
            data['count'], data['points'], user_id))
        db_test_holms.commit()


####################

async def pre_points_test_stress(user_id, username):
    user = cur_test_stress.execute(
        "SELECT 1 FROM points WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_stress.execute("INSERT INTO points VALUES(?, ?, ?, ?)",
                                (user_id, username, '', ''))
        db_test_stress.commit()


async def pre_answers_test_stress(user_id, username):
    user = cur_test_stress.execute(
        "SELECT 1 FROM answers WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_stress.execute(
            "INSERT INTO answers VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, 0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
             '', '', '', '', '', '', '', '', '', '', '', ''))
        db_test_stress.commit()


async def points_test_stress(state, user_id):
    async with state.proxy() as data:
        cur_test_stress.execute("UPDATE points SET count = '{}', points = '{}' WHERE user_id == '{}'".format(
            data['count'], data['points'], user_id))
        db_test_stress.commit()


#######################


async def pre_points_test_selfefficacy(user_id, username):
    user = cur_test_selfefficacy.execute(
        "SELECT 1 FROM points WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_selfefficacy.execute("INSERT INTO points VALUES(?, ?, ?, ?)",
                                      (user_id, username, '', ''))
        db_test_selfefficacy.commit()


async def points_test_selfefficacy(state, user_id):
    async with state.proxy() as data:
        cur_test_selfefficacy.execute("UPDATE points SET count = '{}', points = '{}' WHERE user_id == '{}'".format(
            data['count'], data['points'], user_id))
        db_test_selfefficacy.commit()


# POP tests


async def pre_points_test_control(user_id, username):
    user = cur_test_control.execute(
        "SELECT 1 FROM points WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_control.execute("INSERT INTO points VALUES(?, ?, ?, ?)",
                                 (user_id, username, '', ''))
        db_test_control.commit()


async def points_test_control(state, user_id):
    async with state.proxy() as data:
        cur_test_control.execute("UPDATE points SET count = '{}', points = '{}' WHERE user_id == '{}'".format(
            data['count'], data['points'], user_id))
        db_test_control.commit()


async def pre_points_test_typeperson(user_id, username):
    user = cur_test_typeperson.execute(
        "SELECT 1 FROM points WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_test_typeperson.execute("INSERT INTO points VALUES(?, ?, ?, ?)",
                                    (user_id, username, '', ''))
        db_test_typeperson.commit()


async def points_test_typeperson(state, user_id):
    async with state.proxy() as data:
        cur_test_typeperson.execute("UPDATE points SET count = '{}', points = '{}' WHERE user_id == '{}'".format(
            data['count'], data['points'], user_id))
        db_test_typeperson.commit()


async def prehabit_sleep_db(user_id, username):
    user = cur_habit_sleep.execute(
        "SELECT 1 FROM sleep WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_habit_sleep.execute("INSERT INTO sleep VALUES(?, ?, ?, ?, ?)",
                                (user_id, username, '', '', ''))
        db_habit_sleep.commit()


async def prehabit_water_db(user_id, username):
    user = cur_habit_water.execute(
        "SELECT 1 FROM water WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_habit_water.execute("INSERT OR IGNORE INTO water VALUES(?, ?, ?, ?, ?, ?,?)",
                                (user_id, username, 0, 0, 0, 0, ''))
        print('123')
        db_habit_water.commit()
        cur_habit_water.execute("INSERT OR IGNORE INTO waterDates VALUES(?)",
                                (user_id,))
        db_habit_water.commit()


async def course_anxiety_db(user_id, username, interested):
    user = cur_course_anxiety.execute(
        "SELECT 1 FROM anxiety WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur_course_anxiety.execute("INSERT INTO anxiety VALUES(?, ?, ?)",
                                   (user_id, username, interested))
        db_course_anxiety.commit()


async def save_user_action(*, user_id=None, action=None):
    timeNow = datetime.now()
    timeNow = str(timeNow)[:-7]
    db_user_interactions = sq.connect('Databases/user_interactions.db')
    cur_user_interactions = db_user_interactions.cursor()
    cur_user_interactions.execute("INSERT INTO users VALUES(?, ?, ?)",
                                  (user_id, action, timeNow))
    db_user_interactions.commit()
