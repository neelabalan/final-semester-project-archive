// include files
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Arduino.h>
#include <Adafruit_ADS1015.cpp>
#include <Wire.h>
#include <PubSubClient.cpp>

// defines
#define TRUE  1
#define FALSE 0
#define HSENS D5
#define MUX_A D6
#define MUX_B D7
#define MUX_C D8
#define SECOND 1000

#define DELAY_500 delay(2000)
#define DELAY_200 delay(200)


// function declaration
void get_currenta();
void get_currentb();
void get_currentc();
void get_voltagea();
void get_voltageb();
void get_voltagec();

void setup_wifi();
void mqtt_reconnect();
void callback(char*, byte*, unsigned int);
//void reconnect();

void set_muxpin();
void changeMux(int c, int b, int a);

void float_conversion(float);
void int_conversion(unsigned int);
void reset_buffer(char buff[]);

int   find_voltage(unsigned int);
float find_current(unsigned int);

// variable declaration and initialization

unsigned int ADC_UP_COUNT   = 32768;        // adc maximum count
unsigned int ADC_LIMIT      = 31000;        // adc upper limit count
unsigned int motor_rpm		= 0;
bool LEDstatus              = LOW;
unsigned long previous_ms   = 0;
unsigned long current_ms    = 0;
const char* ssid            = "cowabunga";
const char* password        = "cowabunga";
const char* mqtt_server     = "192.168.43.111";
const char* clientname      = "espdeviceOne";
long lastmsg                = 0;
char msg[50]                = "";
int value                   = 0;
float adc1                  = 0;
char buffer[64];
//IPAddress mqtt_server(192, 168, 1, 9);
WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_ADS1115 ads;


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
	//pinMode(HSENS, INPUT) ;  
   
    // wifi setup
    setup_wifi();


    // setting up mqtt server
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
}

void loop(void)
{
	int flag=1;
	if(client.connected() == TRUE)
    {
        int counter=0;
		bool flag=LOW;
		
		get_currenta();
		client.publish("esp1/currenta", buffer);
        reset_buffer(buffer);
        DELAY_200;
		
        get_currentb();
		client.publish("esp1/currentb", buffer);
        reset_buffer(buffer);
        DELAY_200;

		get_currentc();
		client.publish("esp1/currentc", buffer);
        reset_buffer(buffer);
        DELAY_200;


		get_voltagea();
		client.publish("esp1/voltagea", buffer);
        reset_buffer(buffer);

		get_voltageb();
	    client.publish("esp1/voltageb", buffer);
        reset_buffer(buffer);

		get_voltagec();
    	client.publish("esp1/voltagec", buffer);
        reset_buffer(buffer);



		Serial.println("connection on");

	}
	else
	{
		mqtt_reconnect();
        Serial.println("reconnection on process");
    }

    client.loop();  
}

void float_conversion(float adc1)
{
    
    int ret = snprintf(buffer, sizeof buffer, "%f", adc1);

    if (ret < 0)
    {
        Serial.println("FLOAT BUFFER ERROR");
    }
    // else (ret >= sizeof buffer)
    // result was truncated - resize the buffer and try again
}

void int_conversion(unsigned int adc1)
{
    int ret = snprintf(buffer, sizeof buffer, "%d", adc1);

    if(ret < 0)
    {
        Serial.println("INTEGER BUFFER ERROR");
    }
    // else (ret >= sizeof buffer)
}

int find_voltage(unsigned int adccount)
{
    int motor_voltage=0;
    if(adccount<ADC_LIMIT)
    {
        motor_voltage = (450*adccount)/ADC_UP_COUNT;
    }
    else
    {
        Serial.println("-- OVER VOLTAGE LIMIT ERROR --");
    }
    return motor_voltage;
    
}

float find_current(unsigned int adccount)
{
   float motor_current=0;
   if(adccount<ADC_LIMIT)
   {
        motor_current = (1.5*adccount)/ADC_UP_COUNT;
   } 
   else
   {
   		Serial.println("-- OVER CURRENT LIMIT ERROR --");
   }

   return motor_current;
}

void reset_buffer(char buf[])
{
    for(int i=0; i<sizeof(buf); i++)
    {
        buf[i]=0;
    }
}

void setup_wifi()
{
    delay(10);
    Serial.println();
    Serial.println("connecting to SSID - ");
    Serial.println(ssid);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    while(WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connection established");
    Serial.println("IP Address - ");
    Serial.println(WiFi.localIP());
}


void mqtt_reconnect() 
{                                                    
   while (client.connected() == FALSE) 
   {                                       
        Serial.print("Attempting MQTT connection...");                    
        if (client.connect(clientname) == TRUE)
        {                           
           Serial.println("--MQTT connection established--");                                    
        } 
        else
        {                                                          
            Serial.print("FAILED MQTT CONNECTION, ERROR=");                                    
            Serial.print(client.state());                                   
            Serial.println(" try again in 5 seconds");                      
            delay(5000);                                                    
        }                                                                 
    }                                                                   
}

void callback(char* topic, byte* payload, unsigned int length)
{
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");

    for(int i=0; i<length; i++)
    {
        Serial.print((char)payload[i]);
    }
}

void changeMux(int c, int b, int a)
{
  digitalWrite(MUX_A, a);
  digitalWrite(MUX_B, b);
  digitalWrite(MUX_C, c);
}

void get_currenta()
{
    unsigned int current_phaseA=0;
    changeMux(0, 0, 0);
    DELAY_500;
    current_phaseA  = ads.readADC_SingleEnded(1);
    float current_a = find_current(current_phaseA);
    float_conversion(current_a);

    Serial.println("CURRENT A - "); 
    Serial.print(current_a);
    Serial.print("  -   ");
    Serial.print(buffer);
}
void get_currentb()
{
    unsigned int current_phaseB=0;
    changeMux(0, 0, 1);
    DELAY_500;
    current_phaseB  = ads.readADC_SingleEnded(1);
    float current_b = find_current(current_phaseB); 
    float_conversion(current_b);
    
    Serial.println("CURRENT B  "); 
    Serial.print(current_b); 
    Serial.print("  -  ");
    Serial.print(buffer);

}
void get_currentc()
{
  
    unsigned int current_phaseC=0;
    changeMux(0, 1, 0);
    DELAY_500;
    current_phaseC  = ads.readADC_SingleEnded(1);
    float current_c = find_current(current_phaseC);
    float_conversion(current_c);

    Serial.println("CURRENT C  "); 
    Serial.print(current_c);
    Serial.print("  -  ");
    Serial.print(buffer);

}
void get_voltagea()
{
    unsigned int voltage_phaseA=0;
    DELAY_200;
    changeMux(0, 1, 1);
    DELAY_500;
    voltage_phaseA = ads.readADC_SingleEnded(1);
    int voltage_a  = find_voltage(voltage_phaseA); 
    int_conversion(voltage_a);

    Serial.println("VOLTAGE A  "); 
    Serial.print(voltage_a);
    Serial.print("  -  ");
    Serial.print(buffer);

}
void get_voltageb()
{
    unsigned int voltage_phaseB=0;
    DELAY_200;
    changeMux(1, 0, 0);
    DELAY_500;
    voltage_phaseB = ads.readADC_SingleEnded(1);
    int voltage_b  = find_voltage(voltage_phaseB); 
    int_conversion(voltage_b);

    Serial.println("VOLTAGE B  "); 
    Serial.print(voltage_b);
    Serial.print("  -  ");
    Serial.print(buffer);

}
void get_voltagec()
{
    unsigned int voltage_phaseC=0;
    DELAY_200;
    changeMux(1, 0, 1);
    DELAY_500;
    voltage_phaseC = ads.readADC_SingleEnded(1);
    int voltage_c = find_voltage(voltage_phaseC);
    int_conversion(voltage_c);

    Serial.println("VOLTAGE C "); 
    Serial.print(voltage_c);
    Serial.print("  -  ");
    Serial.print(buffer);

}
  
 


/* Put IP Address details */



/*
IPAddress local_ip(192,168,0,123);
IPAddress gateway(192,168,0,1);
IPAddress subnet(255,255,255,0);

*/
