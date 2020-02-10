import sys
import time
import traceback

import commander
from globals import DtoClientHandler, StopSigException, threads, run


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
                print("connection closed")

            if not data:
                # if data is not received break
                break

            print("from connected user: " + str(data[:-1]))
            commander.dispatchCommand(data, dtoCH)
    except StopSigException:
        pass
    except:
        print("Exception in clientHandler:\n" + traceback.format_exc())
    finally:
        print("ClientHandler shutting down...")
        try:
            dtoCH.con.close()
        except: pass

        try:
            if not run:
                commander.dispatchCommand("/gpio bye", dtoCH)
        except StopSigException: pass
        except: print("no delegation" + traceback.format_exc())

        sys.exit(1)
