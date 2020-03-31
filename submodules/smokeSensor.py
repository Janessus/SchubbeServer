
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
# import RPi.GPIO as gpio


def init():
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)
    # you can specify an I2C adress instead of the default 0x48
    # ads = ADS.ADS1115(i2c, address=0x49)

    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)

    # Create differential input between channel 0 and 1
    # chan = AnalogIn(ads, ADS.P0, ADS.P1)

    # pin = 2
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pin, GPIO.OUT)
    # GPIO.output(pin, GPIO.LOW)
    return chan


def getADCValue(chan):
    return chan.value


def getADCVoltage(chan):
    return chan.voltage


'''
def printValues(chan):
    print("{:>5}\t{:>5}".format('raw', 'v'))
    while True:
        print("values without formatting: " + chan.value + ", " + chan.voltage + "v")
        print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
        time.sleep(0.5)


def main():
    printValues(init())
'''
