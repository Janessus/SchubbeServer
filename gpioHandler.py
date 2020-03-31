import sys
import time
import traceback

import submodules.gpioReceiver as sub
import JPrinter as log

automode = True
log.logInfo("Starting GPIO Thread")
# set initial states for gpio's
global light1
global light2
global ventilator
global smokeSensor
global de_smoker
bias = 0


def init():
    global light1
    global light2
    global ventilator
    global smokeSensor
    global automode
    global de_smoker

    automode = True
    log.logInfo("Starting GPIO Thread")
    # set initial states for gpio's
    light1 = sub.Light("light1", 16)
    light2 = sub.Light("light2", 20)
    ventilator = sub.Ventilator("ventilator", 21)
    smokeSensor = sub.SmokeSensor("smokesensor", -1)
    de_smoker = sub.AutoMode(smokeSensor, ventilator)


def tearDown():
    log.logInfo("GPIO-Handler shutting down...")
    # set final states for gpio's
    sys.exit(1)


def startThread(gpioQueue):
    init()
    readCommand(gpioQueue)
    tearDown()


def readCommand(gpioQueue):
    # main loop for this handler
    while True:
        message = str("")
        try:
            if not gpioQueue.empty():
                message = str(gpioQueue.get())
                log.logInfo("Message: " + message)
            else:
                de_smoker.autoMode()
                print(str(smokeSensor.getValue()))
                time.sleep(.51) # for debugging .5 in normal operation .1
        except:
            log.logError("Exception in GpioHandler shutting down thread...\n" + traceback.format_exc())
            break

        if message.strip() == "bye":
            break
        elif message.strip() == "help":
            help()
        elif message.strip() == "test":
            test()
        elif message.startswith("auto"):
            de_smoker.action(message[4:].strip())
        elif message.startswith("light1"):
            light1.action(message[6:].strip())
        elif message.startswith("light2"):
            light2.action(message[6:].strip())
        elif message.startswith("ventilator"):
            ventilator.action(message[10:].strip())
        else:
            if message != "":
                log.logWarning("Bad Format")


def test():
    log.logInfo("OOOOOHHH NEIIIN DAS ... DAS WUSSTE ICH NICHT\nAAAABER CAAAAAAAAAAAAAAAARRRRRRRRRRRRRLLLLLLLLLLLLLLL")


def help():
    print("Usage: gpio [Receiver][Action]\n" +
          "Receivers are:\n" +
          "    ventilator\n" +
          "    light1\n" +
          "    light2\n" +
          "    auto\n" +
          "\n" +
          "Actions are:\n" +
          "    on\n" +
          "    off\n" +
          "    auto\n" +
          "\n" +
          "Examples:\n" +
          "    gpio ventilator on\n" +
          "    gpio light1 auto\n" +
          "    gpio auto on\n" +
          "   gpio auto setupper 1234\n")
