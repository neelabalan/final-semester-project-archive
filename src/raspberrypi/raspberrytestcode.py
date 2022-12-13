import sched, time
import datetime
import sys
import paho.mqtt.client as mqtt
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import threading

mqtt_broker = "192.168.0.100"
mqtt_port = 1883
TOKEN = ""

updater = Updater(TOKEN)
# bot         = telegram.Bot(TOKEN)

# s = sched.scheduler(time.time, time.sleep)


# TODO important
# updating the voltage, current rpm and duration values with zeroes precided

# TODO default values to be changed later
# default values of motor_params

motor_params = ["999", "999", "999", "99.99", "99.99", "99.99", "9999", "99H 99M 99S"]


def main():

    # bot = telegram.Bot(TOKEN)
    dp = updater.dispatcher
    logdata(t_stop)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("report", reportcsv))
    dp.add_handler(CommandHandler("test", test))
    updater.start_polling()
    updater.idle()


t_stop = threading.Event()


def logdata(t_stop):
    file = open("report.csv", "a+")
    running = datetime.datetime.now()
    minute = str(running.minute)
    file.write(minute)
    file.write("\n")
    file.close()

    if not t_stop.is_set():
        threading.Timer(30, logdata, [t_stop]).start()


#    s.enter(60, 1, logdata, (sc,))

# s.enter(60, 1, logdata, (s,))
# s.run()

# |-----------------------------------------------------------------|
# |                     TELEGRAM PROGRAM STARTS                     |
# |-----------------------------------------------------------------|


def start(bot, update):
    start_text = (
        "Welcome to Motor Parametrs Monitoring \n"
        "     Internet of Things Bot             "
    )
    update.message.reply_text(start_text)


def reportcsv(bot, update):
    bot.send_document(chat_id=update.message.chat_id, document=open("report.csv", "rb"))


def test(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="`hello world`", parse_mode="MARKDOWN"
    )


# |-----------------------------------------------------------------|
# |                     TELEGRAM PROGRAM ENDS                       |
# |-----------------------------------------------------------------|


if __name__ == "__main__":
    main()
