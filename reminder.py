import telebot as tb
import bazdan as bd
import random
import requests
from datetime import datetime, timezone
import zoneinfo
from config import TELEGRAM_TOKEN, API_KEY

# Create bot connection
bot = tb.TeleBot(TELEGRAM_TOKEN)

# set list of questions
exercise = {'Find the area of a square with side 4': ['16', '8', '12', '20'], 'Find 2th root of 81': ['9', '8', '7', '11'], "What's the capital of Australia?": ['Canberra', 'Sydney', 'Vienna', 'Melbourne'], "What's the capital of Germany?": ['Berlin', 'Munich', 'Cologne', 'Moscow'], "What's the capital of Spain?": ['Madrid', 'Milan', 'Barcelona', 'Valencia'], "What's the capital of Canada?": ['Ottawa', 'Toronto', 'Quebec City', 'Halifax'], "Find factorial 3 (3!)": ['6', '9', '3', '1']}

# set dictionary for timezones
timezones = {'GMT 0': 'Etc/GMT0', 'GMT - 14': 'Etc/GMT-14', 'GMT - 13': 'Etc/GMT-13', 'GMT - 12': 'Etc/GMT-12', 'GMT - 11': 'Etc/GMT-11', 'GMT - 10': 'Etc/GMT-10', 'GMT - 9': 'Etc/GMT-9', 'GMT - 8': 'Etc/GMT-8', 'GMT - 7': 'Etc/GMT-7', 'GMT - 6': 'Etc/GMT-6', 'GMT - 5': 'Etc/GMT-5', 'GMT - 4': 'Etc/GMT-4', 'GMT - 3': 'Etc/GMT-3', 'GMT - 2': 'Etc/GMT-2', 'GMT - 1': 'Etc/GMT-1', 'GMT + 1': 'Etc/GMT+1', 'GMT + 2': 'Etc/GMT+2', 'GMT + 3': 'Etc/GMT+3', 'GMT + 4': 'Etc/GMT+4', 'GMT + 5': 'Etc/GMT+5', 'GMT + 6': 'Etc/GMT+6', 'GMT + 7': 'Etc/GMT+7', 'GMT + 8': 'Etc/GMT+8', 'GMT + 9': 'Etc/GMT+9', 'GMT + 10': 'Etc/GMT+10', 'GMT + 11': 'Etc/GMT+11', 'GMT + 12': 'Etc/GMT+12'}

# set supportive dictionary for reminders
time_notification = {'0': '00:00', '15': '00:15', '30': '00:30', '1': '01:00', '2': '02:00', '6': '06:00', '12': '12:00', '24': '24:00'}

# start message. Check if there is a timezone for user
@bot.message_handler(commands=['start'])
def start(message):
    if str(message.chat.id) not in bd.show_users():
        markup = tb.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        markup.row(tb.types.KeyboardButton('Send location', request_location=True))
        btns = []
        for k, v in timezones.items():
            btn = tb.types.KeyboardButton(v)
            btns += [btn]
        markup.add(*btns)
        bot.send_message(message.chat.id, text='Seems like you are a new user\nPlease, choose your time zone or send your approximate location\nI need it to determine your time zone, and then we can start'.format(message.from_user), reply_markup = markup)


    else:
        markup = tb.types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard=True)
        btn1 = tb.types.InlineKeyboardButton("Create new reminder")
        btn2 = tb.types.InlineKeyboardButton("Show my reminders")
        btn3 = tb.types.InlineKeyboardButton("Delete reminder")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Choose action".format(message.from_user), reply_markup = markup)


# create new timezone for user
@bot.message_handler(content_types=['location'])
def location (message):
    try:
        if message.location is not None:
            query_params = {"LATITUDE": message.location.latitude, "LONGITUDE": message.location.longitude, 'API_key': API_KEY}
            response = requests.get("https://htmlweb.ru/json/geo/timezone/", params=query_params)
            tz = zoneinfo.ZoneInfo(response.json()['name'])
        bd.create_time_zone(message.chat.id, tz)
        bot.send_message(text='Thank you! Now type in /start', chat_id=message.chat.id)
    except:
        bot.send_message(text='Sorry!\nSomething went wrong, please, try again', chat_id=message.chat.id)


# request for changing timezone for user
@bot.message_handler(commands=['change'])
def change_tz(message):
    markup = tb.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    markup.row(tb.types.KeyboardButton('Send location', request_location=True))
    btns = []
    for k, v in timezones.items():
        btn = tb.types.KeyboardButton(v)
        btns += [btn]
    markup.add(*btns)
    bot.send_message(message.chat.id, text='Please, choose your time zone or send your location'.format(message.from_user), reply_markup = markup)


# create or change timezone in case user didn't send location but choose timezone
@bot.message_handler(func = lambda message: message.text.startswith('Etc'))
def location(message):
    tz = zoneinfo.ZoneInfo(message.text)

    bd.create_time_zone(message.chat.id, tz)
    bot.send_message(chat_id=message.chat.id, text='Thank you! Now type in /start')

# create new dictionary for collecting information about new reminder
dic = {}

# creating new reminder. firstly check if there is a timezone for user
@bot.message_handler(func = lambda message: message.text == 'Create new reminder')
@bot.message_handler(commands=['new'])
def new(message):
    if str(message.chat.id) not in bd.show_users():
        markup = tb.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        markup.row(tb.types.KeyboardButton('Send location', request_location=True))
        btns = []
        for k, v in timezones.items():
            btn = tb.types.KeyboardButton(v)
            btns += [btn]
        markup.add(*btns)
        bot.send_message(message.chat.id, text='Seems like you are a new user\nPlease, choose your time zone or send your approximate location\nI need it to determine your time zone, and then we can start'.format(message.from_user), reply_markup = markup)
    else:
        msg = bot.reply_to(message, 'Type in text:')
        bot.register_next_step_handler(msg, get_text)

def get_text(message):
    try:
        user_id = message.chat.id
        dic['user_id'] = user_id
        text = message.text
        dic['text'] = text
        msg = bot.reply_to(message, 'Type in date in format YYYY-MM-DD:')
        bot.register_next_step_handler(msg, get_date)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def get_date(message):
    try:
        date = message.text
        try:
            # t = datetime(*[int(i) for i in date.split('-')])

            dic['date'] = date
            msg = bot.reply_to(message, 'Type in time in format HH:MM :')
            bot.register_next_step_handler(msg, get_time)
        except:
            msg = bot.reply_to(message, 'Wrong format, try again\n\nType in date in format YYYY-MM-DD:')
            bot.register_next_step_handler(msg, get_date)

    except Exception as e:
        bot.reply_to(message, 'oooops')    

def get_time(message):
    try:
        tim = message.text
        try:
            # m = time(*(int(i) for i in tim.split(':')))

            dic['time'] = tim
            msg = bot.reply_to(message, 'Type in priority status (from 1 to 3, where 1 - highest):')
            bot.register_next_step_handler(msg, get_priority)
        except:
            msg = bot.reply_to(message, 'Wrong format, try again\n\nType in time in format HH:MM :')
            bot.register_next_step_handler(msg, get_time)
    except Exception as e:
        bot.reply_to(message, 'oooops')  

def get_priority(message):
    try:
        priority = message.text
        if priority in ('1', '2', '3'):
            priority = int(priority)
            dic['priority'] = priority
            msg = bot.reply_to(message, "Type in notification before: 15 min/30 min/1 h/2 h/6 h/12 h/1 day\nType in numbers only, if you need a few notification, specify them separated by commas.\nIf you don't need advance notice, type in 0:")
            bot.register_next_step_handler(msg, get_notification)
        else:
            msg = bot.reply_to(message, 'Wrong format, try again\n\nType in priority status (from 1 to 3, where 1 - highest):')
            bot.register_next_step_handler(msg, get_priority)
    except Exception as e:
        bot.reply_to(message, 'oooops')  

def get_notification(message):
    try:
        notification = message.text
        try:
            notification = [time_notification[i.strip()] for i in notification.split(',')]
            dic['notification'] = notification
            if '00:00' not in dic['notification']:
                dic['notification'].append('00:00')
        except:
            msg = bot.reply_to(message, "Wrong format, try again\n\nType in notification before: 15 min/30 min/1 h/2 h/6 h/12 h/1 day\nType in numbers only, if you need a few notification, specify them separated by commas.\nIf you don't need advance notice, type in 0:")
            bot.register_next_step_handler(msg, get_notification)
    except Exception as e:
        bot.reply_to(message, 'oooops')   



    tz = zoneinfo.ZoneInfo(bd.get_tz(message.chat.id))
    date = [int(i) for i in dic['date'].split('-') + dic['time'].split(':')]
    date_local = datetime(*date, tzinfo=tz)
    date_utc = date_local.astimezone(timezone.utc)

    bd.set_new_reminder(dic['user_id'], dic['text'], date_utc, dic['priority'])
    bd.add_notifications(dic['text'], date_utc, notification, dic['user_id'])
    bot.send_message(message.chat.id, 'New reminder was created')



# show reminders
@bot.message_handler(commands=['show'])
@bot.message_handler(func = lambda message: message.text == 'Show my reminders')
def show(message):
    if str(message.chat.id) not in bd.show_users():
        markup = tb.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        markup.row(tb.types.KeyboardButton('Send location', request_location=True))
        btns = []
        for k, v in timezones.items():
            btn = tb.types.KeyboardButton(v)
            btns += [btn]
        markup.add(*btns)
        bot.send_message(message.chat.id, text='Seems like you are a new user\nPlease, choose your time zone or send your approximate location\nI need it to determine your time zone, and then we can start'.format(message.from_user), reply_markup = markup)
    else:

        markup1 = tb.types.InlineKeyboardMarkup(row_width=1)
        btn1 = tb.types.InlineKeyboardButton('Show previous reminders', callback_data='previous')
        btn2 = tb.types.InlineKeyboardButton("Show today's reminders", callback_data='today')
        btn3 = tb.types.InlineKeyboardButton('Show reminders for week', callback_data='week')
        btn4 = tb.types.InlineKeyboardButton('Show reminders for month', callback_data='month')
        btn5 = tb.types.InlineKeyboardButton('Show all reminders', callback_data='all')
        markup1.add(btn1, btn2, btn3, btn4, btn5)

        bot.send_message(chat_id=message.chat.id, reply_markup=markup1, text='Choose period')


# handling  all requests from buttons
@bot.callback_query_handler(func = lambda call: True)
def actions(call):

    bot.answer_callback_query(callback_query_id=call.id)

    unix = call.message.date
    tz = zoneinfo.ZoneInfo(bd.get_tz(call.message.chat.id))
    local_date = datetime.fromtimestamp(unix, tz)
    date_utc = local_date.astimezone(timezone.utc)
    time = date_utc.time()
    date = date_utc.date()

    # show reminders according to time frame
    if call.data == 'today':
        ans = bd.show_reminders(call.message.chat.id, time=time, period='today', date=date)
        bot.edit_message_text(text=ans, chat_id=call.message.chat.id, message_id=call.message.message_id)


    elif call.data == 'previous':
        ans = bd.show_reminders(call.message.chat.id, time=date_utc, period='previous')
        bot.edit_message_text(text=ans, chat_id=call.message.chat.id, message_id=call.message.message_id)



    elif call.data == 'week':
        ans = bd.show_reminders(call.message.chat.id, time=time, period='week', date=date)
        bot.edit_message_text(text=ans, chat_id=call.message.chat.id, message_id=call.message.message_id)


    elif call.data == 'month':
        ans = bd.show_reminders(call.message.chat.id, time = time, period='month', date=date)
        bot.edit_message_text(text=ans, chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'all':

        ans = bd.show_reminders(call.message.chat.id, time=time, period='all')
        bot.edit_message_text(text=ans, chat_id=call.message.chat.id, message_id=call.message.message_id)

    # handling  answer to question for delay important messages
    elif call.data.startswith('&'):
        ind = call.data[1]
        reminder_id = call.data[2:]
        if ind == '0':
            bot.edit_message_text(text='Cool! This is the right answer', chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.edit_message_text(text='Nope, reminder will be shown again in 15 min', chat_id=call.message.chat.id, message_id=call.message.message_id)
            bd.add_additional_notification(reminder_id, date_utc, '00:15')

    # delete certain reminder
    elif call.data.isdigit():
        bd.delete_reminder(call.message.chat.id, call.data)
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text="This reminder was deleted")
    
    # delay reminder by 15 min
    elif call.data.startswith('delay'):
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text='Ok, notification delayed by 15 min')

        bd.add_additional_notification(call.data[5:], date_utc, '00:15')

    # create question for delay important reminder
    elif call.data.startswith('solve'):
        reminder_id = call.data[5:]
        question = random.choice(list(exercise.keys()))
        answers = (exercise[question])

        a = answers.copy()
        random.shuffle(a)
        markup_ex = tb.types.InlineKeyboardMarkup(row_width=2)
        for answer in a:
            ret = str(answers.index(answer))
            btn = tb.types.InlineKeyboardButton(answer, callback_data=f'&{ret}{reminder_id}')
            markup_ex.add(btn)
        bot.edit_message_text(message_id=call.message.message_id, reply_markup=markup_ex, chat_id=call.message.chat.id, text=f'{question}')

    

# create menu for deleting reminders
@bot.message_handler(func = lambda message: message.text == 'Delete reminder')
@bot.message_handler(commands=['delete'])
def delete_menu(message):
    if str(message.chat.id) not in bd.show_users():
        markup = tb.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        markup.row(tb.types.KeyboardButton('Send location', request_location=True))
        btns = []
        for k, v in timezones.items():
            btn = tb.types.KeyboardButton(v)
            btns += [btn]
        markup.add(*btns)
        bot.send_message(message.chat.id, text='Seems like you are a new user\nPlease, choose your time zone or send your approximate location\nI need it to determine your time zone, and then we can start'.format(message.from_user), reply_markup = markup)
    else:

        reminders = bd.show_delete_reminder(message.chat.id)
        markup_del = tb.types.InlineKeyboardMarkup(row_width=1)
        if type(reminders) ==  str:
            bot.send_message(chat_id=message.chat.id, text=reminders)
        else:
            for reminder, rem_id in reminders.items():
                btn = tb.types.InlineKeyboardButton(reminder, callback_data=rem_id)
                markup_del.add(btn)

            bot.send_message(chat_id=message.chat.id, reply_markup=markup_del, text='Choose reminder to delete')



bot.infinity_polling()
