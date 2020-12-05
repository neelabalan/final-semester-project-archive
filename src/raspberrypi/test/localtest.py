import datetime
import time
import sys 
import paho.mqtt.client as mqtt
import telegram
from telegram.ext import Updater,       \
                         CommandHandler,\
                         MessageHandler,\
                         Filters

# some default value for mqtt broker

mqtt_broker        = "192.168.43.111"
mqtt_port          = 1883
TOKEN              = ''
mqtt_flag          = 1
duration_flag      = 0
voltage_error_flag = 0
initialvalue       = "start"
sminute            = 0
shour              = 0
rminute            = 0
rhour              = 0
alertminute        = "alrt"
alert_flag         = 0
storechatid        = []
time_minute        = 0
# TODO important
# updating the voltage, current rpm and duration values with zeroes precided

# TODO default values to be changed later
# default values of motor_params

motor_params=[                          \
              "999", "999", "999",      \
              "99.99", "99.99", "99.99" \
             ]

duration = ["99H:99M", "fromtime", "stillrun"]

updater = Updater(TOKEN)

j = updater.job_queue 

def main():
    global mqtt_flag
    dp      = updater.dispatcher
    client  = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message


    try:
        client.connect(mqtt_broker, mqtt_port)
    except:
        print("not connected to mqtt")
        client.loop_stop()
    
    dp.add_handler(CommandHandler("start"   , start       ))
    dp.add_handler(CommandHandler("motorval", motorval    ))
    dp.add_handler(CommandHandler("setip"   , setip       )) 
    dp.add_handler(CommandHandler("help"    , help        ))
    dp.add_handler(CommandHandler("test"    , test        ))
    dp.add_handler(CommandHandler("settime" , set_duration))    
    dp.add_handler(CommandHandler("report"  , reportcsv   ))
    updater.start_polling()
#    updater.idle()
 


# |-----------------------------------------------------------------|
# |                     NORMAL ROUTINE STARTS                       |
# |-----------------------------------------------------------------|


def reportfault():
    global voltage_error_flag 
    global alert_flag

    bot     = telegram.Bot(TOKEN)
    if (int(motor_params[0]) > 220 and \
        int(motor_params[1]) > 220 and \
        int(motor_params[2]) > 200     \
       ):
        print("")
    else:
        job_minute=j.run_repeating(callback_voltage, interval=60, first=0)

    if time_minute==alertminute:
        job_minute=j.run_repeating(callback_duration, interval=60, first=0)

def logscv():
    d = datetime.datetime.now()
    file = open('report.csv', 'a+')
    text = d + ","  + motor_params[0] +  "," \
                    + motor_params[1] +  "," \
                    + motor_params[2] +  "," \
                    + motor_params[3] +  "," \
                    + motor_params[4] +  "," \
                    + motor_params[5]    
         
    file.write(text)
    # write program here


# |-----------------------------------------------------------------|
# |                     NORMAL ROUTINE ENDS                         |
# |-----------------------------------------------------------------|




# |-----------------------------------------------------------------|
# |                     MQTT PROGRAM STARTS                         |
# |-----------------------------------------------------------------|


def on_connect(client, userdata, flags, rc):
    global mqtt_flag
    if rc==0:
        print("-- CONNECTION SUCCESSFUL --")
        client.subscribe("esp1/currenta")
        client.subscribe("esp1/currentb")
        client.subscribe("esp1/currentc")
        client.subscribe("esp1/voltagea")
        client.subscribe("esp1/voltageb")
        client.subscribe("esp1/voltagec") 
    else:
        print("-- MQTT CONNECTION FAILED --")
    mqtt_flag=rc


def setmotor_params(topic, message):
    global motor_params 
    if(topic == "esp1/voltagea"):
        motor_params[0] = message
    if(topic == "esp1/voltageb"):
        motor_params[1] = message
    if(topic == "esp1/voltagec"):
        motor_params[2] = message
    if(topic == "esp1/currenta"):
        motor_params[3] = message
    if(topic == "esp1/currentb"):
        motor_params[4] = message
    if(topic == "esp1/currentc"):
        motor_params[5] = message
    print(motor_params)
    finduration(motor_params[3], motor_params[4], motor_params[5])


# need to fine tune

def findduration(currenta, currentb, currentc):
    global initialvalue, time_minute
    global sminute, shour, rminute, rhour 
    global duration

    intcurrenta=float(currenta)
    intcurrentb=float(currentb)
    intcurrentc=float(currentc)
   
    if(                                  \
            initialvalue == "start"  and \
            intcurrenta>0.1          and \
            intcurrentb>0.1          and \
            intcurrentc>0.1              \
      ):
        starting = datetime.datetime.now()
        sminute  = starting.minute()
        shour    = starting.hour()
        duration[1]=str(shour) + ":" + str(sminute)

    
    if(intcurrenta<0.1 and intcurrentb<0.1 and intcurrentc<0.1):
        initialvalue = "start"
        return "MOTOR OFF"

    if(a>0.1):
        running = datetime.datetime.now()
        rminute = running.minute
        rhour   = running.hour
        duration[2]=str(rhour) + ":" + str(rminute)

    time_minute   = rminute - sminute
    time_hour     = rhour - shour
    time_duration = str(time_hour) + ":" + str(time_minute)
    duration[0]   = time_duration
    return time_duration
    
def on_disconnect(client, userdata, rc):
    print("-- DISCONNECTED FROM THE BROKER --")

def on_message(client, userdata, message):
    setmotor_params(message.topic, message.payload.decode("utf-8"))
    print("-- MESSAGE RECEIVED --" + message.payload.decode()) 
    print("-- TOPIC            --" + message.topic) 


# |-----------------------------------------------------------------|
# |                     MQTT PROGRAM ENDS                           |
# |-----------------------------------------------------------------|





# |-----------------------------------------------------------------|
# |                     TELEGRAM PROGRAM STARTS                     |
# |-----------------------------------------------------------------|


def callback_voltage(bot, job):
    for num in storechatid:
        voltage_etext= "*ERROR - Possible wire loose connection in motor terminal*"
        bot.send_message(chat_id=num, text=voltage_etext, parse_mode='MARKDOWN')


def callback_duration(bot, job):
    for num in sotrechatid:
        duration_etext="*ALERT - The set operation time of motor has exceded*"
        bot.send_message(chat_id=num, text=duration_etext, parse_mode='MARKDOWN')

def reportcsv(bot, update):
    bot.send_document(chat_id=update.message.chat_id, document=open('report.csv', 'rb'))

def start(bot, update):
    start_text = "Welcome to Motor Parameters Monitoring \n" \
                 "        Internet of Things Bot         \n" \
                 "use the _/help_ command for assistance   " \
                 " Your ID is now added in the database    "
    update.message.reply_text(start_text)
    storechatid.append(update.message.chat_id) 

def setip(bot, update):
    # update.message.reply_text("Enter the MQTT Broker IP address")
    ip_addr=update.message.text 
    ip_addr=ip_addr[7:] 
    
    try:
        global mqtt_broker
        socket.inet_aton(ip_addr)
        update.message.reply_text("IP Address set successfully")
        mqtt_broker=ip_addr
    except:
        update.message.reply_text("Not a valid IP Address")

def set_duration(bot, update):
    global alertminute
    text="ERROR - string input not permitted"
    duration=update.message.text
    alertminute=duration[9:]
    if(not alertminute.isdigit()):
        bot.send_message(chat_id=update.message.chat_id, text=text)

def motorval(bot, update):
    global mqtt_flag
     
    error_text=("*ERROR! DEVICE NOT CONNECTED*       \n   "
                "*TO MQTT BROKER*                    \n \n"
                "`by setting the IP address of      `\n   "
                "`MQTT broker using /setip command  `\n   "
                "`for example - 192.168.0.0         `     ")
    
    start_text = "*MOTOR#1*"
    voltage_text = ("`VOLTAGE - R {0} V`\n"        
                    "`VOLTAGE - Y {1} V`\n"         
                    "`VOLTAGE - B {2} V`  ").format(motor_params[0], motor_params[1], motor_params[2])
   
    bot.send_message(chat_id=update.message.chat_id, text="hello") 
    current_text = ("`CURRENT - R {0} A`\n"     
                    "`CURRENT - Y {1} A`\n"           
                    "`CURRENT - B {2} A`  ").format(motor_params[3], motor_params[4], motor_params[5])
                
    duration_text=("`TOTAL TIME DURATION - {0}`\n"   
                   "`FROM - {1}`               \n"                  
                   "`TO   - {2}`").format(duration[0], duration[1], duration[2])
    if(mqtt_flag==0):
        bot.send_message(chat_id=update.message.chat_id, text=start_text, parse_mode='MARKDOWN') 
    
    else:
        bot.send_message(chat_id=update.message.chat_id, text=error_text, parse_mode='MARKDOWN')

def help(bot, update):
    help_text="*List of commands available*                 \n\n"   \
              "*/setip*                                       \n"   \
              "For setting the IP address of the MQTT broker\n\n"   \
              "*/motorval*                                    \n"   \
              "For viewing all the motor parameters like      \n"   \
              "current and voltage etc,. "                          \

    bot.send_message(                                   \
                        chat_id=update.message.chat_id, \
                        text=help_text,                 \
                        parse_mode='MARKDOWN'           \
                    )
def test(bot, update):
    bot.send_message(chat_id=update.message.chat_id,\
            text="`hello world`",                   \
            parse_mode='MARKDOWN')

# |-----------------------------------------------------------------|
# |                     TELEGRAM PROGRAM ENDS                       |
# |-----------------------------------------------------------------|


if __name__ == '__main__':
    main()

