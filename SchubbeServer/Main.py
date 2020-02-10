import socket
import sys
import traceback
from threading import Thread

import clientHandler
import gpioHandler
import scriptExecutor
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

    # GPIO Thread
    gpioHandlerThread = Thread(target=gpioHandler.readCommand, args=(gpioQueue,))
    gpioHandlerThread.start()
    threads.append((gpioHandlerThread, gpioQueue))

    # Executor Thread
    executorHandlerThread = Thread(target=scriptExecutor.readCommand, args=(executorQueue,))
    executorHandlerThread.start()
    threads.append((executorHandlerThread, executorQueue))

    # get instance
    server_socket = socket.socket()

    # bind host address and port together
    server_socket.bind((host, port))
    try:
        while True:
            print("Waiting for connection...")
            # configure how many client the server can listen simultaneously
            server_socket.listen(maxClients)
            conn, address = server_socket.accept()  # accept new connection
            print("New connection: " + str(address[:]))

            dtoDCH = DtoClientHandler(conn, gpioQueue, executorQueue)

            # Client Handler Thread
            t = Thread(target=clientHandler.clientHandler, args=(dtoDCH,))
            t.start()
            threads.append((t, dtoDCH))

    except KeyboardInterrupt:
        print("\nMain -- Terminated by user")
    except:
        print("An exception occurred" + traceback.format_exc())
    finally:
        print("Cleaning up...")
        gpioQueue.put("bye")
        executorQueue.put("bye")

        try:
            server_socket.close()
            conn.close()  # close the connection
        except UnboundLocalError:
            print("UnboundLocalError")
        finally:
            global run
            run = False

            for (t, q) in threads:
                try:
                    t.join(2)
                except RuntimeError:
                    pass
                except:
                    print(traceback.format_exc())

            print("Exiting...")
            sys.exit()


if __name__ == '__main__':
    main()
