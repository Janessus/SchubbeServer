import socket
import sys
import traceback
from threading import Thread

import clientHandler
import gpioHandler
import scriptExecutor
import API
from globals import *


# find local ip
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# Listen for new Clients and handle them in a new Thread each
def main():
    host = get_ip()
    port = 5000  # initiate port above 1024
    maxClients = 10
    print("Server Starting on " + host + ":" + str(port))

    queues = list()

    gpioQueue = JQueue()
    queues.append(DtoQueues("gpio", gpioQueue))

    executorQueue = JQueue()
    queues.append(DtoQueues("exec", executorQueue))

    apiQueue = JQueue()
    queues.append(DtoQueues("api", apiQueue))

    # GPIO Thread
    gpioHandlerThread = Thread(target=gpioHandler.readCommand, args=(gpioQueue,))
    gpioHandlerThread.start()
    threads.append((gpioHandlerThread, gpioQueue))

    # Executor Thread
    executorHandlerThread = Thread(target=scriptExecutor.readCommand, args=(executorQueue,))
    executorHandlerThread.start()
    threads.append((executorHandlerThread, executorQueue))

    #start API
    API.start(host, queues)


if __name__ == '__main__':
    main()
