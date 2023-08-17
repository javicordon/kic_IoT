# Project Title

Motion detection with email alerts using esp8266

## Getting Started

This project allow to to use esp8266 with a PIR sensor to monitor and detect motion. In the case of no motion detected within a specific timeframe an email is sent to remind the user to turn off the Air condtioner.


### Prerequisites

The tools and equipment used 

* esp8266
* PIR sensor
* breadboard
* wires
* USB cable

### Installation
---------------------------------------------------------------------
* Gmail Email account creation and setup :  
1- Create an email address on gmail.com
You need to create an app password so that the ESP32 is able to send emails using your Gmail account. 
An App Password is a 16-digit passcode that gives a less secure app or device permission to access your Google Account
2- Open your Google Account.
3- In the navigation panel, select Security.
4- Under “Signing in to Google,” select 2-Step Verification > Get started.

After enabling 2-step verification, you can create an app password.

5- Open your Google Account.
6- In the navigation panel, select Security.
7- Under “Signing in to Google,” select App Passwords.
---------------------------------------------------------------------
* esp8266 and PIR sensor setup 
1- The VCC of the PIR sensor needs to be connected to the VIN of the esp8266
2- The GND of the PIR sensor needs to be connected to the GND of the esp8266
3- The output of the PIR sensor needs to be connected to the D1 pin 

---------------------------------------------------------------------


## Code setup

When using the code there are lines that needs to be adjusted depending on the WIFI connection used and the email address ;

const char* ssid = "YourWiFiSSID";
const char* password = "YourWiFiPassword";

-----------

const char* emailSenderAddress = "YourEmailAddress";
const char* emailSenderPassword = "YourEmailPassword";
const char* emailRecipientAddress = "TheRecepientEmailAddress";