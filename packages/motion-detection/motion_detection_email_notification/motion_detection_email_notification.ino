#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <base64.h>

const char* ssid = "HIH-Dorm";
const char* password = "welcomehyogo";

const char* smtpServer = "smtp.gmail.com";
const int smtpPort = 465;

const char* emailSenderAddress = "iotsuperteam@gmail.com";
const char* emailSenderPassword = "mqduehzfrzngcgxt";
const char* emailRecipientAddress = "iotsuperteam@gmail.com";

const int pirPin = D1;

unsigned long lastMotionTime = 0;
bool motionDetected = false;

void setup() {
  pinMode(pirPin, INPUT);

  Serial.begin(115200);
  delay(10);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  int pirState = digitalRead(pirPin);

  if (pirState == HIGH) {
    motionDetected = true;
    lastMotionTime = millis();
  }

  if (motionDetected && (millis() - lastMotionTime > 60000)) { // 10 minutes in milliseconds
    sendMotionAlertEmail();
    motionDetected = false;
  }

  delay(100);
}

void sendMotionAlertEmail() {
  WiFiClientSecure client;
  client.setInsecure(); // Allow connections to servers with self-signed certificates

  if (client.connect(smtpServer, smtpPort)) {
Serial.println("Connected to SMTP server");
    client.println("HELO example.com");
    delay(100);

    client.println("AUTH LOGIN");
    delay(100);
    client.println(base64::encode(emailSenderAddress));
    delay(100);
    client.println(base64::encode(emailSenderPassword));
    delay(100);

    client.println("MAIL FROM:<" + String(emailSenderAddress) + ">");
    delay(100);
    client.println("RCPT TO:<" + String(emailRecipientAddress) + ">");
    delay(100);

    client.println("DATA");
    delay(100);
    client.println("From: " + String(emailSenderAddress));
    client.println("To: " + String(emailRecipientAddress));
    client.println("Subject: Motion not Detected!");
    client.println();
    client.println("Motion has not been detected by the PIR sensor did you remember to turn off the AC.");
    client.println(".");
    delay(100);

    client.println("QUIT");
    delay(100);
    client.stop();
    Serial.println("Email sent successfully!");
  } else {
    Serial.println("Failed to connect to SMTP server");
  }
}