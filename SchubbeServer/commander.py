from globals import JQueue
from globals import StopSigException
from globals import DtoAPI


def isCommand(cmd):
    if cmd.startswith('/'):
        return True


def dispatchCommand(commandString, dto: list):
    print("Delegating...")
    if isCommand(commandString):
        cmd = str(commandString)
        print("Cmd = " + cmd)
        if cmd.startswith("/bye"):
            raise StopSigException

        # GPIO
        elif cmd.startswith("/gpio"):
            print("GPIO Command")
            for q in dto:
                if q.name == 'gpio':
                    q.queue.put(cmd[6:])

        # EXECUTOR
        elif cmd.startswith("/exec"):
            print("Executor Command")
            for q in dto:
                if q.name == 'exec':
                    q.queue.put(cmd[6:])

    else:
        print("Not a valid Command")
