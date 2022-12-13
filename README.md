# Final semester project archive

This is a proof of concept for using the MQTT protocol for data acquisition in industrial drives. We ([Neelabalan](twitter.com/neelabalan), [Navin Kumar](https://github.com/Naveen-noob98) and [Hariharaa Sudan](https://twitter.com/hariharaa_sudan)) started this project at start of 2019 and worked on it for 2 months. We wanted the project to be out in the internet with the schematics and the source code. The documentation here does not have all the information like BOM but has enough information to get the circuit up and running if you are ready to spend some time and understand what is being done here.



# Table of Contents

* [Abstract](https://github.com/neelabalan/final-semester-project-archive#abstract)

* [Introduction](https://github.com/neelabalan/final-semester-project-archive#introduction)

    * [MQTT protocol](https://github.com/neelabalan/final-semester-project-archive#mqtt-protocol)
        * [Why MQTT? Why not HTTPS?](https://github.com/neelabalan/final-semester-project-archive#why-mqtt-why-not-https)
    * [Using Telegram Chat Bot](https://github.com/neelabalan/final-semester-project-archive#using-telegram-chat-bot)
    * [NodeMCU](https://github.com/neelabalan/final-semester-project-archive#nodemcu)
    * [Raspberry Pi Zero](https://github.com/neelabalan/final-semester-project-archive#raspberry-pi-zero)

    * [Block diagram of the overall flow](https://github.com/neelabalan/final-semester-project-archive#block-diagram-of-the-overall-flow)

* [Hardware Development](https://github.com/neelabalan/final-semester-project-archive#hardware-development)

    * [Circuit Block diagram](https://github.com/neelabalan/final-semester-project-archive#circuit-block-diagram)
    * [Power Supply](https://github.com/neelabalan/final-semester-project-archive#power-supply)
        * [Power supply for the signal conditioning circuit and multiplexer circuit](https://github.com/neelabalan/final-semester-project-archive#power-supply-for-the-signal-conditioning-circuit-and-multiplexer-circuit)
        * [Power supply for MCU](https://github.com/neelabalan/final-semester-project-archive#power-supply-for-mcu)
    * [Using CT and PT](https://github.com/neelabalan/final-semester-project-archive#using-ct-and-pt)
        * [Position of CT and PT](https://github.com/neelabalan/final-semester-project-archive#position-of-ct-and-pt)
    * [Position of Hall effect sensor for speed measurement](https://github.com/neelabalan/final-semester-project-archive#position-of-hall-effect-sensor-for-speed-measurement)
    * [Signal Conditioning Unit](https://github.com/neelabalan/final-semester-project-archive#signal-conditioning-unit)
    * [Multiplexer](https://github.com/neelabalan/final-semester-project-archive#multiplexer)

* [Software development](https://github.com/neelabalan/final-semester-project-archive#software-development)

    * [ESP8266](https://github.com/neelabalan/final-semester-project-archive#esp8266)
    * [RaspberryPi](https://github.com/neelabalan/final-semester-project-archive#raspberrpipi)
    * [Telegram bot commands and responses](https://github.com/neelabalan/final-semester-project-archive#telegram-bot-commands-and-responses)

* [Final outcome](https://github.com/neelabalan/final-semester-project-archive#final-outcome)

    * [Screenshots of terminal](https://github.com/neelabalan/final-semester-project-archive#screenshots-of-terminal)
    * [Telegram Chat Bot screenshots](https://github.com/neelabalan/final-semester-project-archive#telegram-chat-bot-screenshots)
    * [Waveform screenshot](https://github.com/neelabalan/final-semester-project-archive#waveform-screenshot)

* [Assembled Ciruit in General Purpose Board](https://github.com/neelabalan/final-semester-project-archive#assembled-ciruit-in-general-purpose-board)

* [References](https://github.com/neelabalan/final-semester-project-archive#references)



## Wireless monitoring of Industrial drives using MQTT protocol



### Abstract

Electrical motors and drives consumes about 45% of the power generation. However, if the electrical machines are not maintained properly it will lead to discontinued production which may affect the productivity and revenue. Continuous monitoring of critical parameters of various machines and drives is crucial for an industry which operates large number of machines continuously. Before the advent of Internet of Things (IoT) technology, monitoring of the machine parameters were carried out using Supervisory Control and Data Acquisition (SCADA). [Compared to SCADA](https://blog.se.com/industrial-software/2019/04/10/4-key-differences-between-scada-and-industrial-iot/) , The collected data using IoT can be stored in cloud and integrated with all cross platform applications which benefits the end user by cutting down huge investment costs. 

In the proposed work, current, voltage, speed and number of working hours of the 3 phase AC motor in the laboratory are monitored. These parameters are sensed by the current transformer, potential transformer and Hall effect sensor respectively.  The data is collected and processed using microcontroller and transferred to a remote server wirelessly using **Message Queuing Telemetry Transport (MQTT)** protocol. Any deviation from the rated operating conditions is reported to the concerned person through chat bot in telegram mobile app.



### Introduction

#### MQTT protocol

MQTT stands for Message Queuing Telemetry Transport. It is a publish/subscribe, extremely simple and lightweight messaging protocol, designed for constrained devices and low-bandwidth, high-latency or unreliable networks. The design principles are to minimise network bandwidth and device resource requirements whilst also attempting to ensure reliability and some degree of assurance of delivery. These principles also turn out to make the protocol ideal of the emerging “machine-to-machine” (M2M) or “Internet of Things” world of connected devices, and for mobile applications where bandwidth and battery power are at a premium



##### Why MQTT? Why not HTTPS?

| **FEATURES**       | **MQTT**                                | **HTTP**                          |
| ------------------ | --------------------------------------- | --------------------------------- |
| Design Methodology | The protocol is data centric.           | The protocol is document centric. |
| Complexity         | Simple                                  | More complex                      |
| Message size       | Small, it is binary with 2-byte header. | Large, it is in ASCII format.     |
| Service levels     | 3                                       | 1                                 |

[Performance comparison](https://cloud.google.com/blog/products/iot-devices/http-vs-mqtt-a-tale-of-two-iot-protocols) between the two protocols has demonstrated that MQTT shows less latency, less bandwidth usage and less energy consumption when compared to REST HTTP, all critical factors in resource deprived IoT infrastructures 



#### Using Telegram Chat Bot

The current, voltage and speed can be requested from the telegram bot using the commands. The data acquired from the very start can also be requested from the bot in excel format. The software development time and cost here was very less compared to developing a full blown UI and hosting it on AWS. The downside to this decision is that the voltage and current params cannot be viewed in realtime.

#### NodeMCU

NodeMCU is a Wi-Fi SOC (system on a chip) based on ESP8266 -12E Wi-Fi module. It is a highly integrated chip designed to provide full internet connectivity in a small package. It can be programmed directly through USB port using various languages. The reason why we chose NodeMCU was because it was cheap and was easy to develop in VSCode using [PlatformIO](https://platformio.org/).

![nodemcu](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/nodemcu.png)

#### Raspberry Pi Zero

Raspberry pi zero wireless is a credit card sized computer that on runs on ARMV6Z (32 – bit) 1GHz processor. The SoC has an inbuilt 802.11b/g/n single band 2.4 GHz wireless, Bluetooth 4.1 BLE (Bluetooth Low Energy) hardware driver module. We hosted the telegram bot and the MQTT broker locally in the RaspberryPi. The RaspberryPi here can be entirely replaced with AWS or Heroku or similar cloud platform.

![raspberrypizero-image](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/raspberrypizero.png)

### Block diagram of the overall flow

![flow-diag](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/flow-diag.png)



### Hardware Development

#### Circuit Block diagram

![circuit-block-diagram](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/circuit-block-diagram.png)

#### Power Supply

There are three power supply connections involved in this project. One is for the signal conditioning circuit, multiplexer and opto-isolator (level shifting) combined. The second one is for the microcontroller board and the accompanying **ADS1115** board which works in the logic level of **3.3 V**. The third supply is a 3 phase AC supply for the motor which is **415 V (220 V ph-ph)**



##### Power supply for the signal conditioning circuit and multiplexer circuit

![ps1](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/ps1.png)

The power transformer of rating **415 V/15 V** with center tap gets a supply voltage of **230 V** and this supply can be drawn from the mains. The transformer steps down the voltage down to **+9** and **–9 V**. The **+9 V** and **–9 V** AC supply from the transformer secondary is provided to bridge rectifier **IC DB104**. The output of **DB104** is a DC voltage of **+ 5.34 V** and **– 5.34 V** considering the potential drop across the 4 diodes. The positive and negative output of the bridge rectifier IC is fed as input to the voltage regulator **ICs LM7805** (positive supply) and **LM7905** (negative supply). A rectifier output voltage of **+5 V** and **-5 V** are obtained at the output of **LM7805 IC** and **LM7905 IC** respectively.



##### Power supply for MCU

The NodeMCU board receives 5 V supply though micro USB cable from a mobile charge adapter. The 5 V is regulated to 3.3 V internally in the board using the **AM1117 IC**. 

The opto-isolator which is being used here as a level shifter which shifts the 3.3 V to 5 V. The opto-isolator gets both 5 V and 3.3 V supply from the **LM7805 IC** and NodeMCU board respectively. The level shifter is being used to select the pins in the multiplexer (CD451)



#### Using CT and PT

The potentiometer at the current transformer (CT) and potential transformers (PT) are adjusted in such a way that they provide an output voltage of 2 V when they reach their maximum voltage and current limits. These are **450 V** and **1.5 A** respectively. The **2 V** peak to peak AC signal will be received at the input of the signal conditioner circuit for the peak values of measurement. The AC voltage received at the input of the signal conditioner varies with voltage and current variation at the motor's supply side.

The potential transformer steps down **450 V** to **9 V**. The PT is connected in parallel with the circuit. The primary windings of the potential transformer are directly connected to the power circuit whose voltage is to be measured. The secondary terminals of the potential transformer are connected to the multiplexer channels. The current transformer AC1005 having a turns ratio of **1000:1** nominal is used to measure the voltage. A burden resistor of **100 ohms** is added so that an output of **100 mV per Amp ratio at 5 A**

The potentiometer connected in series with the CT is adjusted such that for a current of **1.5 V Amps** gives an output of **2 V** at the input of the signal conditioner circuit. 

With a time delay of 2 seconds between sampling of two different sensor's analog outputs. So a total of 12 seconds is required to convert the analog signal of all the sensors to digital and display that data in telegram. The multiplexer channel selects are switched in that fashion with inherent delay in the program.

The analog data from the sensors need to be converted to a digital form for the microcontroller to read it. An analog to digital conversion **IC ADS-1115** of **16-bit** resolution is being used here. This IC has high precision measurement and has a 860 samples/second speed at maximum. Of the four single ended input channels namely A0, A1, A2 and A3. Channel A1 is used in the continuous conversion mode. The inherent programmable gain amplifier is set at 2 times gain. The 2X gain corresponds to **+/- 2.048 V** measurement at A1 channel of the ADC. With this gain of two, a voltage resolution of **1 mV** for 1 bit is obtained.

$$Motor Voltage = { 450 * ADCcount  \over ADCupcount }\ (1)  \ where \ ADCupcount=32768\ for\ 16bit\ ADC$$

The ADC count in the above equation (1) refers to the digital value received for the corresponding analog value of the measured voltage.

$$Motor Current = {1.5* ADC Count \over ADCupcount}\ (2)\ where \ ADCupcount=32768\ for\ 16bit\ ADC$$


The ADC count in the above equation (2) refers to the digital value received for the corresponding analog value of the measured current



##### Position of CT and PT

![ct-pt](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/position_ct_pt.png)



#### Position of Hall effect sensor for speed measurement

![hallsensor](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/hallsensor.png)



#### Signal Conditioning Unit

![signal-conditioning-unit](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/signal-conditioning-unit.png)

Among many methods that are being used to monitor the current and voltage of a device, using a current and potential transformer is preferable because it is an easy and cost effective method. The current transformer is easy to install and susceptible to very less mechanical stress compared to Hall effect current sensor. The potential transformer is a better method to measure AC voltage compared to using potential divider and then using a precision rectifier to measure the voltage.

The signal conditioning circuit here is required to convert the AC signal that is being received from the current sensor and potential sensor to DC voltage levels. A precision rectifier circuit being used here to convert the peak to peak AC voltage to DC voltage and remove noise from the signal if any found. A typical bridge rectifier alone cannot do this because the 0.7 V drop across the four diodes would amount to loss of voltage measurement. Moreover, the bridge rectifier cannot filter the noise encountered at the input. 

The precision rectifier circuit uses the Op-Amp **IC LM324**. The **LM324 IC** has four Op-Amp built in. This makes the circuit very compact and easy to debug if any issues arises. Of the four Op-Amps present in the **LM324 IC** only three are being used here. The first two Op-Amps are used for precision rectification purpose and the last Op-Amp is used as a means to adjust the gain. The gain can be adjusted by the use of the **10 Kilo Ohm** potentiometer



#### Multiplexer

The **CD4051** is a CMOS single 8-channel analog   multiplexer/demultiplexer with logic level conversion. Analog input of **20V peak-peak** and can supplied. The multiplexer is used here to avoid building six separate precision rectification and amplifier circuit for 3 current transformer input and 3 potential transformer input. The single circuit can be used for conditioning the AC signal by switching the channels. The secondary of the three potential transformer and the secondary of the three current transformers are connected to the Multiplexer input. 

![multiplexer-circuit](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/multiplexer-cicuit.png)

| **Phase voltage and current** | **Channel selection** |
| ----------------------------- | --------------------- |
| R Phase Current               | Channel 0             |
| Y Phase Current               | Channel 1             |
| B Phase Current               | Channel 2             |
| R Phase Voltage               | Channel 3             |
| Y Phase Voltage               | Channel 4             |
| B Phase Voltage               | Channel 5             |

The input is AC and is unfiltered. The input to three channel selects namely A, B and C are provided from the NodeMCU GPIOs through the level shifter. Upon setting high and low levels in GPIOs the channels are selected in the multiplexer accordingly. The GPIOs D6, D7 and D8 are configured in the output mode and are toggled in accordance with the table to select a channel to which the sensors are connected.

![multiplexer](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/multiplexer.png)

The suitable current or voltage sensor’s input to the ADC can be selected from the MCU. The level shifter senses the input from the GPIO of NodeMCU and then outputs 5 V at the multiplexer channel select pins The **3.3 V to 5 V** level shifter is used to select the channels in the multiplexer. The output of the multiplexer is connected the **ADS1115 (ADC)** and the digital values is being read by the MCU using I2C from the defined address in the EEPROM.



### Software development

#### ESP8266

```cpp
#include <ESP8266WiFi.h>			// wifi library for ESP8266
#include <ESP8266WebServer.h>		// library for acting as web server
#include <Arduino.h>				
#include <Adafruit_ADS1015.cpp>		// driver for ADS1115
#include <Wire.h>					// library for I2C communication
#include <PubSubClient.cpp>			// Publish and subscribe client for MQTT

// for setting up the WiFi connection with the SSID and password in the Nodemcu microcontroller
void setup_wifi();	

//makes sure that the MQTT connection is re-established when there is some error that is encountered
void mqtt_reconnect();


// used here for selecting the multiplexer pin for getting in the input from the precision rectifier
void changeMux(int c, int b, int a);

// reset char buffer
void reset_buffer(char buff[]);

// convert the digital values received from the ADC to actual voltage and current values respectively
int   find_voltage(unsigned int);
float find_current(unsigned int);


//------------SNIPPET-------------------//
void setup(void)
{
    Serial.println("baud rate set to 9600");
   // pinMode(LEDpin, OUTPUT);

    Serial.begin(9600);

	 // ADS GAIN VALUES
	 // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
	 // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
	 // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
	 // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
	 // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
	 // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV
		
    ads.setGain(GAIN_TWO);
    ads.begin();

    /*
     CD4051 Multiplexer
     ---------------
     D6    ->   S0 (A)
     D7    ->   S1 (B)
     D8    ->   S2 (C)
    */


    //Deifne output pins for Mux
    pinMode(MUX_A, OUTPUT);
    pinMode(MUX_B, OUTPUT);     
    pinMode(MUX_C, OUTPUT);  
   
   
    // wifi setup
    setup_wifi();


    // setting up mqtt server
    client.setServer(mqtt_server, 1883);
    //client.setCallback(callback);
}



get_currenta();

// send the data stored in the `buffer` to the topic that the client has subscribed to, 
// which is currenta
client.publish("esp1/currenta", buffer);
reset_buffer(buffer);
// A delay of 200 milliseconds is being used here so that for before 
// getting the sensor data from the next pin there is a time period gap 
// to stabilize the input getting received
DELAY_200;

```



#### RaspberrpiPI

```python
import socket									// for socket programming
import datetime									// datetime library
import time
import sys 
import paho.mqtt.client as mqtt					// MQTT library
import telegram									// telegram messenger API wrapper
from telegram.ext import Updater,       \
                         CommandHandler,\
                         MessageHandler,\
                         Filters
            
            
# snippet

# API TOKEN of telegram bot
updater = Updater(TOKEN) 
bot     = telegram.Bot(TOKEN)
dp      = updater.dispatcher

dp.add_handler(CommandHandler("start"   , start   ))
dp.add_handler(CommandHandler("motorval", motorval))
dp.add_handler(CommandHandler("setip"   , setip   )) 
dp.add_handler(CommandHandler("help"    , help    ))
dp.add_handler(CommandHandler("test"    , test    ))

client.on_connect = on_connect
client.on_message = on_message

updater.start_polling()
# updater.idle()
client.loop_forever()

# __client.on_connect__ and __client.on_message__ methods are used 
# here for receiving and handling the MQTT messages from the NodeMCU
```



The RaspberryPi Zero listen to the following topics

| **TOPIC** | **MEASURED SENSOR DATA**       |
| --------- | ------------------------------ |
| Current a | R Phase Current                |
| Current b | Y Phase Current                |
| Current c | B Phase Current                |
| Voltage a | R Phase Voltage                |
| Voltage b | Y Phase Voltage                |
| Voltage c | B Phase Voltage                |
| Duration  | Duration of operation of motor |

When there is current in the motor above certain threshold level the clock starts ticking the registers the ON time.

The topics are created by the publisher to which the client subscribers. The publisher and the subscriber are connected to a broker. Here the Raspberry Pi acts as both subscriber and the broker. The local IP address of the broker is coded in the NodeMCU at port **1883**. If the NodeMCU has any errors in establishing connection with the broker, Then the microcontroller tries to reconnect with delay of 5 seconds. Since only characters can be sent to the broker the internal float and integer to character conversion routine is programmed in the NodeMCU.

The Raspberry Pi runs the Eclipse Mosquitto server. Eclipse Mosquitto is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 3.1. All sensors data from the publishers and subscribers are routed through Eclipse Mosquitto server

As a subscriber the Raspberry Pi runs a python program to get the data from the broker and then send those data to telegram server upon the reception. The Raspberry Pi subscribes to these topics and sends these messages to the telegram chat bot server. The python Paho-MQTT library is used to establish client connections. The broker IP address and the port are set in the program through which data is received and acknowledged.

If the connections with the NodeMCU is not established, then the commands to display the motor parameters in Telegram Chat Bot are responded with apt error message.

The program to find the duration of operation of the motor is included in the python program. The duration of operation is started once the required load current is sensed. The time duration is stopped when the current value is less than 100 Milli-Amps. The starting time of operation along with the end time is noted and the total time duration is also displayed in the Chat Bot.



#### Telegram bot commands and responses

| **COMMANDS** | **RESPONSE**                                                 |
| :----------- | ------------------------------------------------------------ |
| setip        | Used for setting the local IP address of the Mosquitto server |
| motorval     | Used for displaying various motor parameters                 |
| help         | Used for listing the available commands and their functions  |
| report       | Sends the logged 3 phase current and voltage data in excel format |
| settime      | This command is used to set the time in terms of minutes after which if the motor is still running an alert is received every one minute |



### Final outcome

#### Screenshots of terminal

* Viewing the three phase current and voltage from ESP8266 using PlatformIO device monitor commands, Pretty useful :smile:

![cli-snapshot](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/cli-snapshot2.png)



* Screenshot of MQTT connection getting established

![mqtt-cli-snapshot](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/mqtt-cli-snapshot.png)





#### Telegram Chat Bot screenshots



![cli-snapshot3](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/cli-snapshot3.png)



![telegram-bot-snapshot](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/telegram-bot-snapshot.png)

![telegram-bot-snapshot2](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/telegram-bot-snapshot2.png)

![telegram-bot-snapshot3](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/telegram-bot-snapshot3.png)

![excel-screenshot](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/excel-snapshot.png)



The Chat Bot logs the 3 phase current and voltage of the motor at the moment along with time and date in CSV format. Upon using the “report” command, the logged report is sent to user through the Chat Bot. The graphical representation of the current and voltage can be done by the user using the Excel formulas. The Chat Bot reports an error every one minute if either one or two wires of the three phase supply to the motor has loose connections. The error will be stopped only when the fault is rectified. With the “settime” command the duration of the operation can be set in terms of minutes. If the motor runs beyond that duration assigned in the “settime” then an alert is pops up in the Chat Bot every one minute. The “settime” value can be reset to reset the alert. The duration can be set in hours to which the motor can be operated in maximum limit.



### Waveform screenshot

Below image shows the captured output voltage of the 3 potential transformer used to measure the 3 phase voltage of the motor. From the oscilloscope graph, It can be clearly seen that the voltage are displaced **120 degrees** apart with almost the same magnitude

![waveform-voltage](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/waveform-voltage.png)





The output of the three current transformer used to measure the 3 phase current output of the motor is a voltage. This voltage is measured across the burden resistor of **100 Ohms**. The waveform output of the current transformers are displaced 120 degrees from each. The output voltage from both the current transformer and the voltage transformer are set to 200 mV when peak values of measurements are reached

![waveform-current](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/waveform-current.png)



The multiplexer switching is done with two second delay and that is observed in the switching input received from the microcontroller in the below image

![waveform-mux](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/waveform-mux.png)



The output of the precision rectification circuit is DC waveform. Fig. 5.10 shows the comparison of the input AC signal and the output of the rectifier. The magnitude of AC signal (peak-peak) and DC is same here and can be observed in the waveform

![waveform-rec](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/waveform-rec.png)



### Assembled Ciruit in General Purpose Board

> The speed sensor is removed from the below diagram. We faced some issue at last in sensing the speed. What we did here is not the standard way of measuring the speed of a motor. Our workaround wasn't effective :pensive:

![assembly](https://github.com/neelabalan/final-semester-project-archive/blob/main/assets/photo-assembly.jpg)



### References

* KeliangZhou ,Taigang Liu, Lifeng Zhou (2015) “Industry 4.0: Towards Future Industrial Opportunities and Challenges”, 2015 12th International Conference on Fuzzy Systems and Knowledge Discovery (FSKD) 
* Li Da Xu, Wu He, Shancang Li (2014) “Internet of Things in Industries: A Survey”, IEEE Transactions On Industrial Informatics, Vol. 10, No. 4, November 2014.
* Dr.BharatiWukkadada, Dr.KirtiWankhede, Mr.RamithNambiar, Ms. Amala Nair (2018) “Comparison with HTTP and MQTT in Internet of Things (IoT)”, International Conference on Inventive Research in Computing Applications (ICIRCA 2018) 
* YazidBenazzouz, Christophe Munilla, OzanGünalp, Mathieu Gallissot, LeventGürgen (2014) “Sharing User IoT Devices in the Cloud”, 2014 IEEE World Forum on Internet of Things (WF-IoT).
* D.K. Chaturvedi, Md. Sharif Iqbal, MayankPratap Singh (2015) “Condition Monitoring of Induction Motor”, 2015 International Conference on Recent Developments in Control, Automation and Power Engineering (RDCAPE)
* Sevil Ahmed, Andon Topalov, Nikola Shakev (2017) “A Robotized Wireless Sensor Network Based on MQTT Cloud Computing”, 2017 IEEE International Workshop of Electronics, Control, Measurement, Signals and Their Application to Mechatronics (ECMSM).
* Breivold, H. P., &Sandstrom, K. (2015), “Internet of Things for Industrial Automation -- Challenges and Technical Solutions”, 2015 IEEE International Conference on Data Science and Data Intensive Systems
* Sen, M., & Kul, B. (2017), “IoT-based wireless induction motor monitoring.”, 2017 XXVI International Scientific Conference Electronics (ET)
* Hunkeler, U., Truong, H. L., & Stanford-Clark, A. (2008) “MQTT-S — A publish/subscribe protocol for Wireless Sensor Networks”, 2008 3rd International Conference on Communication Systems Software and Middleware and Workshops (COMSWARE ’08)
* Heiko Koziolek, Andreas Burger, Jens Doppelhamer, “Self-commissioning Industrial IoT-Systems in Process Automation: a Reference Architecture”, 2018 IEEE International Conference on Software Architecture
* Zhou, K., Taigang Liu, &Lifeng Zhou. (2015) “Industry 4.0: Towards future industrial opportunities and challenges”, 2015 12th International Conference on Fuzzy Systems and Knowledge Discovery (FSKD)
* Ravi Kishore Kodali, KopulwarShishir Mahesh (2016) “A low cost implementation of MQTT using ESP8266”, 2016 2nd International Conference on Contemporary Computing and Informatics.
* HeinerLasi, Hans-Georg Kemper, Peter Fettke, Thomas Feld, Michael Hoffmann (2014) “Industry 4.0. In: Business & Information Systems Engineering”, pp. 239-242
* Kagermann, H., W. Wahlster and J. Helbig, eds., (2013) “Recommendations for implementing the strategic initiative Industrie 4.0”
* M. Ananda Velan, M. Aravind Raj, K. Kannadasan, D.Kirubakaran (2018)“Monitoring and Control of Three Phase Induction Motor Using Iot Based Concept”, International Conference On Progressive Research In Applied Sciences, Engineering And Technology (ICPRASET 2K18)
* J. Dizdarević,F. Carpio,A. Jukan, X. Masip-Bruin, ―A Survey of Communication Protocols for Internet-of-Things and Related Challenges of Fog and Cloud Computing Integration. ‖ACM Computer. Surveys, Volume 1, Number 1, pp. 1-27, April2018
