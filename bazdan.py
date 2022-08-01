import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta, timezone
from types import NoneType
import zoneinfo



def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f'The error {e} occured')
        
    return connection

connection = create_connection('.\\bd.sqlite')



def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f'The error {e} occured')


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'The error {e} occured')
        return 'Oops, something went wrong'


def example(query):
    res = execute_query(connection, query)
    return res

#example('delete from time_zone')

def set_new_reminder(user_id, text, date, priority):
    execute_query(connection, f"insert into reminders (id_user, reminder, reminder_date, priority) values ('{user_id}', '{text}', '{date}', '{priority}');")


def add_notifications(text, date, notification, user_id):
    for  notif in notification:
        hour = int(notif.split(':')[0])
        minut = int(notif.split(':')[1])
        delta = timedelta(hours=hour, minutes=minut)
        notification_time = date - delta
        if notif == '00:00':
            before_time = 0
        else:
            before_time = 1
        execute_query(connection, f"INSERT INTO notifications (reminder_id, notification_time, before_time) VALUES ((SELECT id FROM reminders WHERE reminder = '{text}' AND reminder_date = '{date}' AND id_user = '{user_id}'), '{notification_time}', {before_time} );")


def add_additional_notification(reminder_id, date, notification):
    hour = int(notification.split(':')[0])
    minut = int(notification.split(':')[1])
    delta = timedelta(hours=hour, minutes=minut)
    notification_time = date + delta

    execute_query(connection, f"INSERT INTO notifications (reminder_id, notification_time, before_time) VALUES ('{reminder_id}', '{notification_time}', 0);")


def create_time_zone(user_id, tz):
    res = execute_read_query(connection, f"select id_user from time_zone;")
    res = [r[0] for r in res]
    if res is None or str(user_id) not in res:
        execute_query(connection, f"insert into time_zone(id_user, tz) values('{user_id}', '{tz}');")
    else:
        execute_query(connection, f"update time_zone set tz = '{tz}' where id_user = '{user_id}'")


def show_users():
    result = execute_read_query(connection, "select id_user from time_zone;")
    result = [res[0] for res in result]
    return result


def get_tz(user_id):
    result = execute_read_query(connection,f"select tz from time_zone where id_user = '{user_id}';")

    return result[0][0]

def show_info():
    result = execute_read_query(connection, f"select id_user, reminder, notification_time, reminder_date, priority, reminder_id, before_time from notifications join reminders on notifications.reminder_id = reminders.id;")

    return result

def delete_reminder(user_id, id):
    execute_query(connection, f"delete from reminders where id_user = '{user_id}' and id = {id};")
    execute_query(connection, f"delete from notifications where reminder_id = '{id}'")

def show_delete_reminder(user_id):

    result = execute_read_query(connection, f"select reminder, reminder_date, id from reminders where id_user = '{user_id}' order by reminder_date;")

    tz = zoneinfo.ZoneInfo(get_tz(user_id))

    result_dic = {}
    for res in result:
        date = datetime.fromisoformat(res[1]).astimezone(tz)
        st = str(date.date()) +'  ' + str(date.time()) + ' \n' + str(res[0])
        result_dic[st] = res[2]
    if result == []:
        result_dic = "You don't have any reminders"
    return result_dic



def show_reminders(user_id, period, time=None, date=None):
    dictionary = {}

    if period == 'previous':
        result = execute_read_query(connection, f"select reminder, reminder_date, priority from reminders where id_user = '{user_id}' and reminder_date < '{time}';")
        st = 'Previous reminders:\n\n'


    elif period == 'today':

        result = execute_read_query(connection, f"select reminder, reminder_date, priority from reminders where id_user = '{user_id}' and reminder_date between '{date}' and '{date + timedelta(days=1)}' order by reminder_date;")
        st = f'Reminders for {date}:\n\n'

    elif period == 'week':
        result = execute_read_query(connection, f"select reminder, reminder_date, priority from reminders where id_user = '{user_id}' and strftime('%W', reminder_date) = strftime('%W', '{date}');")
        st = f'Reminders for current week:\n\n'
        
    elif period == 'month':
        result = execute_read_query(connection, f"select reminder, reminder_date, priority from reminders where id_user = '{user_id}' and strftime('%m', reminder_date) = strftime('%m', '{date}');")
        st = 'Reminders for current month:\n\n'
    
    elif period == 'all':
        result = execute_read_query(connection, f"select reminder, reminder_date, priority from reminders where id_user = '{user_id}' order by reminder_date;")
        st = 'All your reminders:\n\n'

    tz = zoneinfo.ZoneInfo(get_tz(user_id))
    if result == [] or result is NoneType:
        st += "You don't have any reminders"
    else:
        for res in result:
            if res[2] == 1:
                st += '! '
            date = datetime.fromisoformat(res[1]).astimezone(tz)
            st += str(date.date()) +'  ' + str(date.time()) + ' \n' + str(res[0]) + '\n\n'

    return st


create_table_reminders = '''
CREATE TABLE IF NOT EXISTS reminders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user TEXT,
    reminder TEXT,
    reminder_date DATETIME,
    priority INTEGER
    );
'''


create_table_notifications = '''
CREATE TABLE IF NOT EXISTS notifications(
    id INTEGER  PRIMARY KEY AUTOINCREMENT,
    reminder_id INTEGER,
    notification_time DATETIME,
    before_time INTEGER,
    FOREIGN KEY (reminder_id) 
    REFERENCES reminders (id) 
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
'''

create_table_time_zone = '''
CREATE TABLE IF NOT EXISTS time_zone(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user TEXT,
    tz TEXT
);'''
