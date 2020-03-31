import sys
import time
import traceback
import socket

import dispatcher
from globals import DtoClientHandler, StopSigException, threads, run
import JPrinter as log


def clientHandler(dtoCH: DtoClientHandler):
    try:
        global run
        dtoCH.con.setblocking(0)
        while run:
            try:
                # receive data stream. it won't accept data packet greater than 1024 bytes
                data = dtoCH.con.recv(1024).decode()
            except BlockingIOError:
                time.sleep(.5)
                continue
            except OSError:
                log.logWarning("connection closed")

            if not data:
                # if data is not received break
                break

            log.logInfo("from connected user: " + str(data[:-1]))
            if data != "":
                dispatcher.dispatchCommand(data, dtoCH)
            data = ""
    except StopSigException:
        pass
    except:
        log.logError("Exception in clientHandler:\n" + traceback.format_exc())
    finally:
        log.logWarning("ClientHandler shutting down...")
        try:
            if not run:
                dispatcher.dispatchCommand("/gpio bye", dtoCH)

            dtoCH.con.shutdown(socket.SHUT_RDWR)
            dtoCH.con.close()
        except StopSigException:
            pass
        except:
            log.logError("no delegation" + traceback.format_exc())

        sys.exit(1)
