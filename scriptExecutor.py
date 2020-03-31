import runpy
import sys
import time
import traceback

from globals import *
import JPrinter as log

def test():
    log.logInfo("Executor Test AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHH!!!!!")
    execute("executorTest")


def execute(script):
    log.logInfo("Executing " + script)
    try:
        runpy.run_path(path_name="./scripts/" + script + ".py")
    except:
        log.logWarning("Cannot run desired script")


def readCommand(executorQueue):
    log.logInfo("Starting ScriptExecutor")

    while True:
        message = str("")
        try:
            if not executorQueue.empty():
                message = str(executorQueue.get())
                log.logInfo("Message: " + message)
            else:
                time.sleep(1)
        except:
            log.logError("Exception in ScriptExecutor shutting down thread...\n" + traceback.format_exc())
            break

        if message.strip() == "bye":
            break
        elif message.strip() == "test":
            test()
        else:
            if message != "":
                execute(message.strip()) # todo check if script is available

    log.logInfo("ScriptExecutor shutting down...")
    sys.exit(1)
