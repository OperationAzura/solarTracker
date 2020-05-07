import time
import _thread
import machine
from machine import ADC
from math import sqrt
#machine.freq(80000000)
print(machine.freq())
time.sleep(1)

#Solar tracking stuff below

#Pin Setup
#For motor controller
#motorPower controls the power sent to the motor controller by PulseWidthModulation, on the ENA pin on the motor controller
motorPowerPin = Pin(13, Pin.OUT) #ENA pin, not picked out yet Pin(2, Pin.OUT)
motorPowerPWM = PWM(motorPowerPin)
motorPowerPWM.freq(500) #undecided
motorPowerPWM.duty(0) #undecided

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
    #runing motor test
    #motorTest()
    #start of solarTracking loop  
    deadZone = 5
    signalDifference = 0
    x = 0
    while x < 10:
        x += 1
        r = ReadSensor(solarSensorRight, 5)
        l = ReadSensor(solarSensorLeft, 5)
        print( 'right sensor: ', r)
        print('left sensor: ', l)
        dif = abs(r - l)
        #print('dif: ', dif)
        time.sleep(1)
        if False:
            sensorReadingR = ReadSensor(solarSensorRight)
            sensorReadingL = ReadSensor(solarSensorLeft)

            signalDifference = abs(sensorReadingL - sensorReadingL)
            #debug! checking for 0s
            if sensorReadingR == 0:
                print('right sensor is 0!!!')
            if sensorReadingL == 0:
                print('left sensor is 0!!!')
