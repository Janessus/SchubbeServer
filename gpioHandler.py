import sys
import time
import traceback

import submodules.gpioReceiver as sub
import JPrinter as log

automode = True
log.logInfo("Starting GPIO Thread")
# set initial states for gpio's
light1 = sub.Light("light1", 0)
light2 = sub.Light("light2", 1)
ventilator = sub.Ventilator("ventilator", 2)
smokeSensor = sub.SmokeSensor("smokesensor", -1)

de_smoker = sub.AutoMode(smokeSensor, ventilator)

bias = 0


def init():
    pass


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
                time.sleep(.1)
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
          "    all\n" +
          "\n" +
          "Actions are:\n" +
          "    on\n" +
          "    off\n" +
          "    auto\n" +
          "\n" +
          "Examples:\n" +
          "    gpio ventilator on" +
          "    gpio light1 auto")
