import time
import machine
import dht
import ubinascii
import ujson
import network
import usocket

WIFI_SSID = "Attack"
WIFI_PASSWORD = "asdf1234"
AWS_IOT_ENDPOINT = "a2eeevfozxj6nc-ats.iot.us-east-1.amazonaws.com"

AWS_CERT_CA = static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
)EOF";

AWS_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
MIIDWjCCAkKgAwIBAgIVAPHaIsy3ZXj/zM3pKEQYfJv8bxofMA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yMzA4MTQxNzI5
MzFaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQClIxsckWaI6EAX611n
yGHOWdCOg6/E8glM+kA7yfzF8LxakxaApWF2A+adnyG3T1Ucu7Qi2IaBUrnPV9wb
qU7CIxApwskb+lSJ0I4ywZVOLjlASmop0lmZqL9NkqS22MSx9yijvNx9DVWjfCqr
utpAvg13RhsTsJB9MmMtdpIOwR97vbPwmLxfRVaPe6iEV1n+fiqc1N1DxfoNXZ89
w5TCmYpbQBjtMpZb6/dTgq6km5/2qLoPnKxguFbSp0UGTGe7LCPOU4Qod+gj7DZn
NRbaR2AkOBugZoAnAbpLkr0Zox1aluRF/NACKqwZWZxQkZhy5UskCV9tuGVd2n+M
Efa/AgMBAAGjYDBeMB8GA1UdIwQYMBaAFOC40SQ++kiDUwkhBUTq9WxoBuKWMB0G
A1UdDgQWBBRYhF9A+n3irIlWIaMb5FQZ8WcRczAMBgNVHRMBAf8EAjAAMA4GA1Ud
DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAKcOUcbY0bu20cg68dhTlXSV3
06S5Hnh9gFGKmLro2f+tZGmeYnjpKASIcjsX9m+acSUOHfdyMXhMnjt1D9U7N5PE
bi1poAkVN1U2T88K0Te9KWw74RokB4iesQTQwqG8MCDHBAaj/BLo9Q/7/d1tUxbQ
lEm6AW6tZlRhLo738mziyhO/TGnPrjx+qpU1UT1tYjaB13GXj5FZHQjCFMq+Kdki
iEpQSvjeEAX52N2riQMi55ChdrPogrrlIbztMwdBlllFYjqcerHi4xhAlsl7Gw4N
OA9Ikqly8PfRzf3VWLr57/PD/EFEMyfe2bmiPiZJBugtfLw5gcaghUrnfy2scA==
-----END CERTIFICATE-----
)KEY";

AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEApSMbHJFmiOhAF+tdZ8hhzlnQjoOvxPIJTPpAO8n8xfC8WpMW
gKVhdgPmnZ8ht09VHLu0ItiGgVK5z1fcG6lOwiMQKcLJG/pUidCOMsGVTi45QEpq
KdJZmai/TZKkttjEsfcoo7zcfQ1Vo3wqq7raQL4Nd0YbE7CQfTJjLXaSDsEfe72z
8Ji8X0VWj3uohFdZ/n4qnNTdQ8X6DV2fPcOUwpmKW0AY7TKWW+v3U4KupJuf9qi6
D5ysYLhW0qdFBkxnuywjzlOEKHfoI+w2ZzUW2kdgJDgboGaAJwG6S5K9GaMdWpbk
RfzQAiqsGVmcUJGYcuVLJAlfbbhlXdp/jBH2vwIDAQABAoIBAE1BczmWPGXoYbPP
BM+8yyUCl7NUoDJ/GSLOIKbYBE2GJlgpX+mndUUE5irve5KKpsLefZOfwK1Xyl3a
OLsoJhRk2vbuja9tGYev7haIwhTlQxt0tN4D7q8YZwcfh7eTCdJIUtbnUC+gwWPO
fxgAPoLzZtFaFujLPY2UuRlX01Ta/AdnI6dA+A/wUMbt+XfeL3Ms+oaOjNwMRwoe
cr5r7u8R2wfWyMOTWfBntoiyKBg8MM64anvAKyHiei70fs1F7Ftc1padaHoKQEDa
HhBJku5kEUX3mmU6ElQs+YSB8k00zqbIocnoO9QYCxmz+ljS8l//mqM+r0bkCvuQ
HXIMs4ECgYEA198d/SW0GehBKvE9YX75yp6BMut3R58z3tA/VtXXaZJgeQw5b0rk
8xkYS68/AYUkMPKGR7Zg/xXDCReTG6HHoxpEmu8wpxElQs98SMOhkWQRK9TBdtK6
4ZXCYq5D/j0M2ct3eZtm4avuJfPFtB8SmL2hFHMYZ8XY6MKueW7G0RECgYEAw9Wk
ZdB/tbpx4PH74LSta/YLWR7NveZbPXxUUIO4n5c3rkSOn4cmNvwkRSNXEwCA8Yv9
XT1BoZYO4ukDR97rFnG8VYJa4XABs7LeWl1Xk9LNCPm41jFlBL+LLR5/as33QShl
DELEG1JuGB4JkdnymRVFU8HuG4M9jgshqXLgSs8CgYEAtEIOY6XJN1z2leotzCzg
Xu5uiluPFdJ92M/iJBuargBZ6Jppl2JdvhU1cXWb0iQgbXMG5/kGE9tTKlNyNr+n
2a2Eni+fW9J4X8qsSIJ7dtGteQFGr3cWMGsCj65e/nxyL6e0U2qNxWHxEeX2MAtG
Vx750/6r4XOXRf3S/XmgMVECgYATyZyI5R5iYGptTkYjGF6FkCDpamFjlMkXV161
m/mltoPbyfWXTPKhj6yih8Wel+hvf7OkHjJpf14Vs3Gva2jZpbhf84H3UXf6jlJF
UzUsLJqnE4SHsAoDBs+rSW+afSFEpi4/pOdn01ZofXB+GkWXDj0pD2ldwk8P8TP/
iSn8pQKBgFe0UE/Z79V/qUw5lSFEZr+kh+/mgbfYu2gMrI0/E/THYj7PLKBLMBjH
lmiJD2jmva7+Yjwf3NmjyCj+nPZdcZHR+HlTJbwe5vcvEb8eb7VrofyO+BXAvy58
Mjkp931B2NiJxwYN/NhfIbF2f9ME2XqTmPbyY3pA/qyKn7v6aF8k
-----END RSA PRIVATE KEY-----
)KEY";

AWS_IOT_ENDPOINT = b"a2eeevfozxj6nc-ats.iot.us-east-1.amazonaws.com"
AWS_IOT_PUBLISH_TOPIC = b"esp32/pub"
AWS_IOT_SUBSCRIBE_TOPIC = b"esp32/sub"
THINGNAME = ubinascii.hexlify(machine.unique_id()).decode()

h = 0.0
t = 0.0

dht_pin = machine.Pin(26)
dht_sensor = dht.DHT11(dht_pin)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    pass

client = MQTTClient(THINGNAME, AWS_IOT_ENDPOINT, port=8883)
client.set_callback(lambda topic, msg: message_handler(topic, msg))
client.connect()
client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC)

def message_handler(topic, msg):
    print("incoming:", topic)
    doc = ujson.loads(msg)
    message = doc["message"]
    print(message)

def publish_message():
    doc = {
        "humidity": h,
        "temperature": t,
    }
    json_payload = ujson.dumps(doc)
    client.publish(AWS_IOT_PUBLISH_TOPIC, json_payload)

while True:
    h = dht_sensor.humidity()
    t = dht_sensor.temperature()

    if isinstance(h, float) and isinstance(t, float):
        print("Humidity: {}%  Temperature: {}°C".format(h, t))
        publish_message()
    else:
        print("Failed to read from DHT sensor!")

    client.check_msg()
    time.sleep(1)
def connect_aws():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        pass
    
    client_id = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    c = MQTTClient(client_id, AWS_IOT_ENDPOINT, ssl=True,
                   ssl_params={"ca_certs": AWS_CERT_CA, 
                               "certfile": AWS_CERT_CRT, 
                               "keyfile": AWS_CERT_PRIVATE})
    c.connect()
    c.subscribe(THINGNAME + "/sub")
    return c

def publish_message(client, h, t):
    data = {
        "humidity": h,
        "temperature": t
    }
    json_data = ujson.dumps(data)
    client.publish(THINGNAME + "/pub", json_data)

def main():
    d = dht.DHT11(dht.DHT11)
    client = connect_aws()
    
    while True:
        try:
            d.measure()
            h = d.humidity()
            t = d.temperature()
            if h is not None and t is not None:
                publish_message(client, h, t)
                print("Humidity:", h, "% Temperature:", t, "°C")
        except Exception as e:
            print("Error:", e)
    
        utime.sleep(10)

if __name__ == '__main__':
    main()