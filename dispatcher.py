from globals import StopSigException
from globals import DtoClientHandler
import JPrinter as log


def dispatchCommand(commandString, dto: DtoClientHandler):
    log.logInfo("Dispatching...")
    if commandString.startswith('/'):
        cmd = str(commandString).rstrip("\n\r")
        log.logInfo("Cmd = " + cmd)
        if cmd.startswith("/bye"):
            raise StopSigException

        # GPIO
        elif cmd.startswith("/gpio"):
            log.logInfo("GPIO Command")
            dto.gpioQueue.put(cmd[6:])

        # EXECUTOR
        elif cmd.startswith("/exec"):
            log.logInfo("Executor Command")
            dto.executorQueue.put(cmd[6:])
    else:
        log.logWarning("Not a valid Command")
