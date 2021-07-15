import time
import _thread
import machine
from machine import Pin
from machine import PWM
from machine import ADC
from machine import Timer
import machine
from math import sqrt

import webrepl
webrepl.start()

#machine.freq(80000000)
print(machine.freq())
time.sleep(1)


def logToFile(s):
    f = open('log.log', 'a+')
    f.write(s)
    f.write('\n')
    f.close()
    
#Solar tracking stuff below

#restart timer, so auto updates will be checked
restartTimer = Timer(0)
#restartHandler for handling the timer
def restartHandler(timer):
    print('RESTARTING!!!')
    time.sleep(1)
    machine.reset()
#initialize the timer

#Pin Setup
#For motor controller
#motorPower controls the power sent to the motor controller by PulseWidthModulation, on the ENA pin on the motor controller
motorPowerPin = Pin(13, Pin.OUT) #ENA pin, not picked out yet Pin(2, Pin.OUT)
motorPowerPWM = PWM(motorPowerPin)
motorPowerPWM.freq(500) #undecided
motorPowerPWM.duty(0) #undecided

dutyCycle = 800 # value between 0 and 023

#onPin1 sends a signal to the motor controller, pin N!, to move the motor one way 
onPin1 = Pin(12, Pin.OUT) #N1, undecided Pin(2, Pin.OUT)
#onPin2 sends a signal to the motor controller, pin N2, to move the motor one way 
onPin2 = Pin(14, Pin.OUT) #N2, undecided Pin(2, Pin.OUT)

#For solar sensors
rightSolarSensorPin = machine.Pin(36)
leftSolarSensorPin = machine.Pin(39)
solarSensorRight = ADC(rightSolarSensorPin)
solarSensorLeft = ADC(leftSolarSensorPin)

solarSensorRight.atten(ADC.ATTN_11DB)
solarSensorLeft.atten(ADC.ATTN_11DB)
#End Pin Setup

#motorTest will test the bi directional motor control
def motorTest():
    motorPowerPWM.duty(950)
    onPin1.value(1)
    time.sleep(1)
    onPin1.value(0)
    onPin2.value(1)
    time.sleep(1)
    onPin2.value(0)
    motorPowerPWM.duty(0)

motorTest()

#Mean will get the mean of the samples
#currently unused for reducing signal erros
def Mean(samples):
    samples.sort()
    return samples[3] #hard coded for five samples at the moment

#ReadSensor recieves an ADC object and a number for how many times to check the sensor and  will take a reading and return the results
def ReadSensor(sensor, count):
    samples = [] #array of sensor samples
    loopCount = 0 
    avg = 0.0
    while loopCount < count:
        samples.append(sensor.read())
        loopCount += 1
        
    
    #get and return the average of the samples
    for s in samples:
        avg += s
        if s > 100:
            print(s)
    return avg / len(samples)


#run will be called from main, and run the solar tracking program
def run():
    restartTimer.init(period=100000000, mode=Timer.PERIODIC, callback=restartHandler)

    #runing motor test
    motorTest()
    #start of solarTracking loop  
    deadZone = 15
    signalDifference = 0
    c = 10000
    x = 0
    while x < c:
        x += 1
        sensorReadingR = ReadSensor(solarSensorRight, 5)
        sensorReadingL = ReadSensor(solarSensorLeft, 5)

        print('right: ', sensorReadingR)
        print('left: ', sensorReadingL)
        signalDifference = abs(sensorReadingR - sensorReadingL)
        print('diff: ', signalDifference)
        if signalDifference > deadZone:
            if sensorReadingL > sensorReadingR:
                s = 'L: ' + str(sensorReadingL) + ' > R: ' + str(sensorReadingR)
                logToFile(s)
                s = 'XXXXX turning onPin1'
                logToFile(s)
                
                #move motor
                print('L > R')
                onPin2.value(0)#make sure pin 2 is low
                onPin1.value(1)#make sure pin 1 is high
                motorPowerPWM.duty(dutyCycle) # power the pwm
                time.sleep(0.1)
            if sensorReadingL < sensorReadingR:
                s = 'R: ' + str(sensorReadingR) + ' > L: ' + str(sensorReadingL)
                logToFile(s)
                s = 'XXXXX turning onPin2'
                logToFile(s)
                
                #
                #move motor
                print('L < R')
                onPin1.value(0)#make sure pin 2 is low
                onPin2.value(1)#make sure pin 1 is high
                motorPowerPWM.duty(dutyCycle) # power the pwm
                time.sleep(0.1)
        else: 
            print('else')
            #set motor controls to zero and wait for a bit
            onPin2.value(0)#make sure pin 2 is low
            onPin1.value(0)#make sure pin 1 is high
            motorPowerPWM.duty(0) # power the pwm
            s = 'L: ' + str(sensorReadingL) + ' =kinda= R: ' + str(sensorReadingR)
            logToFile(s)
            s = 'XXXXX power down both pins'
            logToFile(s)
            #
            time.sleep(300)
