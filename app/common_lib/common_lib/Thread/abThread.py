import threading
from abc import abstractmethod, ABC
from enum import Enum



class cThreadEvent:
    def __init__(self):
        self.vset=False
    def evt_set(self):
        self.vset=True
        return self.vset
    def evt_reset(self):
        self.vset=False
        return self.vset
    def evt_clear(self):
        self.vset=False
    def evt_is_set(self):
        return self.vset


class abThread ( threading.Thread , cThreadEvent , ABC ):
    class E_THREAD_STATUS(Enum):
        WAITING = 0
        RUNNING = 1
        STOPING = 2
    def __init__( self ):
        threading.Thread.__init__(self)
        cThreadEvent.__init__(self)

        self.thread_status = abThread.E_THREAD_STATUS.WAITING
        # super( abThread , self ).__init__()
        # self._stop = threading.Event()
        # self.thread_status = abThread.E_THREAD_STATUS.WAITING

    #
    # def OnInit(self):
    #     # self._stop = threading.Event()
    #     self.thread_status = abThread.E_THREAD_STATUS.WAITING
    #     pass

    def setThreadStatus(self , _status ):
        self.thread_status=_status

    def GetThreadStatus(self):
        return self.thread_status

    def Stop(self):
        # self._stop.set()
        self.evt_set()
        self.setThreadStatus(abThread.E_THREAD_STATUS.STOPING)

    def IsStop(self):
        return self.evt_is_set()
        # return self._stop.isSet()

    def IsRunning(self):
        return not self.IsStop()

    def Start(self):
        self.start()
        self.evt_clear()
        # self._stop.clear()
        self.setThreadStatus(abThread.E_THREAD_STATUS.RUNNING)

    def run(self):
        self.Action()
        self.Stop()

    @abstractmethod
    def Action(self):
        print("abThread ")
        pass

