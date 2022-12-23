Reminder Bot
##
This is a Telegram bot for creating and managing reminders. With this bot, you can:

- Create new reminders
- View all of your reminders (or choose a different time frame for displaying reminders)
- Delete reminders (select the 'delete' button from the menu, then choose which reminders you want to delete)

When you set a new reminder, you can specify the text of the reminder, the date and time, the priority, and the time when you want to receive a preliminary notification (e.g. 15 minutes before the main time).

Each reminder has a priority status, which you can set while creating it. If the priority status is set to 1, you will receive a question or task (such as solving a math problem) with the notification. If you answer correctly, the reminder will be marked as done. If your answer is incorrect, the bot will show you the reminder again after 15 minutes with a different question (and so on until you answer correctly).

To properly handle timezones, you will need to provide your location or choose a timezone from a list provided by the bot when you first start using it.

This bot is built using Python, the telebot library, SQLITE database, multiprocessing and APi "https://htmlweb.ru/geo/api_timezone.php" for definition timezone from location.

##
   How to use

To start using the Reminder Bot, find @Alex_reminder_for_you_bot in Telegram and add it to your accaunt (this is my version of this bot, but I don't run it constantly)

- Type in /start
- After that bot will ask you for your timezone (You can choose from the given options or (more preferable) send yor location)

The following commands are available (you can find them in bottom menu, or in left menu):
- Create new reminder (/new)
Here you just should follow instructions from the bot. In separate messages type in text of reminder, date in format YYYY-MM-DD, time in format HH:MM, priority status, time for preliminary notification
 
 - Show my reminders (/show)
 Bot will suggest you time frames. All previous, Today's reminders, For this week, For this month, All reminders. Choose one option from suggested.
 Bot will show you your reminders. If you see symbol "!" before date - it means priority status is 1
 
 - Delete reminder (/delete)
 Bot will show you all your reminders. Choose one and click on it. Bot will delete it. It doesn't exist anymore, so you can't see it anywhere
 
 - Change time zone / location (/change)
 Here you can change your timezone. The actions are the same as in section "Type in /start" (if you are a new user, of course)
 
 Notifications
 
 When it's time, bot will send you a message with notification and reminder's text.
 If priority status is 1, bot will ask you what you want to do with it. Choose one option: Delay (notification will be delyed by 15 min) or Solve.
 If you choose Solve, bot will send you a question and answer options. Choose one option. If you answer correctly, the reminder will be marked as done. If your answer is incorrect, the bot will show you the reminder again after 15 minutes with a different question (and so on until you answer correctly).
 
 ##
 
    Installation
To install and run the Reminder Bot from your computer, follow these steps:

- Clone the repository: git clone https://github.com/PAMartynova/telegram_reminder.git

- Navigate to the project directory: cd telegram_reminder

- Install the required dependencies: pip install -r requirements.txt

- Create a config.py file and add your Telegram token and Api key for 'https://htmlweb.ru/geo/api_timezone.php'
Use this template:
   TELEGRAM_TOKEN = "token"
   API_KEY = "api-key"
   
- Run the bot script: python reminder.py

Note: You will need to have Python and pip installed on your computer to run the bot. You will also need to obtain a Telegram API tokenm and API key from "https://htmlweb.ru/geo/api_timezone.php" and add it to the config.py file.
##

Feel free to use this code for any purpose
You can contact me for any questions via email pamartynova@gmail.com




