import JPrinter as log
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO


GPIO.setup(GPIO.BCM) # GPIO number not pin number!!

class GPIOReceiver:
    def __init__(self, name, pinNumber):
        self.name = name
        self.pinNumber = pinNumber
        self.__state = "blank"
        if self.pinNumber != -1:
            GPIO.output(self.pinNumber, GPIO.LOW)

    def action(self, action):
        pass

    def getState(self):
        return self.__state


class AutoMode:
    def __init__(self, smokeSensor, ventilator):
        self.smokeSensor = smokeSensor
        self.ventilator = ventilator
        self.__upper = 0
        self.__lower = 0
        self.__state = "inactive"         # valid states: active, inactive

    def setUpperBound(self, value):
        self.__upper = value

    def setLowerBound(self, value):
        self.__lower = value

    def setState(self, state):
        self.__state = state

    def action(self, action):
        log.logInfo(self.name + " with PinNo: " + str(self.pinNumber))
        if action == "on":
            self.setState("active")
        elif action == "off":
            self.setState("inactive")
        elif action.startswith("setupper"):
            self.setUpperBound(action[len("setupper"):].strip())
        elif action.startswith("setlower"):
            self.setLowerBound(action[len("setlower"):].strip())

    def autoMode(self):
        if self.getState() == "active":
            smokeLevel = self.smokeSensor.getValue()
            if smokeLevel > self.__upper and self.ventilator.getState() == "off":
                self.ventilator.on()
                log.logInfo("De-Smoking...")
            elif smokeLevel < self.__lower and self.ventilator.getState() == "on":
                self.ventilator.off()
                log.logInfo("De-Smoking done!")



class SmokeSensor(GPIOReceiver):
    chan = None

    def __init(self, name, pinNumber):
        GPIOReceiver.__init__(self, name, pinNumber)

    def action(self, action):
        log.logInfo(self.name + " with PinNo: " + str(self.pinNumber))
        if action == "init":
            self.__initADC()
        elif action == "getvalue":
            self.getValue()
        elif action == "getvoltage":
            self.getVoltage()

    def __initADC(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # you can specify an I2C adress instead of the default 0x48
        # ads = ADS.ADS1115(i2c, address=0x49)

        # Create single-ended input on channel 0
        self.chan = AnalogIn(ads, ADS.P0)

        # Create differential input between channel 0 and 1
        # chan = AnalogIn(ads, ADS.P0, ADS.P1)

    def getValue(self):
        return self.chan.value

    def getVoltage(self):
        return self.chan.voltage


class Light(GPIOReceiver):
    def action(self, action):
        log.logInfo(self.name + " with PinNo: " + str(self.pinNumber))
        if action == "on":
            self.on()
        elif action == "off":
            self.off()
        elif action == "auto":
            self.auto()

    def on(self):
        log.logInfo(self.name + " On")
        GPIO.output(self.pinNumber, GPIO.HIGH)
        self.state = "on"

    def off(self):
        log.logInfo(self.name + " Off")
        GPIO.output(self.pinNumber, GPIO.LOW)
        self.state = "off"

    def auto(self):
        log.logInfo(self.name + " auto")




class Ventilator(GPIOReceiver):
    def action(self, action):
        log.logInfo(self.name + " with PinNo: " + str(self.pinNumber))
        if action == "on":
            self.on()
        elif action == "off":
            self.off()
        elif action == "auto":
            self.auto()

    def on(self):
        log.logInfo(self.name + " On")
        GPIO.output(self.pinNumber, GPIO.HIGH)
        self.state = "on"

    def off(self):
        log.logInfo(self.name + " Off")
        GPIO.output(self.pinNumber, GPIO.LOW)
        self.state = "off"

    def auto(self):
        log.logInfo(self.name + " auto")
