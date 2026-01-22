import time
from abc import ABC, abstractmethod

from common_lib.Thread.abThreading import abThreading


class abThreadingControlled ( abThreading , ABC ):

    def __init__(self,thread_controller , name, sleep_time=0):
        abThreading.__init__(self,sleep_time = sleep_time)
        self._thread_controller = thread_controller
        self._name = name
    def run(self):

        try:
            while not self.IsStop():
                self.HandleThread()
                time.sleep(self._sleep_time)
        except Exception as e:
            print(f"error:{e}")
            self.setException(e)

    def getName(self):
        return self.name

    def setException(self , e ):
        self._thread_controller.setException(e , self)
        pass

    @abstractmethod
    def HandleThread(self):
        print("abThreading ")
        pass
