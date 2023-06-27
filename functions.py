import sqlite3
import random
import logging
import inspect
import itertools
import datetime
import time
import telebot

import config


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def count_associated_manager(user_id):
    """Checks does user have related manager or not."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    related_number = cursor.execute(f'''SELECT COUNT(user_id) 
                                    FROM associated_managers 
                                    WHERE user_id="{user_id}"
                                    ''').fetchall()[0][0]

    cursor.close()
    database.close()

    return related_number


def get_associated_manager(user_id):
    """Gets user's related manager's name and username."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    manager_info = cursor.execute(f'''SELECT manager_name, manager_username
                                  FROM associated_managers 
                                  WHERE user_id="{user_id}"
                                  ''').fetchall()[0]

    cursor.close()
    database.close()

    manager_name = manager_info[0]
    manager_username = manager_info[1]

    return manager_name, manager_username


def choose_manager():
    """Selects a manager to relate with user."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    manager_info = cursor.execute('''
                        SELECT manager_name, manager_username
                        FROM managers
                        WHERE clients = (
                            SELECT MIN(clients)
                            FROM managers
                        )
                    ''').fetchall()
    
    cursor.close()
    database.close()

    manager_info = random.choice(manager_info)

    manager_name = manager_info[0]
    manager_username = manager_info[1]

    return manager_name, manager_username


def associate_manager(user_id, manager_name, manager_username):
    """Adds information about related user and manager to the associated_managers table."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    cursor.execute(f'''
            INSERT INTO associated_managers (user_id, manager_name, manager_username)
            VALUES ("{user_id}", "{manager_name}", "{manager_username}")
            ''')
    
    database.commit()
    cursor.close()
    database.close()

    count = count_clients(manager_username)
    increase_clients(manager_username, count)

    logging.info(f'{inspect.currentframe().f_code.co_name}: В таблицу "associated_manager" добавлена запись. Пользователь ({user_id}) - менеджер ({manager_username})')


def add_user(message):
    """Adds information about new users to database."""

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_username = message.from_user.username

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    user = check_user(user_id)

    if not user:
        database = sqlite3.connect("china_travel.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()

        join_date = datetime.datetime.utcnow()
        
        cursor.execute(f'''
                INSERT INTO users (user_id, user_name, user_username, join_date)
                VALUES ("{user_id}", "{user_name}", "{user_username}", "{join_date}")
                ''',)

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: В таблицу "users" добавлена запись. Пользователь ({user_id}).')


def check_user(user_id):
    """Checks if user already in database."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    user = cursor.execute(f"SELECT user_name from users WHERE user_id='{user_id}'").fetchall()

    cursor.close()
    database.close()

    if user == []:
        return False
    
    return True


def track_action(user_id, action):
    """Track actions if it was performed for the first time."""

    action_performed, count = check_action(user_id, action)

    if action_performed == 0:
        database = sqlite3.connect("china_travel.db")
        cursor = database.cursor()

        cursor.execute(f'''
            UPDATE users
            SET {action}=1, actions={count + 1}
            WHERE user_id="{user_id}"
            ''')


        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Обновлена таблица "users", выполнено действие {action}.')

        return True

    return False


def check_action(user_id, action):
    """Checks if action were performed."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    data = cursor.execute(f"SELECT {action}, actions from users WHERE user_id='{user_id}'").fetchall()[0]
    action = data[0]
    count = data[1]

    cursor.close()
    database.close()

    return action, count


def manager_action(manager_username, user_username):
    """Adds a 'manager action' to users table."""

    user_id = get_user_id(user_username)
    related_manager_username = get_associated_manager_username(user_id)

    if related_manager_username == manager_username:
        first_contact = track_action(user_id, 'manager')

        if first_contact:
            return True
    
    return False


def get_managers():
    """Gets managers ids from managers table."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    managers = cursor.execute(f"SELECT DISTINCT manager_id FROM managers").fetchall()

    cursor.close()
    database.close()

    managers = itertools.chain.from_iterable(managers)

    return managers


def get_user_id(user_username):
    """Gets users id based on username."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    user_id = cursor.execute(f"SELECT user_id FROM users WHERE user_username='{user_username}'").fetchall()

    cursor.close()
    database.close()

    if user_id !=[]:
        user_id = user_id[0][0]
    
    return user_id


def get_associated_manager_username(user_id):
    """Gets related managers username based on user's id."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    manager_username = cursor.execute(f"SELECT manager_username FROM associated_managers WHERE user_id='{user_id}'").fetchall()

    if manager_username != []:
        manager_username = manager_username[0][0]

    cursor.close()
    database.close()

    return manager_username


def count_clients(manager_username):
    """Gets clients amount from managers table."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    count = cursor.execute(f"SELECT clients FROM managers WHERE manager_username='{manager_username}'").fetchall()[0][0]

    cursor.close()
    database.close()

    return count


def increase_clients(manager_username, count):
    """Increase clients count for manager."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    cursor.execute(f'''
            UPDATE managers
            SET clients={count + 1}
            WHERE manager_username="{manager_username}"
            ''')
    
    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Добавлен клиент {manager_username}.')


def construct_reply(user_username):
    """Constructs reply message when manager adds a user who contacted him."""

    data = get_user_actions(user_username)

    actions = ['stock', 'reviews', 'networks', 'addresses', 'details', 'cost', 'terms', 'poizon', 'alipay', 'currency', 'contract', 'download', 'shipment']

    results = {}

    for num in range(len(actions)):
        if data[num] == 0:
            results[actions[num]] = 'не просмотрено'
        else:
            results[actions[num]] = 'просмотрено'

    actions_count = data[13]
    
    reply_text = f'''
                \nПользователь @{user_username} совершил *{actions_count}* действий:\
                \n1. *О складе*: {results['stock']}\
                \n2. *Отзывы*: {results['reviews']}\
                \n3. *Социальные сети*: {results['networks']}\
                \n4. *Адреса складов*: {results['addresses']}\
                \n5. *Реквизиты*: {results['details']}\
                \n6. *Стоимость доставки*: {results['cost']}\
                \n7. *Условия по выкупу*: {results['terms']}\
                \n8. *Poizon*: {results['poizon']}\
                \n9. *Alipay*: {results['alipay']}\
                \n10. *Курс доллара и юаня*: {results['currency']}\
                \n11. *Шаблон договора*: {results['contract']}\
                \n12. *Бланк заявки*: {results['download']}\
                \n13. *Калькулятор доставки*: {results['shipment']}\
                '''
    
    return reply_text


def get_user_actions(user_username):
    """Get information about what actions user was performed."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    data = cursor.execute(f'''
                        SELECT stocks, reviews, networks, addresses, details, cost, terms, poizon, alipay, currency, contract, download, shipment, actions
                        FROM users
                        WHERE user_username="{user_username}"
                    ''').fetchall()[0]
    
    cursor.close()
    database.close()

    return data


def filter_users():
    """Gets users who didn't contact manager after bot usage."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    time_filter = datetime.datetime.utcnow() - datetime.timedelta(minutes=config.INFORM_TIME)

    usernames = cursor.execute(f'''
                        SELECT DISTINCT user_username
                        FROM users
                        WHERE manager=False and retarget=False and join_date<"{time_filter}"
                    ''').fetchall()
    
    cursor.close()
    database.close()

    if usernames != []:
        usernames = itertools.chain.from_iterable(usernames)

    return usernames


def inform_managers():
    """Informs managers about users, who didn't contact them."""
    
    while True:
        usernames = filter_users()

        for username in usernames:
            if username != 'None':
                user_id = get_user_id(username)
                managers = get_managers()

                if user_id not in managers:
                    text = construct_reply(username, user_id)
                    manager_username = get_associated_manager_username(user_id)
                    manager_id = get_manager_id(manager_username)
                    reply_text = f'Пользователь не связался с вами по прошествии {config.INFORM_TIME} минут.{text}'

                    try:
                        bot.send_message(chat_id=manager_id,
                                        text=reply_text,
                                        parse_mode='Markdown',
                                        )
                        change_redirect_status(user_id)
                    except:
                        pass

        time.sleep(60)


def get_manager_id(manager_username):
    """Gets managers id based on his username."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()


    manager_id = cursor.execute(f"SELECT manager_id FROM managers WHERE manager_username='{manager_username}'").fetchall()
    
    cursor.close()
    database.close()

    if manager_id != []:
        manager_id = manager_id[0][0]
    
    return manager_id


def change_redirect_status(user_id):
    """Changes user's redirect status, when manager was informed."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    cursor.execute(f'''
        UPDATE users
        SET retarget=1
        WHERE user_id="{user_id}"
        ''')

    database.commit()
    cursor.close()
    database.close()

    logging.info(f'{inspect.currentframe().f_code.co_name}: Изменен статус информирования {user_id}.')


def construct_users_stat():
    """Gets statistic about users."""

    users = get_user_without_stat()
    change_user_stat(users)
    reply_info = construct_stat_reply(users)
    replies = construct_text_reply(reply_info)

    return replies


def get_user_without_stat():
    """Gets users whose stats hasn't checked yet."""

    database = sqlite3.connect("china_travel.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = database.cursor()

    users = cursor.execute(f"SELECT user_id, user_username, join_date, manager FROM users WHERE stats=False").fetchall()

    cursor.close()
    database.close()

    return users


def change_user_stat(users):
    """Changes users stats when it checked."""

    database = sqlite3.connect("china_travel.db")
    cursor = database.cursor()

    for user in users:
        cursor.execute(f'''
            UPDATE users
            SET stats=1
            WHERE user_id="{user[0]}"
            ''')
        
        database.commit()
    
    cursor.close()
    database.close()


def construct_stat_reply(users):
    """Puts information together when user asks for stat."""

    reply_info = []
    for user in users:
        manager_name, manager_username = get_associated_manager(user[0])
        reply_info.append((user[1], manager_username, user[2].strftime("%d.%m.%Y %H:%M"), user[3], user[0]))

    return reply_info


def construct_text_reply(reply_info):
    """Converts information to a reply text."""

    replies = []
    count = 0
    reply_text = ''

    managers = get_managers()

    for info in reply_info:
        if info[3] == 0:
            manager = 'связался'
        else:
            manager = 'не связался'

        if info[4] not in managers:
            reply_text += f'Пользователь: @{info[0]} - @{info[1]}, {info[2]} ({manager}).\n'
        count += 1

        if count == 50 or count == len(reply_info):
            replies.append(reply_text)
            reply_text = ''
            count = 0
    
    return replies