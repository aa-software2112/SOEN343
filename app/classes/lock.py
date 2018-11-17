import threading


class ReadWriteLock:
    """
    An implementation of a lock following the Readers-Writers Problem #4
    from "Concurrent Programming Concepts" by Constantinos Constantinides.

    A process can read if there are no writers in and no writers waiting.
    A process can write if there are no readers reading and no writers waiting.
    """

    def __init__(self):
        self._rw_lock = threading.Condition(threading.Lock())
        self._lock = threading.Lock()
        self._num_of_readers = 0
        self._readers_waiting = 0
        self._writers_waiting = 0

    def start_read(self):
        with self._lock:
            self._readers_waiting += 1

        self._rw_lock.acquire()

        while self._writers_waiting > 0:
            self._rw_lock.wait()
        try:
            self._num_of_readers += 1
            self._readers_waiting -= 1
        finally:
            self._rw_lock.release()

    def end_read(self):
        self._rw_lock.acquire()
        try:
            self._num_of_readers -= 1
            if self._num_of_readers == 0:
                self._rw_lock.notify_all()
        finally:
            self._rw_lock.release()

    def start_write(self):
        with self._lock:
            self._writers_waiting += 1

        self._rw_lock.acquire()

        while self._num_of_readers > 0 or self._writers_waiting > 1:
            self._rw_lock.wait()

        with self._lock:
            self._writers_waiting -= 1

    def end_write(self):
        try:
            self._rw_lock.notify_all()
        finally:
            self._rw_lock.release()
