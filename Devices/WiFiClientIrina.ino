/*
    This sketch establishes a TCP connection to a "quote of the day" service.
    It sends a "hello" message, and then prints received data.
*/

#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID ""
#define STAPSK  ""
#endif

#define PIN_GREEN 4
#define PIN_RED 2
#define PIN_BLUE 0
#define PIN_PHOTO_SENSOR A0
#define PIN_MOTOR1 9
#define PIN_MOTOR2 10
#define PIN_MOTORVAL 14

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "host";
const uint16_t port = ;
String strVal;
WiFiClient client;
int testInt;
int rVal = 0;
int gVal = 0;
int bVal = 0;
int val;
const int freqAver = 1000;

void WiFiBegin()
{

   // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}


bool WiFiConnectToServer ()
{
  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);

  // Use WiFiClient class to create TCP connections
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(5000);
    return false;
  }

  return true;
}

void WiFiSendToServer (String strIn)
{

  // This will send a string to the server
  if (client.connected()) {
    client.println(strIn);
  }
  
}

String WiFiRecvFromServer ()
{

  String strOut;
  // Read all the lines of the reply from server and print them to Serial
  // not testing 'client.connected()' since we do not need to send data here
  while (client.available()) {
    char ch = static_cast<char>(client.read());
    if (ch == ' ')
    {
      break;
    }
    String str(ch);
    strOut = strOut + ch;
  }
  return strOut;
  
}


void WiFiCloseConnection ()
{

  // Close the connection
  Serial.println();
  Serial.println("closing connection");
  client.stop();
  
}

void changeRGB(int R,int G,int B)
{
  analogWrite(PIN_RED,R);
  analogWrite(PIN_GREEN,G);
  analogWrite(PIN_BLUE,B);
}



void setup() 
{
  Serial.begin(115200);
  pinMode(PIN_RED, OUTPUT);  
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BLUE, OUTPUT);  
  pinMode(PIN_MOTOR1, OUTPUT);
  pinMode(PIN_MOTOR2, OUTPUT);  
  pinMode(PIN_MOTORVAL, OUTPUT);
  WiFiBegin();
}

void loop() 
{
  
  if (!(WiFiConnectToServer ()))
  {
    return;
  }

  int timeMilStart = millis();
  int timeMilNow = millis();
  while ((client.available() != 0) || (timeMilNow - timeMilStart < 10000))
  {
    strVal = WiFiRecvFromServer ();
    int numPacket = strVal.toInt();

    if (numPacket == 1)
    {
      strVal = WiFiRecvFromServer ();
      rVal = strVal.toInt();

      strVal = WiFiRecvFromServer ();
      gVal = strVal.toInt();

      strVal = WiFiRecvFromServer ();
      bVal = strVal.toInt();

      changeRGB(rVal,gVal,bVal);
      WiFiSendToServer("RGB change ok");
      break;
    }

    if (numPacket == 2)
    {
       WiFiSendToServer("RGB: R - " + String(rVal) + ", G - " + String(gVal) + ", B - " + String(bVal));
       break;
    }

    if (numPacket == 3)
    {

      val = 0;
      
       for(int i = 0; i<freqAver; i++)
      {
        val += analogRead(PIN_PHOTO_SENSOR);
      }

       WiFiSendToServer("Photoresistor value " +String(val/freqAver));
       break;
      
    }

    if (numPacket == 4)
    {
      strVal = WiFiRecvFromServer ();
      int motorVal = strVal.toInt();

      if (motorVal > 0)
      {
        digitalWrite(PIN_MOTOR1, HIGH);
        digitalWrite(PIN_MOTOR2, LOW);
      }

      if (motorVal < 0)
      {
        digitalWrite(PIN_MOTOR1, LOW);
        digitalWrite(PIN_MOTOR2, HIGH);
      }

      if (motorVal == 0)
      {
        digitalWrite(PIN_MOTOR1, LOW);
        digitalWrite(PIN_MOTOR2, LOW);
        
      }

      analogWrite(PIN_MOTORVAL, motorVal);
      WiFiSendToServer("motor value changed");
      break;
      }

    timeMilNow = millis();
  }

  delay(500);
  
}
