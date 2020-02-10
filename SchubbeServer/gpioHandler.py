import time
import sys
import traceback
from globals import *


def test():
    print("OOOOOHHH NEIIIN DAS ... DAS WUSSTE ICH NICHT\nAAAABER CAAAAAAAAAAAAAAAARRRRRRRRRRRRRLLLLLLLLLLLLLLL")


def readCommand(gpioQueue):
    print("Starting GPIO Thread")

    while True:
        message = str("")
        try:
            if not gpioQueue.empty():
                message = str(gpioQueue.get())
                print("Message: " + message)
            else:
                time.sleep(1)
        except:
            print("Exception in GpioHandler shutting down thread...\n" + traceback.format_exc())
            break

        if message.strip() == "bye":
            break
        elif message.strip() == "test":
            test()
        else:
            if message != "":
                print("Message was: " + message)

    print("GPIO-Handler shutting down...")
    sys.exit(1)
