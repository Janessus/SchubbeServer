import runpy
import sys
import time
import traceback

from globals import *


def test():
    print("Executor Test AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHH!!!!!")
    execute("executorTest")


def execute(script):
    print("Executing " + script)
    try:
        runpy.run_path(path_name="./scripts/" + script + ".py")
    except:
        print("Cannot run desired script")


def readCommand(executorQueue):
    print("Starting ScriptExecutor")

    while True:
        message = str("")
        try:
            if not executorQueue.empty():
                message = str(executorQueue.get())
                print("Message: " + message)
            else:
                time.sleep(1)
        except:
            print("Exception in ScriptExecutor shutting down thread...\n" + traceback.format_exc())
            break

        if message.strip() == "bye":
            break
        elif message.strip() == "test":
            test()
        else:
            if message != "":
                execute(message.strip()) # todo check if script is available

    print("ScriptExecutor shutting down...")
    sys.exit(1)
