import socket
import sys
import traceback
from threading import Thread
import time

import clientHandler
import gpioHandler
import scriptExecutor
from globals import *
import JPrinter as log


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
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    return IP


# Listen for new Clients and handle them in a new Thread each
def main():
    host = get_ip()
    port = 5000  # initiate port above 1024
    maxClients = 10
    log.logWarning("Server Starting on " + host + ":" + str(port))

    # get instance
    server_socket = socket.socket()
    server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind host address and port together
    while True:
        try:
            server_socket.bind((host, port))
            break
        except OSError:
            log.logWarning("Something went wrong... trying again...")
            time.sleep(5)

    queues = list()

    gpioQueue = JQueue()
    queues.append(DtoQueues("gpio", gpioQueue))

    executorQueue = JQueue()
    queues.append(DtoQueues("exec", executorQueue))

    # GPIO Thread
    gpioHandlerThread = Thread(target=gpioHandler.startThread, args=(gpioQueue,))
    gpioHandlerThread.start()
    threads.append((gpioHandlerThread, gpioQueue))

    # Executor Thread
    executorHandlerThread = Thread(target=scriptExecutor.readCommand, args=(executorQueue,))
    executorHandlerThread.start()
    threads.append((executorHandlerThread, executorQueue))



    try:
        log.logInfo("Waiting for new connection...")
        while True:
            # configure how many client the server can listen simultaneously
            server_socket.listen(maxClients)
            conn, address = server_socket.accept()  # accept new connection
            log.logWarning("New client: " + str(address[:]))

            dtoDCH = DtoClientHandler(conn, gpioQueue, executorQueue)

            # Client Handler Thread
            t = Thread(target=clientHandler.clientHandler, args=(dtoDCH,))
            t.start()
            threads.append((t, dtoDCH))
    except KeyboardInterrupt:
        log.logWarning("\nMain -- Terminated by user")
    except:
        log.logError("An exception occurred" + traceback.format_exc())
    finally:
        log.logInfo("Cleaning up...")
        gpioQueue.put("bye")
        executorQueue.put("bye")

        try:
            server_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()  # close the connection
        except UnboundLocalError:
            log.logError("UnboundLocalError")
        finally:
            global run
            run = False

            for (t, q) in threads:
                try:
                    t.join(2)
                except RuntimeError:
                    pass
                except:
                    log.logError(traceback.format_exc())

            print("Exiting...")
            sys.exit()


if __name__ == '__main__':
    main()
