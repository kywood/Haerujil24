import multiprocessing
from typing import List

from common_lib.Dtos.IDto import IDTO
from common_lib.MessageQueue.MessageChannelDTO import MessageChennelDTOContainer
from common_lib.Thread.abThread import abThread
from common_lib.multiProcess.abProcess import abProcess




class ProcessingDTO(IDTO):

    def __init__(self,_process,_abprocess:abProcess):
        super().__init__()
        self.processing_process=_process
        self.abprocess=_abprocess
    def GetProcessingProcess(self):
        return self.processing_process
    def GetProcess(self):
        return self.abprocess



# class cMultiProcesser(abThread, SingletonInstane):
class MultiProcesser(abThread , abProcess):

    def __init__(self,  messageChennelDTOContainer : MessageChennelDTOContainer ,  process_size=0):
        abThread.__init__(self)
        abProcess.__init__(self ,"MultiProcesser")

        # self._messageQueue = messageQueue

        self.Init(process_size)
        # abThread.OnInit(self)

    def Init(self, process_size : int = 0 ):
        # self.OnInit()

        from queue import Queue
        self._processReadyQueue = Queue()
        # self.processingList = Manager().list()
        self._processingList = []

        if process_size == 0:
            import math
            self._process_size = math.ceil(multiprocessing.cpu_count() * 2.5)
        else:
            self._process_size = process_size

        # self.process_size=_process_size
        self._lock = multiprocessing.Lock()

        return self

    def ShutDown(self):
        # self.shardConfigQueue[E_MP_CONFIG_KEY.COMMUNICATION] = E_MP_COMMUNICATION_MES.SHUTDOWN
        pass

    def ShutDownBlank(self):
        # print("A")
        pass

    def Append(self, process:abProcess):
        with self._lock:
            self._processReadyQueue.put( process )

        return self

    def AppendLists(self, process_lists:List[abProcess]):
        with self._lock:
            for process in process_lists:
                self._processReadyQueue.put( process )

        return self


    def RunAsync(self):
        # self.Start()
        self.Start()
        # abThread.Start(self)

    def Start(self):
        abThread.Start(self)


        pass
    ## thread Call
    def HandleProcess(self , process):
        # self.Run()
        pass
    #
    def HandleThread(self):
        self.Run()
        pass


    def IsEmptySubProcess(self):
        if self._processReadyQueue.empty() and len(self._processingList) == 0:
            return True

        return False


    def Run(self):
        while True:

            if self.IsStop() :
                print("thread Stoped!! force Stop!!")
                return

            with self._lock:

                if self._processReadyQueue.empty() and len(self._processingList) == 0:
                    print("empty work")
                    return

            # allocation process
            with self._lock:

                processingStartQueue = []
                while not self._processReadyQueue.empty() and len(self._processingList) < self._process_size:
                    process = self._processReadyQueue.get()

                    processing = multiprocessing.Process(target=process.HandleProcess, args=(process,))
                    # processing.start()
                    processingStartQueue.append(processing)
                    self._processingList.append( ProcessingDTO( processing , process ) )
                    print("nwe release---------- " + process.GetName())
                    # print("a")
                while processingStartQueue:
                    prc=processingStartQueue.pop(0)
                    prc.start()
                    print("new start---------- " + prc.name)

