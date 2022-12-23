import time
import telebot
import bazdan as bd
from datetime import datetime, timezone
import zoneinfo
from config import TELEGRAM_TOKEN


# set supportive dictionary for questions
exercise = {'Find the area of a square with side 4': ['16', '8', '12', '20'], 'Find 2th root of 81': ['9', '8', '7', '11'], "What's the capital of Australia?": ['Canberra', 'Sydney', 'Vienna', 'Melbourne'], "What's the capital of Germany?": ['Berlin', 'Munich', 'Cologne', 'Moscow'], "What's the capital of Spain?": ['Madrid', 'Milan', 'Barcelona', 'Valencia'], "What's the capital of Canada?": ['Ottawa', 'Toronto', 'Quebec City', 'Halifax'], "Find factorial 3 (3!)": ['6', '9', '3', '1']}


# Create bot connection
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# infinity scanning for new notification
# processing each kind of notifications
while True:
    result = bd.show_info()
    real_time = str(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    for chat_id, text, time_not, reminder_date, priority, reminder_id, before_time in result:
        time_not = str(datetime.fromisoformat(time_not).strftime("%Y-%m-%d %H:%M"))

        if time_not == real_time:
            tz = zoneinfo.ZoneInfo(bd.get_tz(chat_id))
            reminder_date = datetime.fromisoformat(reminder_date).astimezone(tz).strftime("%Y-%m-%d  %H:%M")

            if priority == 1 and before_time == 0:
                markup = telebot.types.InlineKeyboardMarkup(row_width=1)
                btn1 = telebot.types.InlineKeyboardButton('Delay reminder', callback_data=f'delay{reminder_id}')
                btn2 = telebot.types.InlineKeyboardButton("Solve an exercise", callback_data=f'solve{reminder_id}')
                markup.add(btn1, btn2)
                bot.send_message(chat_id=chat_id, text=f"Look! You have an important reminder!\n\n {reminder_date}\n{text}")
                bot.send_message(chat_id=chat_id, reply_markup=markup, text=f"What we gonna do with it?")

            elif before_time == 1:
                res_st = f'Hey! This is your pre-notification\n\n{reminder_date}\n{text}'
                bot.send_message(chat_id, res_st)

            else:
                res_st = f"Look! You have reminder!\n\n {reminder_date}\n{text}"
                bot.send_message(chat_id, res_st)



    time.sleep(60)
