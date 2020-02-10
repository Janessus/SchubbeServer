from globals import JQueue
from globals import StopSigException
from globals import DtoClientHandler


def isCommand(cmd):
    if cmd.startswith('/'):
        return True


def dispatchCommand(commandString, dto: DtoClientHandler):
    print("Delegating...")
    if isCommand(commandString):
        cmd = str(commandString)
        print("Cmd = " + cmd)
        if cmd.startswith("/bye"):
            raise StopSigException

        # GPIO
        elif cmd.startswith("/gpio"):
            print("GPIO Command")
            dto.gpioQueue.put(cmd[6:])

        # EXECUTOR
        elif cmd.startswith("/exec"):
            print("Executor Command")
            dto.executorQueue.put(cmd[6:])

    else:
        print("Not a valid Command")
