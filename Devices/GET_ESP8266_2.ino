// this is type 2 of devices

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define STASSID ""
#define STAPSK  ""

#define UID ""
#define PIN_PHOTO_SENSOR A0
#define PIN_MOTOR1 0
#define PIN_MOTOR2 2

const int freqAver = 10;

const char* ssid = STASSID;
const char* password =  STAPSK;

char rpi[128];

int pVal = 0;
int mVal = 2;

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
  
  post_info_lighter.add(-1);
  post_info_lighter.add(-1);
  post_info_lighter.add(-1);
  
  getLight();
  Serial.println(pVal);
  post_info["uid"] = (const char*)UID;
  Serial.println(UID);
  post_info["rpi"] = (const char*)rpi;
  Serial.println((const char*)rpi);
  post_info["light"] = pVal;
  post_info["motor"] = mVal;
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
      String payload = http.getString();
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

    http.begin("http://host:port/api/v1.0/update/device");
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(output);
    
    DynamicJsonDocument get_change(1000);

    if (httpCode == 201) 
    {
        payload = http.getString();
        payload.toCharArray(_str, 256);
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
            if (get_change.containsKey("motor"))
            {
              mVal = get_change["motor"];
              changeMotor(mVal);
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

void changeMotor(int M)
{
  if (mVal == 1)
  {
    if (M == 2)
    {
      digitalWrite(PIN_MOTOR1, HIGH);
      digitalWrite(PIN_MOTOR2, LOW);
      mVal = 2;
      delay(2000);
      digitalWrite(PIN_MOTOR1, LOW);
      return;
    }
  }
  if (mVal == 2)
  {
    if (M == 1)
    {
      digitalWrite(PIN_MOTOR1, LOW);
      digitalWrite(PIN_MOTOR2, HIGH);
      mVal = 1;
      delay(2000);
      digitalWrite(PIN_MOTOR2, LOW);
      return;
    }
  }
}

void getLight()
{
  pVal = 0;
      
  for(int i = 0; i<freqAver; i++)
  {
    pVal += analogRead(PIN_PHOTO_SENSOR);
  }

  pVal /= freqAver;
}

void setup() 
{
  Serial.begin(115200);
  pinMode(PIN_MOTOR1, OUTPUT);
  pinMode(PIN_MOTOR2, OUTPUT);  
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
