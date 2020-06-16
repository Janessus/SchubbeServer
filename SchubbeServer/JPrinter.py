import datetime


levels = {"NONE": 0,
          "ERROR": 1,
          "WARNING": 2,
          "INFO": 3}

levelsR = {0: "NONE",
           1: "ERROR",
           2: "WARNING",
           3: "INFO"}

outputLevel = levels["WARNING"]


def logInfo(message):
    if outputLevel == levels["INFO"]:
        print(message)
    writeLog(levels["INFO"], message)


def logWarning(message):
    if outputLevel >= levels["WARNING"]:
        print(message)
    writeLog(levels["WARNING"], message)


def logError(message):
    if outputLevel >= levels["ERROR"]:
        print(message)
    writeLog(levels["ERROR"], message)


def writeLog(outputLevel, message):
    logFile = open("JPrinter.log", "a")
    date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    loggedMessage = str(levelsR[outputLevel]) + " --- " + date + " --- " + str(message).replace("\n", " ") + "\n"
    logFile.write(loggedMessage)
    logFile.close()