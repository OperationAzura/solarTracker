# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
webrepl.start()

# Complete project details at https://RandomNerdTutorials.com

import socket
from machine import Pin
from machine import PWM
import network

import time

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'DWW 2.4'
password = 'bazinga1'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
ledPWM = PWM(led)
ledPWM.freq(15)
ledPWM.duty(0)