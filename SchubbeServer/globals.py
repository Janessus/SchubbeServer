from threading import Lock
threads = []


run = True


class StopSigException(Exception):
    pass


class JQueue:
    def __init__(self):
        self.data = list()
        self.lock = Lock()

    def put(self, item):
        self.lock.acquire()
        self.data.append(item)
        self.lock.release()

    def get(self):
        self.lock.acquire()
        val = self.data.pop(0)
        self.lock.release()
        return val

    def empty(self):
        self.lock.acquire()
        if len(self.data) == 0:
            self.lock.release()
            return True
        self.lock.release()
        return False


class DtoAPI:
    def __init__(self, addr, queues: list):
        self.addr = addr
        self.queues = queues


class DtoClientHandler:
    def __init__(self, con, q: JQueue, eq: JQueue):
        self.con = con
        self.gpioQueue = q
        self.executorQueue = eq


class DtoQueues:
    def __init__(self, name, myQueue: JQueue):
        self.name = str(name)
        self.queue = myQueue

