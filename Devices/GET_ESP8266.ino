// this is type 1 of devices

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define STASSID ""
#define STAPSK  ""

#define UID ""
#define PIN_GREEN 4
#define PIN_RED 4
#define PIN_BLUE 2
#define PIN_PHOTO_SENSOR A0

const int freqAver = 10;

const char* ssid = STASSID;
const char* password =  STAPSK;

char rpi[128];

int rVal = 0;
int gVal = 0;
int bVal = 0;
int pVal = 0;

char output[256];
char _str[256];
String payload;

const int post_init_capacity = JSON_OBJECT_SIZE(2);
const int get_init_capacity = JSON_OBJECT_SIZE(3);
const int post_info_capacity = JSON_OBJECT_SIZE(5) + JSON_OBJECT_SIZE(3);
const int post_change_capacity = JSON_OBJECT_SIZE(3);
const int get_change_capacity = JSON_OBJECT_SIZE(3) + JSON_OBJECT_SIZE(3);

DeserializationError err;

void WiFiBegin()
{
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");
  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(2000);
}

void InitDeviceInNetwork()
{
  StaticJsonDocument<post_init_capacity> post_init;
  post_init["uid"] = UID;
  serializeJson(post_init, output);
  
  if ((WiFi.status() == WL_CONNECTED)) 
  { 
    HTTPClient http;
    http.begin("http://host:port/api/v1.0/system/device");
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(output);
    
    StaticJsonDocument<get_init_capacity> get_init;
    
    if (httpCode == 201) 
    {
        payload = http.getString();        
        http.end();
        payload.toCharArray(_str, 256);
        err = deserializeJson(get_init, _str);
        if(err)
        {
          Serial.print(F("deserializeJson() failed with code "));
          Serial.println(err.c_str());
        }
        if (get_init.containsKey("status"))
        {
          if (get_init["status"] == 1)
          {
            if (get_init.containsKey("rpi"))
            {
              const char* _rpi = get_init["rpi"];
              if (_rpi[0] == '0' && _rpi[2] == '0')
              {
                for (int i = 0; i < strlen(_rpi); ++i){
                  rpi[i] = _rpi[i];
                }
                Serial.print("Secessfully added devise into network. RPI "); 
                Serial.println(rpi); 
              }
              else
              {
                Serial.println("Wrong host answered. Check host");
              }
            }
            else
            {
              Serial.println("Fail adding devise into network. Wrong request");
            }
          }
          if (get_init["status"] == 2)
          {
            Serial.println("Device already in network");
            if (get_init.containsKey("rpi"))
            {
              const char* _rpi = get_init["rpi"];
              if (_rpi[0] == '0' && _rpi[2] == '0')
              {
                for (int i = 0; i < strlen(_rpi); ++i){
                  rpi[i] = _rpi[i];
                }
                Serial.print("Secessfully added devise into network. RPI "); 
                Serial.println(rpi);
              }
              else
              {
                Serial.println("Wrong host answered. Check host");
              }
            }
            else
            {
              Serial.println("Fail adding devise into network. Wrong request");
            }
          }
          else
          {
            Serial.println("Fail adding devise into network. Check host");  
          }
        }
        else
        {
          Serial.println("Fail adding devise into network. Wrong request");
        }
    }
    else 
    {
      Serial.print("Error on HTTP request. Code ");
      Serial.println(String(httpCode));
    }
  }
  delay(2000);
}

void SendInfoDevice()
{
  DynamicJsonDocument post_info(1000);
  Serial.println("Init");
  JsonArray post_info_lighter = post_info.createNestedArray("lighter");
  Serial.println("Init");
  
  post_info_lighter.add(rVal);
  post_info_lighter.add(gVal);
  post_info_lighter.add(bVal);
  
  getLight();
  Serial.println(pVal);
  post_info["uid"] = (const char*)UID;
  Serial.println(UID);
  post_info["rpi"] = (const char*)rpi;
  Serial.println((const char*)rpi);
  post_info["light"] = pVal;
  post_info["motor"] = -1;
  serializeJson(post_info, output);
  Serial.println(output);
  
  if ((WiFi.status() == WL_CONNECTED)) 
  { 
    HTTPClient http;
    http.begin("http://host:port/api/v1.0/info/device");
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(output);
    if (httpCode == 201) 
    {
      payload = http.getString();
      Serial.println(payload);
    }
    else 
    {
      Serial.print("Error on HTTP request. Code: ");
      Serial.println(String(httpCode));
    }
    http.end();
  }
}


void GetInfoDevice()
{
  DynamicJsonDocument post_change(1000);
  Serial.println("Init");
  post_change["uid"] = (const char*)UID;
  Serial.println(UID);
  post_change["rpi"] = (const char*)rpi;
  Serial.println((const char*)rpi);
  serializeJson(post_change, output);
  Serial.println(output);
  
  if ((WiFi.status() == WL_CONNECTED)) 
  { 
    HTTPClient http;
    int httpCode;
    http.begin("http://host:port/api/v1.0/update/device");
    http.addHeader("Content-Type", "application/json");
    httpCode = http.POST(output);
    
    DynamicJsonDocument get_change(1000);
    
    if (httpCode == 201) 
    {
      payload = http.getString();
      Serial.println(payload);
      payload.toCharArray(_str, 256);
      Serial.println(_str);
      DeserializationError err = deserializeJson(get_change, _str);
      if(err)
      {
        Serial.print(F("deserializeJson() failed with code "));
        Serial.println(err.c_str());
      }
      if (get_change.containsKey("change"))
      {
        if (get_change["change"] == 1)
        {
          if (get_change.containsKey("lighter"))
          {
            rVal = get_change["lighter"][0];
            gVal = get_change["lighter"][1];
            bVal = get_change["lighter"][2];
            changeRGB(rVal, gVal, bVal);
          }
          else
          {
            Serial.println("Fail in changing. Wrong request");
          }
        }
      }
      else
      {
        Serial.println("Fail in changing. Wrong request");
      }
    }
    else 
    {
      Serial.print("Error on HTTP request. Code: ");
      Serial.println(String(httpCode));
    }
    http.end();
  }
}

void changeRGB(int R, int G, int B)
{
  analogWrite(PIN_RED, R);
  analogWrite(PIN_GREEN, G);
  analogWrite(PIN_BLUE, B);
}

void getLight()
{
  unsigned long tmp = 0;
  for(int i = 0; i<freqAver; i++)
  {
    tmp += (unsigned long)analogRead(PIN_PHOTO_SENSOR);
  }
  Serial.println((String)tmp);
  pVal = (int)(tmp / freqAver);
}

void setup() 
{
  Serial.begin(115200);
  pinMode(PIN_RED, OUTPUT);  
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BLUE, OUTPUT);  
  rVal = 0;
  gVal = 0;
  bVal = 0;
  changeRGB(rVal, gVal, bVal);
  
  WiFiBegin();
  InitDeviceInNetwork();
}

void loop() 
{
  SendInfoDevice();
  delay(1000);
  GetInfoDevice();
  delay(1000);
}
